from django.shortcuts import render, redirect
from django.urls import reverse
from urllib.parse import urlencode
from . import views
from .database import query, secret
import base64
from datetime import date
# Create your views here.

user2 = ""
username2 = ""
readingId2 = ""

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
                        global user2, username2
                        user2 = user[2]
                        username2 = user[5]
                        print(user2)
                        query_params = urlencode({"name": user[2]})
                        print(f"{url}?{query_params}")
                        return redirect(f"{url}?{query_params}")
                    else:
                        print("teacher")
                        url = reverse("group4:g4teacherDashboard")
                        user2 = user[2]
                        username2 = user[5]
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
        return render(request, "g4dashboard.html")
        
        
def g4dashboard(request):
    if request.method == "GET":
        global user2
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
        if new_lvl == "Beginner":
            new_lvl =1
        elif new_lvl == "Intermediate":
            new_lvl = 2
        elif new_lvl == "Advanced":
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

def g4selectTests(request):
    if request.method == "GET":
        mydb= query.create_db_connection(secret.DB_HOST, secret.DB_PORT, secret.DB_USER, secret.DB_PASSWORD, secret.DB_NAME)
        res = query.g4fetchall(mydb=mydb, tableName="g4readings")
        lvl1= []
        lvl2= []
        lvl3= []
        tmp = {}
        for reading in res:
            if reading[18] ==1:
                tmp["title"] = reading[17]
                tmp["id"] = reading[0]
                lvl1.append(tmp)
                tmp = {}
            elif reading[18] == 2:
                tmp["title"] = reading[17]
                tmp["id"] = reading[0]
                lvl2.append(tmp)
                tmp = {}
                
            elif reading[18] == 3:
                tmp["title"] = reading[17]
                tmp["id"] = reading[0]
                lvl3.append(tmp)
                tmp = {}
                
            
        return render(request=request, template_name="g4selectTests.html", context={"lvl1": lvl1, "lvl2": lvl2, "lvl3": lvl3})
    
def g4examReading(request, readingId):
    if request.method == "GET":
        mydb= query.create_db_connection(secret.DB_HOST, secret.DB_PORT, secret.DB_USER, secret.DB_PASSWORD, secret.DB_NAME)
        res = query.g4fetchall(mydb=mydb, tableName="g4readings")
        for i in res:
            if i[0] == readingId:
                global readingId2
                readingId2 = i[0]
                return render(request=request, template_name="g4examReading.html", context={"title" : i[17], "content": i[1], "q1body": i[2], "q1cans": i[3], "q1wans1": i[4], "q1wans2": i[5], "q1wans3": i[6], "q2body": i[7], "q2cans": i[8], "q2wans1": i[9], "q2wans2": i[10], "q2wans3": i[11], "q3body": i[12], "q3cans": i[13], "q3wans1": i[14], "q3wans2": i[15], "q3wans3" : i[16]})


def g4practiceReading(request, readingId):
     if request.method == "GET":
        mydb= query.create_db_connection(secret.DB_HOST, secret.DB_PORT, secret.DB_USER, secret.DB_PASSWORD, secret.DB_NAME)
        res = query.g4fetchall(mydb=mydb, tableName="g4readings")
        for i in res:
            if i[0] == readingId:
                global readingId2
                readingId2 = i[0]
                return render(request=request, template_name="g4practiceReading.html", context={"title" : i[17], "content": i[1], "q1body": i[2], "q1cans": i[3], "q1wans1": i[4], "q1wans2": i[5], "q1wans3": i[6], "q2body": i[7], "q2cans": i[8], "q2wans1": i[9], "q2wans2": i[10], "q2wans3": i[11], "q3body": i[12], "q3cans": i[13], "q3wans1": i[14], "q3wans2": i[15], "q3wans3" : i[16]})

        
def g4tips(request):
    if request.method == "GET":
        mydb= query.create_db_connection(secret.DB_HOST, secret.DB_PORT, secret.DB_USER, secret.DB_PASSWORD, secret.DB_NAME)
        res = query.g4fetchall(mydb, "g4educationalContent")
        list_of_contents = []
        dict_content = {}
        for content in res:
            dict_content["id"] = content[0]
            dict_content["title"] = content[2]
            dict_content["description"] = content[4][:20] + "..."
            list_of_contents.append(dict_content)
            dict_content = {} 
        print(list_of_contents)
        return render(request=request, template_name="g4tips.html", context={'contents': list_of_contents})

def g4tip(request,id: int):
    if request.method == "GET":
        mydb= query.create_db_connection(secret.DB_HOST, secret.DB_PORT, secret.DB_USER, secret.DB_PASSWORD, secret.DB_NAME)
        res = query.g4fetchall(mydb, "g4educationalContent")
        dict_content = {}
        for content in res:
            if content[0] == id:
                dict_content["username"] = content[1] 
                dict_content["title"] = content[2]
                if content[3]:
                    binary_data = content[3]
                    base64_encoded_data = base64.b64encode(binary_data).decode('utf-8')
                    dict_content["file"] = base64_encoded_data
                else:
                    dict_content["file"] = None
                dict_content["description"] = content[4]
                break
        if dict_content["file"]:
            return render(request, 'g4tip.html', {'content': dict_content}) 
        return render(request, 'g4tipWithoutImage.html', {'content': dict_content})
    
def g4saveResult(request):
    if request.method == "POST":
        q1_answer = request.POST.get('q1')  
        q2_answer = request.POST.get('q2')  
        q3_answer = request.POST.get('q3')  
        
        correct_ans = {
            'q1': 'A',
            'q2': 'B',
            'q3': 'D',
        }
        
        user_answers = {
            'q1': q1_answer,
            'q2': q2_answer,
            'q3': q3_answer,
        }
        
        score = sum(1 for key, value in user_answers.items() if correct_ans[key] == value)
        score /= 3
        score *= 100
        
        mydb= query.create_db_connection(secret.DB_HOST, secret.DB_PORT, secret.DB_USER, secret.DB_PASSWORD, secret.DB_NAME)
        res = query.g4fetchall(mydb,"g4users")
        userid = 0
        global username2, readingId2
        print(f"username: {user2}")
        for user in res:
            if user[5] == username2:
                userid = user[0]
                break
        
        
        mydb= query.create_db_connection(secret.DB_HOST, secret.DB_PORT, secret.DB_USER, secret.DB_PASSWORD, secret.DB_NAME)
        query.g4saveResult(mydb, userid, readingId2, date.today(), score)
        url = reverse("group4:g4seeResult")
        query_params = urlencode({"name": user2})
        return redirect(f"{url}?{query_params}")
    
def g4seeResult(request):
    if request.method == "GET":
        mydb= query.create_db_connection(secret.DB_HOST, secret.DB_PORT, secret.DB_USER, secret.DB_PASSWORD, secret.DB_NAME)
        res = query.g4fetchall(mydb, "g4users")
        userid = 0
        sumScore = 0
        count= 0
        last_result = 0
        global username2
        for user in res:
            print(user[0])
            if user[5] == username2:
                userid = user[0]
                break
        res1 = query.g4joinReadinResult(mydb)
        related = []
        temp = {}
        for joind in res1:
            if joind[21] == userid:
                temp["title"] = joind[17]
                temp["date"] = joind[22]
                temp["score"] = joind[23]
                last_result = joind[23]
                sumScore += joind[23]
                count += 1
                related.append(temp)
                temp = {}
        
        try:
            avg = sumScore / count
        except:
            return render(request, "g4noExam.html")
        
        recommendedLevel = ""
        if avg >= 80:
            recommendedLevel = "Advanced"
        elif avg < 80 and avg > 40:
            recommendedLevel = "Intermediate"
        elif avg <= 40:
            recommendedLevel = "Beginner"
        return render(request, 'g4seeResult.html', {"last": last_result, "avg": avg, "related": related, "rl": recommendedLevel})

        
def g4seeReports(request):
    if request.method == "GET":
        mydb= query.create_db_connection(secret.DB_HOST, secret.DB_PORT, secret.DB_USER, secret.DB_PASSWORD, secret.DB_NAME)
        res = query.g4joinReadinResult(mydb)
        users = query.g4fetchall(mydb, "g4users")
        processedUsers = {}
        for user in users:
            processedUsers[user[0]] = user[5]

        
        data = []
        tmp = {}
        for result in res:
            tmp["username"] = processedUsers[result[21]]
            tmp["title"] = result[17]
            if result[18] == 1:
                tmp["lvl"] = "Beginner"
            elif result[18] == 2:
                tmp["lvl"] = "Intermediate"
            elif result[18] == 3:
                tmp["lvl"] = "Advanced"

            tmp["score"] = result[23]
            tmp["date"] = result[22]
            data.append(tmp)
            tmp = {}
        
        return render(request, "g4studentReports.html", context={"data" : data})
    
def g4redirectToDashboard(request):
    if request.method == "GET":
        global user2
        url = reverse("group4:g4dashboard")
        query_params = urlencode({"name": user2})
        return redirect(f"{url}?{query_params}")
    
def g4redirectToTeacherDashboard(request):
    if request.method == "GET":
        global user2
        url = reverse("group4:g4teacherDashboard")
        query_params = urlencode({"name": user2})
        return redirect(f"{url}?{query_params}")