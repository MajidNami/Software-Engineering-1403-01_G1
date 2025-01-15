from django.shortcuts import render, redirect, HttpResponse
from registration import views
from registration.database import query as regq
from django.utils import timezone
from database import query
from database.secret import (DB_NAME, DB_USER,
                     DB_PASSWORD,
                     DB_HOST,
                     DB_PORT)
from .models import Question, Exam, Resource, Exercise
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate,login,logout
import json
import datetime
from django.contrib.auth.decorators import login_required


# Create your views here.

#connectiong to the cloud database
db = query.create_db_connection(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)
cursor = db.cursor()

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
    `user_id` VARCHAR(50) NOT NULL,
    `questions` JSON NOT NULL,
    `answers` JSON,
    `score` DECIMAL(5, 2) NOT NULL DEFAULT 0.00,
    `date_taken` DATETIME(6) NOT NULL,
    PRIMARY KEY (`ID`),
    CONSTRAINT `group9_exam_user_id_fk`
        FOREIGN KEY (`user_id`)
        REFERENCES `users` (`username`)
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
  `user_id` VARCHAR(50) NOT NULL,
  `questions` JSON NOT NULL,
  `answers` JSON ,
  `score` DECIMAL(5, 2) NOT NULL DEFAULT 0.00,
  `date_completed` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`ID`),
  CONSTRAINT `group9_exercise_user_id_fk`
  FOREIGN KEY (`user_id`)
  REFERENCES `users` (`username`)
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

  
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'login.html', {
                'show_popup': True
            })
        else:
            return render(request, 'login.html', {
                'error_message': 'Invalid username or password. Please try again.'
            })

    return render(request, 'login.html')





from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Question

@login_required
def start_exam(request):
    if request.method != 'POST':
        # 1) Fetch 3 random questions
        select_random = """
            SELECT *
            FROM group9_question
            ORDER BY RAND()
            LIMIT 3;
        """
        cursor.execute(select_random)
        random_questions = cursor.fetchall()
        
        # Store them in session
        request.session['random_questions'] = random_questions
        
        # Render template
        return render(request, 'start_exam.html', {
            'questions': random_questions
        })

    else:
        # POST case: handle form submission
        random_questions = request.session.get('random_questions', [])
        
        # Retrieve question IDs
        question_ids = request.POST.getlist('question_ids')
        
        # Collect user answers
        user_answers = {}
        for q_id in question_ids:
            field_name = f'answer_{q_id}'
            user_answers[q_id] = request.POST.get(field_name, '')
        
        # Calculate the number of correct answers
        total_correct = 0
        result_data = []
        
        for q in random_questions:
            q_id_str = str(q[0])         # question ID
            q_body = q[1]               # question text
            q_correct_answer = q[2]     # correct answer

            user_answer = user_answers.get(q_id_str, '')
            if user_answer.strip().lower() == q_correct_answer.strip().lower():
                total_correct += 1
            
            result_data.append({
                'question_body': q_body,
                'user_answer': user_answer,
                'correct_answer': q_correct_answer
            })
        
        # Convert raw score to out of 20
        raw_score = (total_correct / 3) * 20
        final_score = round(raw_score, 2)
        
        # Convert to JSON
        questions_json = json.dumps(question_ids)
        answers_json = json.dumps(user_answers)
        
        # **Use request.user.username here** to avoid NULL
        user_id = request.user.username
        
        insert_sql = """
            INSERT INTO `group9_exam` (user_id, questions, answers, score, date_taken)
            VALUES (%s, %s, %s, %s, %s)
        """
        params = [
            user_id,             # <-- Ensures 'user_id' is not NULL
            questions_json,
            answers_json,
            final_score,
            datetime.datetime.now()
        ]
        cursor.execute(insert_sql, params)
        db.commit()
        
        # Render the result page
        return render(request, 'exam_result.html', {
            'final_score': final_score,
            'total_correct': total_correct,
            'result_data': result_data,
        })
@login_required
def start_exercise(request):
    if request.method != 'POST':
        # 1) Fetch 3 random questions
        select_random = """
            SELECT *
            FROM group9_question
            ORDER BY RAND()
            LIMIT 3;
        """
        cursor.execute(select_random)
        random_questions = cursor.fetchall()  # e.g. [(1, 'question text', 'a'), (2, 'something else', 'b'), ...]

        # 2) Store them in session
        request.session['exercise_questions'] = random_questions

        # 3) Render the "start_exercise.html"
        return render(request, 'start_exercise.html', {
            'questions': random_questions
        })

    else:
        # If request is POST, the user has submitted the exercise
        random_questions = request.session.get('exercise_questions', [])

        # 1) Retrieve question IDs
        question_ids = request.POST.getlist('question_ids')  # e.g. ['1','2','3']

        # 2) Collect user answers
        user_answers = {}
        for q_id in question_ids:
            field_name = f'answer_{q_id}'
            user_answers[q_id] = request.POST.get(field_name, '')

        # 3) Calculate score
        total_correct = 0
        result_data = []

        for q in random_questions:
            q_id_str = str(q[0])
            q_text = q[1]
            q_correct_answer = q[2]

            user_answer = user_answers.get(q_id_str, '')
            if user_answer.strip().lower() == q_correct_answer.strip().lower():
                total_correct += 1

            # Collect data for displaying in results
            result_data.append({
                'question_body': q_text,
                'user_answer': user_answer,
                'correct_answer': q_correct_answer
            })

        # 4) Convert raw score (out of 3) to a score out of 20
        raw_score = (total_correct / 3) * 20
        final_score = round(raw_score, 2)

        # 5) Insert into DB using the logged-in user's username
        insert_sql = """
            INSERT INTO `group9_exercise` (user_id, questions, answers, score, date_completed)
            VALUES (%s, %s, %s, %s, %s)
        """
        questions_json = json.dumps(question_ids)
        answers_json = json.dumps(user_answers)
        
        params = [
            request.user.username,  # <-- Use request.user.username here
            questions_json,
            answers_json,
            final_score,
            datetime.datetime.now()
        ]
        cursor.execute(insert_sql, params)
        db.commit()

        # 6) Render "exercise_result.html"
        return render(request, 'exercise_result.html', {
            'final_score': final_score,
            'total_correct': total_correct,
            'result_data': result_data,  # Contains question body, user & correct answers
        })  


@login_required
def report_exam(request):
    """
    Shows the user:
      - Their average exam and exercise scores
      - Feedback on both
      - A summary table of all their exams
      - A summary table of all their exercises
    """

    user_id = request.user.username  # guaranteed by @login_required

    # -------------------------------------------------
    #  A) Fetch exam records for this user
    # -------------------------------------------------
    select_exams_sql = """
        SELECT ID, questions, answers, score, date_taken
        FROM group9_exam
        WHERE user_id = %s
    """
    cursor.execute(select_exams_sql, [user_id])
    exam_rows = cursor.fetchall()  
    # example: [(1, '[1,2,3]', '{"1":"A","2":"B"}', 18.0, datetime.datetime(2025,1,15, ...)), ...]

    exam_scores_list = []
    exam_data = []  # for display in "Exam Details" table

    for row in exam_rows:
        exam_id = row[0]
        # row[1] = questions JSON
        # row[2] = answers JSON
        score = float(row[3])
        date_taken = row[4]

        # 1) Collect scores for average
        exam_scores_list.append(score)

        # 2) Collect minimal data needed for the table
        exam_data.append({
            'id': exam_id,
            'score': score,
            'date_taken': date_taken,
        })

    # -------------------------------------------------
    #  B) Fetch exercise records for this user
    # -------------------------------------------------
    select_exercises_sql = """
        SELECT ID, questions, answers, score, date_completed
        FROM group9_exercise
        WHERE user_id = %s
    """
    cursor.execute(select_exercises_sql, [user_id])
    exercise_rows = cursor.fetchall()
    # e.g. [(1, '[4,5,6]', '{"4":"Answer4"}', 16.0, datetime.datetime(2025,1,15,...)), ...]

    exercise_scores_list = []
    exercise_data = []  # for display in "Exercise Details" table

    for row in exercise_rows:
        exercise_id = row[0]
        score = float(row[3])
        date_completed = row[4]

        # 1) Collect scores for average
        exercise_scores_list.append(score)

        # 2) Collect minimal data for the table
        exercise_data.append({
            'id': exercise_id,
            'score': score,
            'date_completed': date_completed,
        })

    # -------------------------------------------------
    #  C) Calculate averages & feedback
    # -------------------------------------------------
    if exam_scores_list:
        avg_exam_score = sum(exam_scores_list) / len(exam_scores_list)
    else:
        avg_exam_score = 0.0

    if exercise_scores_list:
        avg_exercise_score = sum(exercise_scores_list) / len(exercise_scores_list)
    else:
        avg_exercise_score = 0.0

    def get_feedback(average):
        if average >= 17:
            return "You've done a great job!"
        elif average >= 14:
            return "You are getting closer to a good result. Keep going!"
        elif average >= 10:
            return "You can still get better. Keep practicing!"
        else:
            return "Don't give up. You need more practice!"

    exam_feedback = get_feedback(avg_exam_score)
    exercise_feedback = get_feedback(avg_exercise_score)

    # -------------------------------------------------
    #  D) Pass data to the template
    # -------------------------------------------------
    return render(request, 'report.html', {
        # These four for the summary up top
        'avg_exam_score': round(avg_exam_score, 2),
        'avg_exercise_score': round(avg_exercise_score, 2),
        'exam_feedback': exam_feedback,
        'exercise_feedback': exercise_feedback,

        # For the tables
        'exam_data': exam_data,
        'exercise_data': exercise_data,
    })
    
def resources(request):
    if request.method != 'POST':
        # Fetch all resources from the database
        select_resources = """
            SELECT *
            FROM group9_resource;
        """
        cursor.execute(select_resources)
        resources_list = cursor.fetchall()  # e.g. [(1, 'Resource Name', 'Description', 'Link'), ...]

        # Pass resources to the template
        return render(request, 'resources.html', {
            'resources': resources_list
        })

    else:  # If back button is pressed, redirect to main page
        return redirect('group9:main')
    


def logout(request):
    return redirect('group9:group9')

    

def mainpage(request):
    return render (request , 'mainpage.html')


def home(request):
    return render (request , 'group9.html' , {'group_number': '9'})


def show_questions(request):
    sample_questions = [
        Question(id=1, body="Describe your last vacation.", answer="My last vacation was..."),
        Question(id=2, body="Explain the importance of exercise.", answer="Exercising is important because..."),
        Question(id=3, body="What is your opinion on remote work?", answer="I think remote work is..."),
    ]
    return render(request, 'questions.html', {"questions": sample_questions})



