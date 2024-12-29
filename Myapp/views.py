from Myapp.Services.utilities import Logger
from rest_framework.views import APIView
from Myapp.models import *
from django.db.models import Q
from Myapp.Services.response import uls_response
from Myapp.serializers import TodoSerializer
from rest_framework.exceptions import ValidationError
from datetime import datetime, timedelta

logger = Logger('Views')

class GetTodoList(APIView):
    """ 
    TAKE QUERY PARAMITERS :
        (1) USER ID 
        (2) STATUS :  ["PENDING", "COMPLETED", "DELEAYED"]
        
    RETUEN VALUE :
        LIST OF TODO_LIST SERIALISED DATA
        
    """
    def get(self, request):
        try:
            user_id = request.query_params.get("user")
            status = request.query_params.get("status")
            page = request.query_params.get("page", 1)
            page_size = request.query_params.get("page_size", 50)
            from_page = 0
            to_page = 50
            if page and page_size:
                try:
                    page = int(page)
                    page_size =  int(page_size)
                    
                    if page < 1 or page_size < 1:
                        raise ValidationError("page and page_size must be grater then 1")
                        
                    from_page = page_size * (page-1)
                    to_page = page_size * page
                except ValueError:
                    raise ValidationError("parameter page and page-sze must be numer")
            
            my_filter = Q()
            if user_id:
                my_filter &= Q(user=user_id)
                
            if status in ["PENDING", "COMPLETED", "DELEAYED"]:
                my_filter &= Q(status=status)
            
            filterd_todo_qs = Todo.objects.filter(my_filter)[from_page: to_page]
            serialized_data = TodoSerializer(filterd_todo_qs, many=True).data
            return uls_response(status_code=200, message="OK", data=serialized_data)
        # except ValueError as ex:
        #     logger.error(ex)
        #     return uls_response(status_code=500, message=str(ex), data=[])
        
        except Exception as ex:
            logger.error(ex)
            return uls_response(status_code=500, message=str(ex), data=[])


class CreateTodo(APIView):
    def post(self, request, user_id):
        try:
            """GET DATA FRO BODY"""
            title = request.data.get("title")
            descriptions = request.data.get("descriptions")
            estimated_completion_time = int(request.data.get("estimated_completion_time"))
            estimated_completion_time = datetime.now() + timedelta(minutes=estimated_completion_time)
            
            """VALIDATIONS"""
            if not user_id:
                raise ValidationError("User id is required")
            
            if not User.objects.filter(id=user_id):
                raise ValidationError("Given User id Does not Exits")
            
            if not title:
                raise ValidationError("title is required")
            
            if not descriptions:
                raise ValidationError("descriptions is required")
            
            if not estimated_completion_time:
                raise ValidationError("estimated_completion_time is required")
            
            """CREATION NEW TODOS"""
            user_obj = User.objects.filter(id=user_id).first()
            todo_obj = Todo()
            todo_obj.user = user_obj
            todo_obj.title = title
            todo_obj.descriptions = descriptions
            todo_obj.estimated_completion_time = estimated_completion_time
            todo_obj.save()
            
            """GET ALL TODOS"""
            todo_qs = Todo.objects.filter(user=user_id)
            return uls_response(status_code=201, message="CREATEDE", data=TodoSerializer(todo_qs, many=True).data)
            
        except Exception as ex:
            logger.error(ex)
            return uls_response(status_code=500, message=str(ex), data=[])
            

class GetUserReport(APIView):
    def get(self, request, user_id):
        pass