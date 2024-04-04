from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status

from .models import *
from .serializers import *

class SubjectsAPIView(APIView):
    def get(self, request):
        subjects = Subject.objects.all()
        serializer = SubjectSerializer(subjects, many=True)
        return Response(serializer.data)

class SubjectTests(APIView):
    def get(self, request, pk):
        tests = Test.objects.filter(subject__id=pk)
        serializer = TestSerializer(tests, many=True)
        return Response(serializer.data)

