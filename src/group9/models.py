# group9/models.py
from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    id = models.AutoField(primary_key=True)
    body = models.TextField()
    answer = models.TextField()
def __str__(self):
        return f"Question {self.id}: {self.body[:50]}..."




class Exam(models.Model):
    # Store the user's ID as an integer (not tied to the Django User model)
    id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=50)
    questions = models.JSONField()
    answers = models.JSONField(null=True, blank=True)
    score = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    date_taken = models.DateTimeField()
    def __str__(self):
        return f"Exam {self.id} by user {self.user_id}"
    

class Resource(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    category = models.CharField(max_length=100)

    def __str__(self):
        return f"Resource {self.id}: {self.title}"


class Exercise(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=50)
    questions = models.JSONField()
    answers = models.JSONField(null=True, blank=True)
    score = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    date_completed = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ تکمیل"
    )

    def __str__(self):
        return f"Exercise {self.id} by user {self.user_id}"
