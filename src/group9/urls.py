from django.urls import path
from . import views

app_name = 'group9'
urlpatterns = [
  path('', views.home, name='group9'),
  path('questions/', views.show_questions, name='show_questions')
] 