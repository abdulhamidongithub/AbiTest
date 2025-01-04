from django.db import models
from django.contrib.auth.models import AbstractUser

class Candidate(AbstractUser):
    phone = models.CharField(max_length=30)
    birth_date = models.DateField(blank=True, null=True)
    balance = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)
    region = models.CharField(max_length=30)
    email = None

    def __str__(self):
        return f"{self.username}: {self.first_name} {self.last_name}"

class Subject(models.Model):
    name = models.CharField(max_length=30)
    is_mandatory = models.BooleanField(default=False)
    description = models.CharField(max_length=150)

    def __str__(self):
        return self.name

class Major(models.Model):
    name = models.CharField(max_length=150)
    subjects = models.ManyToManyField(Subject)
    language = models.CharField(max_length=30, default="o'zbek")

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=50)
    degree = models.CharField(max_length=30, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    photo = models.FileField(null=True, blank=True)

    def __str__(self):
        return self.name

class Test(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)

class Question(models.Model):
    text = models.TextField()
    test = models.ForeignKey(Test, on_delete=models.SET_NULL, null=True)
    correct_one = models.TextField()
    option1 = models.TextField()
    option2 = models.TextField()
    option3 = models.TextField()

    def __str__(self):
        return self.text


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

