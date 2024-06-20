from django.urls import path
from . import views

app_name = 'soac_base'

urlpatterns = [
    path('', views.home, name="home"),

    #CRUD Function
    path('questions/', views.QuestionListView.as_view(), name="question-lists"),
    path('question/new/', views.QuestionCreateView.as_view(), name="question-create"),
    path('questions/<int:pk>/', views.QuestionDetailView.as_view(), name="question-detail"),
    path('questions/<int:pk>/update/', views.QuestionUpdateView.as_view(), name='question-update'),
    path('question/<int:pk>/delete/', views.QuestionDeleteView.as_view(), name='question-delete'),
]
