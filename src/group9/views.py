from django.shortcuts import render
from .models import Question, Exam, Report, Resource, Exercise

# Create your views here.

def home(request):
    return render (request , 'group9.html' , {'group_number': '9'})

def show_questions(request):
    """
    ساخت چند سوال به صورت نمونه و نمایش آن‌ها در قالب
    """
    sample_questions = [
        Question(id=1, body="Describe your last vacation.", answer="My last vacation was..."),
        Question(id=2, body="Explain the importance of exercise.", answer="Exercising is important because..."),
        Question(id=3, body="What is your opinion on remote work?", answer="I think remote work is..."),
    ]
    return render(request, 'group9/questions.html', {"questions": sample_questions})

