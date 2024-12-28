from celery import shared_task, Celery
from Myapp.models import Todo, UserRecord
from Myapp.Services.utilities import Logger
from django.contrib.auth.models import User

logger = Logger('tasks')
    


@shared_task
def manage_user_record(user_id):
    try:
        print("manage_user_record called")
        user_obj = User.objects.filter(id=user_id).first()
        if user_obj:
            """GETING RECORD OF USER"""
            todo_qs = Todo.objects.filter(user=user_id)
            pending = todo_qs.filter(status="PENDING").count()
            completed = todo_qs.filter(status="COMPLETED").count()
            deleayed = todo_qs.filter(status="DELEAYED").count()
            
            """CREATE OR UPDATE RECORD OF USER"""
            user_record_obj = UserRecord.objects.filter(user=user_id).first()
            if not user_record_obj:
                user_record_obj = UserRecord()
                user_record_obj.user = user_obj
            user_record_obj.pending = pending
            user_record_obj.completed = completed
            user_record_obj.deleyed = deleayed
            user_record_obj.save()
        else:
            message = {
                "function_name": "manage_user_record",
                "message": f"User Does not exist For this id {user_id}"
                }
            logger.warning(message)
    except Exception as ex:
        print("ex")
        logger.error(str(ex))
        
@shared_task
def schedul_task():
    """NEED TO ADD LOCKING HERE"""
    user_qs = User.objects.all()
    for user in user_qs:
        manage_user_record.delay(user.id)
