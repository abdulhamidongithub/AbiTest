from django.db import models
from django.contrib.auth.models import AbstractUser

class Candidate(AbstractUser):
    phone = models.CharField(max_length=30)
    age = models.PositiveSmallIntegerField()
    region = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.username}: {self.first_name} {self.last_name}"
