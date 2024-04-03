from django.urls import path

from .views import *

urlpatterns = [
    path("subjects/", SubjectsAPIView.as_view()),
]
