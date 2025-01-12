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
    return views.SignupPage(request)
    
def start_exam(request):

    # getting user id from user
    pass





def home(request):
    views.SignupPage(request)
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



