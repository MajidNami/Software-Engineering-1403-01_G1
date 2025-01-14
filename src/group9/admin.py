from django.contrib import admin
from .models import Question, Exam, Report, Resource, Exercise

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'body', 'answer')
    search_fields = ('id','body', 'answer')


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'score', 'date_taken')
    list_filter = ('user', 'date_taken')
    search_fields = ('user__username',)


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    search_fields = ('user__username',)


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'category')
    search_fields = ('title', 'author', 'category')


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'score', 'date_completed')
    list_filter = ('user', 'date_completed')
    search_fields = ('user__username',)

