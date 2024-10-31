from django.db import models
from django.contrib.auth.models import AbstractUser

class Candidate(AbstractUser):
    phone = models.CharField(max_length=30)
    age = models.PositiveSmallIntegerField()
    balance = models.PositiveSmallIntegerField(default=0)
    active = models.BooleanField(default=True)
    region = models.CharField(max_length=30)
    email = None

    def __str__(self):
        return f"{self.username}: {self.first_name} {self.last_name}"

class Subject(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=150)

    def __str__(self):
        return self.name

class Test(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    author = models.CharField(max_length=50, blank=True, null=True)

class Question(models.Model):
    text = models.TextField()
    test = models.ForeignKey(Test, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.text

class Answer(models.Model):
    text = models.TextField()
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.text} --> {self.is_correct}"

class UserTest(models.Model):
    test = models.ForeignKey(Test, on_delete=models.SET_NULL, null=True)
    candidate = models.ForeignKey(Candidate, on_delete=models.SET_NULL, null=True)
    num_of_questions = models.PositiveSmallIntegerField()
    correct_answers = models.PositiveSmallIntegerField()
    point = models.FloatField()
    is_certified = models.BooleanField(default=False)
    taken_at = models.DateTimeField(auto_now_add=True)

class Result(models.Model):
    user_tests = models.ManyToManyField(UserTest)
    overall = models.FloatField()


