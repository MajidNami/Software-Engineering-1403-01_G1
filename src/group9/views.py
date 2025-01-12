from django.shortcuts import render, redirect, HttpResponse
from registration import views
from registration.database import query as regq
from django.utils import timezone
from database import query
from database.secret import (DB_NAME, DB_USER,
                     DB_PASSWORD,
                     DB_HOST,
                     DB_PORT)
from .models import Question, Exam, Resource, Exercise, Report
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate,login,logout


# Create your views here.

#connectiong to the cloud database
db = query.create_db_connection(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)

#creating question tabel
create_question_query = """
CREATE TABLE IF NOT EXISTS `group9_question` (
    `ID` INT NOT NULL AUTO_INCREMENT,
    `body` LONGTEXT NOT NULL,
    `answer` LONGTEXT NOT NULL,
    PRIMARY KEY (`id`)
);
"""
query.create_table(db, create_question_query)

#creating exam table
create_exam_query = """
CREATE TABLE IF NOT EXISTS `group9_exam` (
    `ID` INT NOT NULL AUTO_INCREMENT,
    `user_id` INT NOT NULL,
    `questions` JSON NOT NULL,
    `answers` JSON,
    `score` DECIMAL(5, 2) NOT NULL DEFAULT 0.00,
    `date_taken` DATETIME(6) NOT NULL,
    PRIMARY KEY (`ID`),
    CONSTRAINT `group9_exam_user_id_fk`
        FOREIGN KEY (`user_id`)
        REFERENCES `auth_user` (`id`)
        ON DELETE CASCADE
);
"""
query.create_table(db, create_exam_query)

#creating resource table
create_resource_query = """
CREATE TABLE IF NOT EXISTS `group9_resource` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(255) NOT NULL,
  `author` VARCHAR(255) NOT NULL,
  `category` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`id`)
);
"""
query.create_table(db, create_resource_query)

#creating exercise table 
create_exercise_query = """
CREATE TABLE IF NOT EXISTS `group9_exercise` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `questions` JSON NOT NULL,
  `answers` JSON ,
  `score` DECIMAL(5, 2) NOT NULL DEFAULT 0.00,
  `date_completed` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`),
  CONSTRAINT `exercise_user_fk`
    FOREIGN KEY (`user_id`)
    REFERENCES `auth_user` (`id`)
    ON DELETE CASCADE
);
"""
query.create_table(db, create_exercise_query)

def sign_up_user(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        name = request.POST.get('name')  # استخراج نام
        age = request.POST.get('age')    # استخراج سن

        if pass1 != pass2:
            return HttpResponse("Your password and confirm password are not the same!")
        else:
            # بررسی نام کاربری برای جلوگیری از تکرار
            if User.objects.filter(username=uname).exists():
                return HttpResponse("This username is already taken. Please choose another one.")
            try:
                my_user = User.objects.create_user(uname, email, pass1)
                # اینجا می‌توانید اطلاعات اضافی مانند 'name' و 'age' را در پروفایل کاربر ذخیره کنید
                print('User created:', my_user)
                print('Name:', name)  # چاپ نام
                print('Age:', age)    # چاپ سن
                my_user.save()
                mydb = regq.create_db_connection(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)
                regq.save_user(mydb, name, uname, pass1, email, age)
                return redirect('group9:login')
            except IntegrityError:
                return HttpResponse("An error occurred while creating your account. Please try again.")
    return render(request, 'signup.html')

  
def login_user(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        request.session['cur_uname'] = username
        print(user)
        print(username)
        print(pass1)
        if user is not None:
            login(request,user)
            return redirect('group9:main')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")

    return render (request,'login.html')


def start_exam(request):

    # getting user id from user
    pass


def mainpage(request):
    return render (request , 'mainpage.html')


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
    return render(request, 'questions.html', {"questions": sample_questions})



