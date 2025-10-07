from typing import Any

from django.core.cache import cache
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, TemplateView, ListView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from catalog.models import Product, Category, Contacts
from catalog.services import get_category_list
from config import settings


class ProductListView(ListView):
    model = Product
    extra_context = {
        'title': 'Главная страница',
    }
    template_name = 'catalog/product_list.html'

    def get_queryset(self, *args, **kwargs):
        # QuerySet — это набор объектов из базы данных, который
        # может использовать фильтры для ограничения результатов
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_active=True)
        return queryset


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    fields = ('name', 'description', 'price', 'image', 'category')
    success_url = reverse_lazy('catalog:list_product')

    def form_valid(self, form):
        # проверка валидации (только create и update)
        # создаем форму, но не отправляем его в БД, пока просто держим в памяти
        # создаем переменную, сохраням и с ней работаем
        # Через реквест передаем недостающую форму, которая обязательна
        # сохраняем в базу данных
        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Product
    fields = ('name', 'description', 'price', 'image', 'category')
    success_url = reverse_lazy('catalog:list_product')


class ProductDetailView(DetailView):
    model = Product
    extra_context = {
        'title': 'Товар',
    }
    template_name = 'catalog/product_detail.html'

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context['categories'] = get_category_list()
        if settings.CACHE_ENABLED:
            key = f'last_{self.object.pk}'
            last = cache.get(key)
            if last is None:
                list = self.object.version_set.all()
                last = sorted(list, key=lambda x: x.add_date, reverse=True)[0]
                cache.set(key, last)
        else:
            list = self.object.version_set.all()
            last = sorted(list, key=lambda x: x.add_date, reverse=True)[0]

        context["last"] = last
        return context

    def get_object(self, queryset: QuerySet[Any] | None = ...) -> Model:
        if settings.CACHE_ENABLED:
            key = f'object_{self.kwargs["pk"]}'
            object = cache.get(key)
            if object is None:
                object = Product.objects.get(pk=self.kwargs['pk'])
                cache.set(key, object)
        else:
            object = Product.objects.get(pk=self.kwargs['pk'])
        return object


class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:list_product')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.user != self.request.user:
            raise Http404

        return self.object

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['categories'] = get_category_list()
        return context


class CategoryListView(ListView):
    model = Category
    extra_context = {
        'title': 'Категории',
    }
    template_name = 'catalog/category_list.html'


class CategoryCreateView(CreateView):
    model = Category
    fields = ('name', 'description', 'image')
    success_url = reverse_lazy('catalog:list_category')

    def form_valid(self, form):
        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class CategoryDetailView(DetailView):
    model = Category
    extra_context = {
        'title': 'Категория',
    }
    template_name = 'catalog/category_detail.html'


class CategoryUpdateView(UpdateView):
    model = Category
    fields = ('name', 'description')
    success_url = reverse_lazy('catalog:list_category')


class CategoryDeleteView(DeleteView):
    model = Category
    success_url = reverse_lazy('catalog:list_category')

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.accepts('text/html'):
            return response
        else:
            return super().form_valid(form.errors)


class ContactsView(TemplateView):
    template_name = 'catalog/contacts.html'
    extra_context = {
        'title': 'Контакты',
    }

    def post(self, request, *args, **kwargs):
        # POST — это запрос, который используется для отправки данных
        # на сервер. Обычно он содержит в своём теле данные, которые
        # предполагается сохранить
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        Contacts.objects.create(name=name, phone=phone, message=message)
        print(f'name: {name}, phone: {phone}, message: {message}')
        return render(request, 'catalog/contacts.html', self.extra_context, {'contacts': Contacts.objects.get(pk=1)})


class ProductThanks(TemplateView):
    model = Product
    http_method_names = ["post"]

    def post(self, request, *args, **kwards):
        return render(request, "catalog/thanks.html")


class ProductAuth(TemplateView):
    model = Product
    http_method_names = ["post", "get"]

    def post(self, request, *args, **kwargs):
        return render(request, "catalog/need.html")
