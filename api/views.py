from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
import random

from .models import *
from .serializers import *

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class UserCreateAPIView(APIView):
    @swagger_auto_schema(request_body=CandidateCreateSerializer)
    def post(self, request):
        user = request.data
        serializer = CandidateCreateSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)

class ChangePasswordAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(request_body=ChangePasswordSerializer)
    def put(self, request):
        serializer = ChangePasswordSerializer(instance=self.request.user, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        user = get_object_or_404(Candidate.objects.all(), id=pk)
        serializer = CandidateSerializer(user)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=CandidateCreateSerializer)
    def put(self, request, pk):
        saved_user = get_object_or_404(Candidate.objects.all(), id=pk)
        data = request.data
        serializer = CandidateCreateSerializer(instance=saved_user, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class MajorsAPIView(APIView):
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('name', openapi.IN_QUERY, description="Search by name", type=openapi.TYPE_STRING)
    ])
    def get(self, request):
        search_name = request.query_params.get("name")
        majors = Major.objects.all()
        if search_name:
            majors = majors.filter(name__contains = search_name)
        serializer = MajorSerializer(majors, many=True)
        return Response(serializer.data)
