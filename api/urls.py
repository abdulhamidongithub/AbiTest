from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import *

urlpatterns = [
    path('get_token/', MyTokenObtainPairView.as_view()),
    path('refresh_token/', TokenRefreshView.as_view()),
    path('change_password/', ChangePasswordAPIView.as_view()),
    path('user_create/', UserCreateAPIView.as_view()),
    path('user_details/<int:pk>/', UserAPIView.as_view()),

    path("majors/", MajorsAPIView.as_view()),
    path("subjects/", SubjectsAPIView.as_view()),

    path("generate_exam/<int:major_id>/", GenerateExamAPIView.as_view()),
]

