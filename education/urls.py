from django.urls import path

from education.apps import EducationConfig
from education.views import education

app_name = EducationConfig.name

urlpatterns = [
    path('education/', education, name='education'),
]