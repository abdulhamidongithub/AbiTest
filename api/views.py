from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import *
from .serializers import *

class SubjectsAPIView(APIView):
    def get(self, request):
        subjects = Subject.objects.all()
        serializer = SubjectSerializer(subjects, many=True)
        return Response(serializer.data)

