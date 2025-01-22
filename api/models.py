from django.db import models
from django.contrib.auth.models import AbstractUser

class Candidate(AbstractUser):
    phone = models.CharField(max_length=30)
    birth_date = models.DateField(blank=True, null=True)
    balance = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)
    region = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.username}: {self.first_name} {self.last_name}"

class Subject(models.Model):
    name = models.CharField(max_length=30)
    is_mandatory = models.BooleanField(default=False)
    description = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name", "id"]

class Major(models.Model):
    name = models.CharField(max_length=150)
    main = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, related_name="main_majors")
    secondary = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    language = models.CharField(max_length=30, default="o'zbek")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name", "id"]


class Author(models.Model):
    name = models.CharField(max_length=50)
    degree = models.CharField(max_length=30, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    photo = models.FileField(null=True, blank=True)
    more_info = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Test(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    source = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.subject.name} - {self.author.name}"

class Question(models.Model):
    text = models.TextField()
    test = models.ForeignKey(Test, on_delete=models.CASCADE, null=True, related_name="questions")
    correct_option = models.TextField()
    options = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.text

STATUS = [
    ("in_progress", "in_progress"),
    ("finished", "finished"),
]

class UserTest(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name="tests", null=True)
    major = models.ForeignKey(Major, on_delete=models.SET_NULL, null=True)
    main_test = models.ForeignKey(Test, on_delete=models.SET_NULL, null=True, related_name="main_user_tests")
    secondary_test = models.ForeignKey(Test, on_delete=models.SET_NULL, null=True, related_name="secondary_user_tests")
    mandatory_tests = models.ManyToManyField(Test, related_name="mandatory_user_tests")

    main_test_points = models.FloatField(default=0.0)
    secondary_test_points = models.FloatField(default=0.0)
    mandatory_points = models.JSONField(default={"matem": 0.0, "tarix": 0.0, "ingliz_tili": 0.0})

    status = models.CharField(max_length=30, choices=STATUS, default="in_progress")
    total_points = models.FloatField(default=0.0)
    taken_at = models.DateTimeField(auto_now_add=True)

    def calculate_total_points(self):
        """Calculate total points from main, secondary, and mandatory tests."""
        mandatory_total = sum(self.mandatory_points.values())
        self.total_points = self.main_test_points + self.secondary_test_points + mandatory_total
        self.save()

    def __str__(self):
        return f"UserTest: {self.candidate.username} - {self.major.name} ({self.total_points} points)"


class UserAnswer(models.Model):
    user_test = models.ForeignKey(UserTest, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name="answers")
    answer = models.TextField(blank=True, null=True)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"Answer by {self.user_test.candidate.username} for {self.question.text}"


