from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, UpdateView, CreateView, DeleteView, ListView
from catalog.models import Product, Category
from django.urls import reverse_lazy


class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'


class ProductCreateView(CreateView):
    model = Product
    fields = ('name', 'description', 'price', 'image', 'category', 'date_modified')
    template_name = 'catalog/product_form.html'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'


class ProductUpdateView(UpdateView):
    model = Product
    fields = ('name', 'description', 'price', 'image', 'category', 'date_modified')
    success_url = reverse_lazy('catalog:product_list')


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'


class CategoryListView(ListView):
    model = Category
    template_name = 'catalog/category_list.html'


class CategoryCreateView(CreateView):
    model = Category
    fields = ('name', 'description', 'created_at')
    template_name = 'catalog/category_form.html'


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'catalog/category_detail.html'


class CategoryUpdateView(UpdateView):
    model = Category
    fields = ('name', 'description', 'created_at')
    success_url = reverse_lazy('catalog:catalog_list')


class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'catalog/category_confirm_delete.html'



def contact(requests):
    context = {
        'title': 'Контакты'
    }
    if requests.method == 'POST':
        name = requests.POST.get('name')
        email = requests.POST.get('email')
        message = requests.POST.get('message')
        print(f'{name} ({email}):{message}')
    return render(requests, 'catalog/contacts.html', context)

# def view_product(requests, pk):
#     product_item = get_object_or_404(Product, pk=pk)
#     context = {
#         'object': product_item,
#         'title': 'Автомобиль'
#     }
#     return render(requests, 'catalog/product_list.html', context)

# def index(requests):
#     store_list = Product.objects.all()
#     context = {
#         'object_list': store_list,
#         'title': 'Главная'
#     }
#     return render(requests, 'catalog/index.html', context)