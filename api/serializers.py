from rest_framework import serializers

from .models import (
    Candidate,
    Subject,
    Test,
    Question,
    Answer,
    UserTest,
    Result
)

class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = '__all__'

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

    def to_representation(self, instance):
        instance = super(QuestionSerializer, self).to_representation(instance)
        answers = Answer.objects.filter(question = instance)
        serializer = AnswerSerializer(answers, many=True)
        instance.update({"answers": serializer.data})
        return instance

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'

class UserTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTest
        fields = '__all__'

class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = '__all__'

