from django.urls import path

from .views import *

urlpatterns = [
    path("subjects/", SubjectsAPIView.as_view()),
    path("subject/<str:pk>/tests/", SubjectTests.as_view()),
]
