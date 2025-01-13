from django.shortcuts import render, redirect
from django.urls import reverse
from urllib.parse import urlencode
from . import views
from .database import query, secret
# Create your views here.

user2 = ""

def home(request):
    return render (request , 'landingPage.html')

def g4login(request):
    if request.method == "GET":
        return render(request, "g4login.html")
    elif request.method == "POST":
        try:
            mydb= query.create_db_connection(secret.DB_HOST, secret.DB_PORT, secret.DB_USER, secret.DB_PASSWORD, secret.DB_NAME)
            username= request.POST.get("username")
            password= request.POST.get("password")
            res= query.g4fetchall(mydb, "g4users")
            print(username, password)
            flag = 0
            for user in res:
                if user[5] == username and user[6] == password:
                    print("success login")
                    flag =1
                    if user[7]:
                        print("user")
                        url = reverse("group4:g4dashboard")
                        global user2
                        user2 = user[2]
                        query_params = urlencode({"name": user[2]})
                        return redirect(f"{url}?{query_params}")
                    else:
                        print("teacher")
                        url = reverse("group4:g4teacherDashboard")
                        user2 = user[2]
                        query_params = urlencode({"name": user[2]})
                        return redirect(f"{url}?{query_params}")
            if flag == 0:
                return render(request, "g4err.html")
        except Exception as e:
            print("KOMAK!", e)
            return render(request, "g4err.html")
            
    
def g4signup(request):
    if request.method == "GET":
        return render(request, "g4signup.html")
    elif request.method == "POST": 
        mydb= query.create_db_connection(secret.DB_HOST, secret.DB_PORT, secret.DB_USER, secret.DB_PASSWORD, secret.DB_NAME)
        name= request.POST.get("name")
        email= request.POST.get("email")
        dateOfBirth= request.POST.get("dob")
        username= request.POST.get("username")
        password= request.POST.get("password")
        usertype= request.POST.get("type")
        if usertype == "Student":
            lvl = request.POST.get("level")
            usertype = True
            query.g4saveUser(mydb, name, email, dateOfBirth, username, password, usertype, lvl)
        else:
            usertype = False
            query.g4saveUser(mydb, name, email, dateOfBirth, username, password, usertype, None)
            
        mydb.close()
        #TODO render dashboard
        return render(request, "g4signup.html")
        
        
def g4dashboard(request):
    if request.method == "GET":
        return render(request=request, template_name="g4dashboard.html", context={"username": request.GET.get("name")})         


def g4teacherDashboard(request):
    if request.method == "GET":
        return render(request=request, template_name="g4teacherDashboard.html", context={"username": request.GET.get("name")})  
    
def g4logout(request):
    if request.method == "GET":
        return redirect("group4:group4")
    
def g4createReading(request):
    if request.method == "GET":
        return render(request, "g4createReading.html")
    elif request.method == "POST":
        title = request.POST.get("test-title")
        context = request.POST.get("main-text")
        # Question 1
        q1 = request.POST.get("question-1", "")
        q1_answers = [
            request.POST.get("question-1-answer-1", ""),
            request.POST.get("question-1-answer-2", ""),
            request.POST.get("question-1-answer-3", ""),
            request.POST.get("question-1-answer-4", ""),
        ]
        q1_correct_index = int(request.POST.get("question-1-correct", 0))  # Correct answer index (1-based)
        q1_correct_answer = q1_answers[q1_correct_index - 1] if q1_correct_index else None
        q1_wrong_answers = [ans for i, ans in enumerate(q1_answers) if i != q1_correct_index - 1]

        q1_wrong1, q1_wrong2, q1_wrong3 = q1_wrong_answers

        # Question 2
        q2 = request.POST.get("question-2", "")
        q2_answers = [
            request.POST.get("question-2-answer-1", ""),
            request.POST.get("question-2-answer-2", ""),
            request.POST.get("question-2-answer-3", ""),
            request.POST.get("question-2-answer-4", ""),
        ]
        q2_correct_index = int(request.POST.get("question-2-correct", 0))  # Correct answer index (1-based)
        q2_correct_answer = q2_answers[q2_correct_index - 1] if q2_correct_index else None
        q2_wrong_answers = [ans for i, ans in enumerate(q2_answers) if i != q2_correct_index - 1]

        q2_wrong1, q2_wrong2, q2_wrong3 = q2_wrong_answers

        # Question 3
        q3 = request.POST.get("question-3", "")
        q3_answers = [
            request.POST.get("question-3-answer-1", ""),
            request.POST.get("question-3-answer-2", ""),
            request.POST.get("question-3-answer-3", ""),
            request.POST.get("question-3-answer-4", ""),
        ]
        q3_correct_index = int(request.POST.get("question-3-correct", 0))  # Correct answer index (1-based)
        q3_correct_answer = q3_answers[q3_correct_index - 1] if q3_correct_index else None
        q3_wrong_answers = [ans for i, ans in enumerate(q3_answers) if i != q3_correct_index - 1]

        q3_wrong1, q3_wrong2, q3_wrong3 = q3_wrong_answers
        lvl = request.POST.get("reading-level")
        if lvl == "beginner":
            lvl = 1
        elif lvl == "intermediate":
            lvl = 2
        elif lvl == "advanced":
            lvl = 3
        
        mydb= query.create_db_connection(secret.DB_HOST, secret.DB_PORT, secret.DB_USER, secret.DB_PASSWORD, secret.DB_NAME)
        query.g4saveReading(mydb=mydb, context=context, title=title, q1body=q1, q1cans=q1_correct_answer, q1wans1=q1_wrong1, q1wans2=q1_wrong2, q1wans3=q1_wrong3, q2body=q2, q2cans=q2_correct_answer, q2wans1=q2_wrong1, q2wans2=q2_wrong2, q2wans3=q2_wrong3, q3body=q3, q3cans=q3_correct_answer, q3wans1=q3_wrong1, q3wans2=q3_wrong2, q3wans3=q3_wrong3, lvl=lvl)

        url = reverse("group4:g4teacherDashboard")                
        query_params = urlencode({"name": user2})
        return redirect(f"{url}?{query_params}")

def g4changeStudentLevel(request):
    if request.method == "GET":
        mydb= query.create_db_connection(secret.DB_HOST, secret.DB_PORT, secret.DB_USER, secret.DB_PASSWORD, secret.DB_NAME)
        res = query.g4fetchall(mydb=mydb, tableName="g4users")
        print(res)
        list_of_user = []
        users = {}
        for user in res:
            users["name"] = user[5]
            users["type"] = user[7]
            list_of_user.append(users)
            users = {}
        return render(request=request, template_name="g4changeStudentLevel.html", context={"users": list_of_user})
    elif request.method == "POST":
        new_lvl = request.POST.get("new-level")
        username = request.POST.get("student-name")
        if new_lvl == "beginner":
            new_lvl =1
        elif new_lvl == "intermediate":
            new_lvl = 2
        elif new_lvl == "advanced":
            new_lvl =3
        
        mydb= query.create_db_connection(secret.DB_HOST, secret.DB_PORT, secret.DB_USER, secret.DB_PASSWORD, secret.DB_NAME)
        res = query.g4fetchall(mydb,"g4users")
        userid = 0
        print(f"username: {username}")
        for user in res:
            if user[5] == username:
                userid = user[0]
                break
        print(f"uid: {userid}")
        query.g4updateUser(mydb=mydb, newAttribute="lvl", newValue=new_lvl, id=userid)
        url = reverse("group4:g4teacherDashboard")
        global user2
        query_params = urlencode({"name": user2})
        return redirect(f"{url}?{query_params}")
        
def g4uploadContent(request):
    if request.method == "GET":
        return render(request, "g4educationalContent.html")
    elif request.method == "POST":
        title = request.POST.get("title")
        file1 = request.FILES["file"].read()
        print(file1)
        description = request.POST.get("description")
        mydb= query.create_db_connection(secret.DB_HOST, secret.DB_PORT, secret.DB_USER, secret.DB_PASSWORD, secret.DB_NAME)
        global user2
        query.g4savetip(mydb=mydb, title=title, file1=file1, description=description, username=user2)
        url = reverse("group4:g4teacherDashboard")
        query_params = urlencode({"name": user2})
        return redirect(f"{url}?{query_params}")
