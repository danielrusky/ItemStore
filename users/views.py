import secrets
import string

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from config import settings
from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, FormView, TemplateView
from users.forms import UserRegisterForm, UserProfileForm
from users.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import login


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        new_user = form.save()
        # Генерируем уникальный код, например, UUID
        import uuid
        verification_code = str(uuid.uuid4())
        new_user.verification_code = verification_code
        new_user.save()

        # Генерируем полный URL для активации
        activation_path = reverse('users:verify_email', kwargs={'token': verification_code})
        activation_url = self.request.build_absolute_uri(activation_path)

        send_mail(
            subject='Активация аккаунта на нашей платформе',
            message=f'Ссылка для активации учетной записи: {activation_url}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[new_user.email],
            fail_silently=False,
        )
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


def generate_new_password(request):
    new_password = create_secret_key(12)
    request.user.set_password(new_password)
    request.user.save()
    send_mail(
        subject='Вы сменили пароль из профиля',
        message=f'Новый пароль {new_password}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email]
    )
    return redirect(reverse_lazy('users:login'))


def create_secret_key(length):
    combination = string.ascii_letters + string.digits
    secret_key = ''.join(secrets.choice(combination) for _ in range(length))
    return secret_key


class VerifyEmail(View):
    def get(self, request, token):
        try:
            user = User.objects.get(verification_code=token)
            user.is_active = True
            user.save()
            return redirect('users:success_verify')
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return redirect('users:error_verify')


class SuccessVerifyView(TemplateView):
    template_name = 'users/success_verify.html'


class ErrorVerifyView(TemplateView):
    template_name = 'users/error_verify.html'
