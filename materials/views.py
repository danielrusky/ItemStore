from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from pytils.translit import slugify

from materials.models import Material


class MaterialListView(ListView):
    model = Material
    extra_context = {
        'title': 'Материалы',
    }

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset


class MaterialCreateView(CreateView):
    model = Material
    fields = ('title', 'body', 'image',)
    success_url = reverse_lazy('materials:list_material')

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)
            new_mat.save()

        return super().form_valid(form)


class MaterialDetailView(DetailView):
    model = Material
    fields = ('title', 'body', 'image', 'is_published', 'views_count')
    success_url = reverse_lazy('materials:list_material')

    def get_object(self, queryset=None):
        obj = super().get_object()
        obj.views_count += 1
        if obj.views_count == 100:
            send_mail(
                subject='Уведомление о достижении',
                message='Поздравляем! Статья набрала 100 просмотров в блоге.',
                from_email='reaver74@yandex.ru',
                recipient_list=['reaver_std@mail.ru'],
                fail_silently=False
            )

        obj.save()
        return obj


class MaterialUpdateView(UpdateView):
    model = Material
    fields = ('title', 'body', 'image',)

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)
            new_mat.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('materials:view_material', args=[self.kwargs.get('pk')])


class MaterialDeleteView(DeleteView):
    model = Material
    success_url = reverse_lazy('materials:list_material')


def toggle_active(request, slug):
    material = get_object_or_404(Material, slug=slug)
    if material.to_publish:
        material.to_publish = False
    else:
        material.to_publish = True
    material.save()
    return redirect('material_detail', slug=material.slug)