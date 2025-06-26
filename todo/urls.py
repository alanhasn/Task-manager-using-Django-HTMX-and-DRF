from django.urls import path

from .views import check, delete_task, index, search

app_name = "todos"

urlpatterns = [
    path("",index , name="home"),
    path("check/<int:pk>", check, name='check'),
    path("delete/<int:pk>", delete_task, name='delete_task'),
    path("search" , search , name="search")
]