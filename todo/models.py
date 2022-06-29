from datetime import datetime

from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Todo(models.Model):
    class Priorities(models.TextChoices):
        HIGH = "HIGH", "HIGH"
        MEDIUM = "MEDIUM", "MEDIUM"
        LOW = "LOW", "LOW"

    user = models.ForeignKey( User, on_delete=models.CASCADE, null=True ,blank=True, related_name="todos")
    name = models.CharField(max_length=200)
    stage = models.IntegerField(default=1)
    priority = models.CharField(
        max_length=20, choices=Priorities.choices, default=Priorities.LOW
    )
    deadline = models.DateField(default=datetime.now)

    def __str__(self) -> str:
        return f"{self.name } | {self.stage}"
