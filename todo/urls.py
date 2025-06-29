from django.urls import path

from .views import *

app_name = "todos"

urlpatterns = [
    path("",list_tasks , name="home"),
    path('about-me/', about_me, name='about-me'),
    path('create-task/',create_task, name='create-todo'),
    path('edit-task/<int:pk>', edit_task, name='edit-todo'),
    path("check/<int:pk>", check, name='check'),
    path("delete/<int:pk>", delete_task, name='delete_task'),
    path("search" , search , name="search"),
]