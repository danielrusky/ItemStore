from django.urls import path

from materials.apps import MaterialsConfig
# from catalog.views import ProductListView, ProductDetailView
from materials.views import MaterialCreateView, MaterialListView, MaterialDetailView, MaterialUpdateView, \
    MaterialDeleteView

app_name = MaterialsConfig.name

urlpatterns = [
    path('', MaterialListView.as_view(), name='material_list'),
    path('material_create/', MaterialCreateView.as_view(), name='material_create'),
    path('material_view/<int:pk>/', MaterialDetailView.as_view(), name='material_view'),
    path('material_edit/<int:pk>/', MaterialUpdateView.as_view(), name='material_edit'),
    path('material_delete/<int:pk>/', MaterialDeleteView.as_view(), name='material_delete'),
]