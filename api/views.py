from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
import random

from .models import *
from .serializers import *


class SubjectsAPIView(APIView):
    def get(self, request):
        subjects = Subject.objects.all()
        serializer = SubjectSerializer(subjects, many=True)
        return Response(serializer.data)

class SubjectRandomTest(APIView):
    def get(self, request, pk):
        tests = Test.objects.filter(subject__id=pk)
        counter = tests.count()
        rand_num = random.randrange(0, counter)
        serializer = TestSerializer(tests[rand_num])
        return Response(serializer.data)

class TestQuestions(APIView):
    def get(self, request, pk):
        questions = Question.objects.filter(test__id=pk)
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)
