from django.urls import path

from .views import *

urlpatterns = [
    path("subjects/", SubjectsAPIView.as_view()),
    path("subject/<int:pk>/random_test/", SubjectRandomTest.as_view()),
    path("test/<int:pk>/questions/", TestQuestions.as_view()),
]
