# group9/models.py
from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    body = models.TextField(verbose_name="Question Body")
    answer = models.TextField(verbose_name="Answer")

    def __str__(self):
        return f"Q{self.id}: {self.body[:50]}..."



class Exam(models.Model):
    # Store the user's ID as an integer (not tied to the Django User model)
    user = models.PositiveIntegerField(verbose_name="شناسه کاربر")

    # Store a list of question IDs (integers) as JSON
    questions = models.JSONField(default=list, verbose_name="شناسه سوالات")

    score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        verbose_name="نمره"
    )
    date_taken = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ آزمون"
    )

    def __str__(self):
        return f"Exam {self.id} (UserID: {self.user})"


class Report(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='report', verbose_name="کاربر")
    exams = models.ManyToManyField(Exam, related_name='reports', verbose_name="آزمون‌ها")

    def __str__(self):
        return f"گزارش {self.user.username}"


class Resource(models.Model):
    title = models.CharField(max_length=255, verbose_name="عنوان")
    author = models.CharField(max_length=255, verbose_name="نویسنده")
    category = models.CharField(max_length=100, verbose_name="دسته‌بندی")

    def __str__(self):
        return self.title


class Exercise(models.Model):
    # Store the user's ID as a plain integer
    user = models.PositiveIntegerField(verbose_name="شناسه کاربر")

    # Store an array of question IDs (integers) in a JSON field
    questions = models.JSONField(default=list, verbose_name="شناسه سوالات")

    score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        verbose_name="نمره"
    )
    date_completed = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ تکمیل"
    )

    def __str__(self):
        return f"تمرین {self.id} توسط کاربر {self.user}"
