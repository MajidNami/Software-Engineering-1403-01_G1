from django.urls import path
from . import views

app_name = 'group4'
urlpatterns = [
  path('', views.home, name='group4'),
  path('login/', views.g4login, name= "g4login"),
  path('signup/', views.g4signup, name="g4signup"),
  path('dashboard/', views.g4dashboard, name="g4dashboard"),
  path('teacherDashboard/', views.g4teacherDashboard, name="g4teacherDashboard"),
  path('logout/', views.g4logout, name="g4logout"),
  path('createReading/', views.g4createReading, name="g4createReading"),
  path('changeStudentLevel/', views.g4changeStudentLevel, name="g4changeStudentLevel"),
  path('uploadContent/', views.g4uploadContent, name="g4uploadContent"),
  path('selectTests/', views.g4selectTests, name= "g4selectTests"),
  path('examReading/<int:readingId>', views.g4examReading, name= "g4examReading"),
  path('practiceReading/<int:readingId>', views.g4practiceReading, name="g4practiceReading"),
  path('tips/', views.g4tips, name="g4tips"),
  path('tip/<int:id>/', views.g4tip, name="g4tip"),
  path('saveScores/', views.g4saveResult, name="g4saveResult"),
  path('seeScores/', views.g4seeResult, name="g4seeResult"),
  path('seeReports/', views.g4seeReports, name="g4seeReports"),
  path('redirectToDashboard/', views.g4redirectToDashboard, name="g4redirectToDashboard"),
  path('redirectToTeacherDashboard/', views.g4redirectToTeacherDashboard, name="g4redirectToTeacherDashboard"),
  
] 