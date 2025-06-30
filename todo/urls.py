from django.urls import path

from .views import *

app_name = "todos"

urlpatterns = [
    # URL patterns for the todo app
    path("",ListTaskView.as_view() , name="home"),
    path('create-task/',CreateTaskView.as_view(), name='create-todo'),
    path('edit-task/<int:pk>', EditTaskView.as_view(), name='edit-todo'),
    path("delete/<int:pk>", DeleteTaskView.as_view(), name='delete_task'),
    path("check/<int:pk>",UpdateTaskStatusView.as_view(), name='check'),
    path("search" , SearchTaskView.as_view() , name="search"),
    path('about-me/', AboutMePageView.as_view() , name='about-me'),
]