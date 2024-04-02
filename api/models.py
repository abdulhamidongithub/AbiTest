from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid import uuid4

class Candidate(AbstractUser):
    id = models.UUIDField(default=uuid4, unique=True, editable=False, primary_key=True)
    phone = models.CharField(max_length=30)
    age = models.PositiveSmallIntegerField()
    balance = models.PositiveSmallIntegerField(default=0)
    active = models.BooleanField(default=True)
    region = models.CharField(max_length=30)
    email = None

    def __str__(self):
        return f"{self.username}: {self.first_name} {self.last_name}"

class Subject(models.Model):
    id = models.UUIDField(default=uuid4, unique=True, editable=False, primary_key=True)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=150)

    def __str__(self):
        return self.name

class Test(models.Model):
    id = models.UUIDField(default=uuid4, unique=True, editable=False, primary_key=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    author = models.CharField(max_length=50, blank=True, null=True)

class Question(models.Model):
    id = models.UUIDField(default=uuid4, unique=True, editable=False, primary_key=True)
    text = models.TextField()
    test = models.ForeignKey(Test, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.text

class Answer(models.Model):
    id = models.UUIDField(default=uuid4, unique=True, editable=False, primary_key=True)
    text = models.TextField()
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.text} --> {self.is_correct}"

class UserTest(models.Model):
    id = models.UUIDField(default=uuid4, unique=True, editable=False, primary_key=True)
    test = models.ForeignKey(Test, on_delete=models.SET_NULL, null=True)
    candidate = models.ForeignKey(Candidate, on_delete=models.SET_NULL, null=True)
    num_of_questions = models.PositiveSmallIntegerField()
    correct_answers = models.PositiveSmallIntegerField()
    point = models.FloatField()
    taken_at = models.DateTimeField(auto_now_add=True)

class Result(models.Model):
    id = models.UUIDField(default=uuid4, unique=True, editable=False, primary_key=True)
    user_tests = models.ManyToManyField(UserTest)
    overall = models.FloatField()


