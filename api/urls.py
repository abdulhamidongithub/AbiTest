from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import *

urlpatterns = [
    path('get_token/', MyTokenObtainPairView.as_view()),
    path('refresh_token/', TokenRefreshView.as_view()),

    path('user_create/', UserCreateAPIView.as_view()),
]
