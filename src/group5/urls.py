from django.urls import path
from . import views

app_name = 'group5'
urlpatterns = [
  path('', views.home, name='group5'),
  path('dictionary/<str:word>', views.dictionary, name='dictionary')
]