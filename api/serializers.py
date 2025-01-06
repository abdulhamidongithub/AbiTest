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

class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    re_new_password = serializers.CharField(required=True, write_only=True)

    def update(self, instance, validated_data):

        instance.password = validated_data.get('password', instance.password)
        if not validated_data['new_password']:
              raise serializers.ValidationError({'new_password': 'not found'})

        if not validated_data['old_password']:
              raise serializers.ValidationError({'old_password': 'not found'})

        if instance.password != validated_data['old_password']:
              raise serializers.ValidationError({'old_password': 'wrong password'})

        if validated_data['new_password'] != validated_data['re_new_password']:
            raise serializers.ValidationError({'passwords': 'passwords do not match'})

        if validated_data['new_password'] == validated_data['re_new_password'] and instance.password == validated_data['old_password']:
            instance.password = validated_data['new_password']
            instance.save()
            return instance

    class Meta:
        model = Candidate
        fields = ['old_password', 'new_password','re_new_password']

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

class MajorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Major
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
