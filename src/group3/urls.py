from django.urls import path
from . import views
# from django.views.generic import TemplateView

app_name = 'group3'
urlpatterns = [
  path('', views.home, name='group3'),
  # path('review/', TemplateView.as_view(template_name="group3/base.html"), name="home"),
  path('wordManagement/', views.WordListView.as_view(), name='word-list'),
  path('learned/', views.learned, name='learned'),
  path('addWord/', views.WordCreateView.as_view(), name='word-create'),
  path('editWord/<int:pk>', views.WordUpdateView.as_view(), name='word-update'),
  path('box/<int:box_num>/', views.box_view, name='box'),
  path('chooseBox/', views.choose_box, name='choose-box'),
  path('startLearning/<int:box_num>/<int:start_index>/', views.start_learning, name='start-learning'),
  path('checkSpelling/<int:word_id>/<int:start_index>/', views.spelling_view, name='spelling'),
] 
