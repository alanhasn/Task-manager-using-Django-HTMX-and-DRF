from django.urls import path

from .views import check, delete_task, index, search , create_task

app_name = "todos"

urlpatterns = [
    path("",index , name="home"),
    path('create-task/',create_task, name='create-todo'),
    path("check/<int:pk>", check, name='check'),
    path("delete/<int:pk>", delete_task, name='delete_task'),
    path("search" , search , name="search")
]