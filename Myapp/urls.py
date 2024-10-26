from django.urls import path
from Myapp.views import GetTodoList, CreateTodo

urlpatterns = [
    path("get-list", GetTodoList.as_view()),
    path("<int:user_id>/create-todo", CreateTodo.as_view()),
]
