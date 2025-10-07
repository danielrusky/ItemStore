from django.urls import path
from materials.views import *
from materials.apps import MaterialsConfig

app_name = MaterialsConfig.name

urlpatterns = [
    path("", MaterialListView.as_view(), name="material_list"),
    path("material_create/", MaterialCreateView.as_view(), name="material_create"),
    path("material_edit/<int:pk>", MaterialUpdateView.as_view(), name="material_edit"),
    path("material_view/<int:pk>", MaterialDetailView.as_view(), name="material_view"),
    path("material_delete/<int:pk>", MaterialDeleteView.as_view(), name="material_delete"),
    path("like/<int:pk>", LikeRecord.as_view(), name="like"),
    path("dislike/<int:pk>", DislikeRecord.as_view(), name="dislike"),
]