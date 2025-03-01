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
            majors = majors.filter(name__icontains = search_name)
        serializer = MajorSerializer(majors, many=True)
        return Response(serializer.data)

class SubjectsAPIView(APIView):
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('name', openapi.IN_QUERY, description="Search by name", type=openapi.TYPE_STRING),
        openapi.Parameter('is_mandatory', openapi.IN_QUERY, description="Search by if mandatory or not", type=openapi.TYPE_BOOLEAN),
    ])
    def get(self, request):
        subjects = Subject.objects.all()
        sub_name = request.query_params.get("name")
        mandatory = request.query_params.get("is_mandatory")
        if sub_name:
            subjects = subjects.filter(name__icontains = sub_name)
        if mandatory:
            subjects = subjects.filter(is_mandatory = mandatory)
        serializer = SubjectSerializer(subjects, many=True)
        return Response(serializer.data)

class GenerateExamAPIView(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request, major_id):
        major = get_object_or_404(Major, id=major_id)

        main_test = Test.objects.filter(subject=major.main).order_by('?').first()
        secondary_test = Test.objects.filter(subject=major.secondary).order_by('?').first()

        mandatory_subjects = Subject.objects.filter(is_mandatory=True)
        mandatory_tests = []
        for subject in mandatory_subjects:
            test = Test.objects.filter(subject=subject).order_by('?').first()
            if test:
                mandatory_tests.append(test)

        if not main_test or not secondary_test or len(mandatory_tests) < 3:
            return Response({"error": "Insufficient test data for the selected major."},
                            status=status.HTTP_400_BAD_REQUEST)

        main_test_serializer = TestSerializer(main_test)
        secondary_test_serializer = TestSerializer(secondary_test)
        mandatory_tests_serializer = TestSerializer(mandatory_tests, many=True)

        response_data = {
            "main_test": main_test_serializer.data,
            "secondary_test": secondary_test_serializer.data,
            "mandatory_tests": mandatory_tests_serializer.data,
        }
        return Response(response_data, status.HTTP_200_OK)

class GenerateExamBySubjects(APIView):
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('main_subject_id', openapi.IN_QUERY, description="ID of the main subject", type=openapi.TYPE_INTEGER),
        openapi.Parameter('secondary_subject_id', openapi.IN_QUERY, description="ID of the secondary subject", type=openapi.TYPE_INTEGER)
    ])
    def get(self, request):
        main_subject_id = request.query_params.get('main_subject_id')
        secondary_subject_id = request.query_params.get('secondary_subject_id')

        if not main_subject_id or not secondary_subject_id:
            return Response({"error": "Both main_subject_id and secondary_subject_id are required."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            main_subject = Subject.objects.get(id=main_subject_id)
            secondary_subject = Subject.objects.get(id=secondary_subject_id)
        except Subject.DoesNotExist:
            return Response({"error": "Invalid subject ID(s) provided."},
                            status=status.HTTP_404_NOT_FOUND)

        main_test = Test.objects.filter(subject=main_subject).order_by('?').first()
        secondary_test = Test.objects.filter(subject=secondary_subject).order_by('?').first()

        mandatory_subjects = Subject.objects.filter(is_mandatory=True)
        mandatory_tests = []
        for subject in mandatory_subjects:
            test = Test.objects.filter(subject=subject).order_by('?').first()
            if test:
                mandatory_tests.append(test)

        if not main_test or not secondary_test or len(mandatory_tests) < 3:
            return Response({"error": "Insufficient test data for the selected subjects."},
                            status=status.HTTP_400_BAD_REQUEST)

        main_test_serializer = TestSerializer(main_test)
        secondary_test_serializer = TestSerializer(secondary_test)
        mandatory_tests_serializer = TestSerializer(mandatory_tests, many=True)

        response_data = {
            "main_test": main_test_serializer.data,
            "secondary_test": secondary_test_serializer.data,
            "mandatory_tests": mandatory_tests_serializer.data,
        }
        return Response(response_data, status.HTTP_200_OK)

class StartTest(APIView):
    @swagger_auto_schema(request_body=UserTestSerializer)
    def post(self, request):
        user_test = request.data
        serializer = UserTestSerializer(data=user_test)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)

class UserAllAnswersAPI(APIView):
    def get(self, request, user_test_id):
        user_answers = UserAnswer.objects.filter(user_test = user_test_id)
        serializer = UserAnswerSerializer(user_answers, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    @swagger_auto_schema(request_body=UserAnswerSerializer)
    def post(self, request, user_test_id):
        answer = request.data
        serializer = UserAnswerSerializer(data=answer)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)

class UserAnswerAPI(APIView):
    def get(self, request, answer_id):
        answer = get_object_or_404(UserAnswer.objects.all(), id=answer_id)
        serializer = UserAnswerSerializer(answer)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=UserAnswerSerializer)
    def put(self, request, answer_id):
        answer = get_object_or_404(UserAnswer.objects.all(), id=answer_id)
        data = request.data
        serializer = UserAnswerSerializer(instance=answer, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_202_ACCEPTED)

class FinishTestAPI(APIView):
    pass
