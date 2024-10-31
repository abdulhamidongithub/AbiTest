from django.urls import path

from .views import *

urlpatterns = [
    path("subjects/", SubjectsAPIView.as_view()),
    path("subject/<int:pk>/tests/", SubjectTests.as_view()),
    path("test/<int:pk>/questions/", TestQuestions.as_view()),
]
