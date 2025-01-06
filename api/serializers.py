from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

from .models import (
    Candidate,
    Subject,
    Major,
    Author,
    Test,
    Question,
    UserTest,
    UserAnswer
)

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = Candidate.objects.filter(username=username, password=password).first()
        if user is None:
            raise serializers.ValidationError({
                'success': "false",
                'message': 'User not found'
            }, code=status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(user)
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            "id": user.id,
            "username": username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "phone": user.phone,
            "birth_date": user.birth_date,
            "balance": user.balance,
            "region": user.region,
            "active": user.active
        }


class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields =  [
            "id", "first_name", "last_name", 'phone', "username",
            "balance", "region", "birth_date", "email"
            ]

class CandidateCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = [
            "first_name", "last_name", 'phone', "username",
            "password", "region", "birth_date"
            ]

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class UserTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTest
        fields = '__all__'

class UserTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTest
        fields = '__all__'
