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
  path('uploadContent/', views.g4uploadContent, name="g4uploadContent")
] 