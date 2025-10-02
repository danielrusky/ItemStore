from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import contact, ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, \
    ProductDeleteView, CategoryListView, CategoryCreateView, CategoryDetailView, CategoryUpdateView, CategoryDeleteView

app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('product_create/', ProductCreateView.as_view(), name='product_create'),
    path('product_detail/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('product_update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('product_delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
    path('category_list/', CategoryListView.as_view(), name='category_list'),
    path('category_create/', CategoryCreateView.as_view(), name='category_create'),
    path('category_detail/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),
    path('category_update/<int:pk>/', CategoryUpdateView.as_view(), name='category_update'),
    path('category_delete/<int:pk>/', CategoryDeleteView.as_view(), name='category_delete'),
    path('contact/', contact, name='contact'),
]