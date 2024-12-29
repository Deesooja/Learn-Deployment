from django.urls import path
from Myapp.views import GetTodoList, CreateTodo, GetUserReport

urlpatterns = [
    path("get-list", GetTodoList.as_view()),
    path("<int:user_id>/create-todo", CreateTodo.as_view()),
    path("<int:user_id>/user-report", GetUserReport.as_view()),
]
