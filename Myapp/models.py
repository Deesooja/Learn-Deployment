from django.db import models
from django.contrib.auth.models import User 


class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    descriptions = models.CharField(max_length=500)
    status = models.CharField(max_length=120, choices=[("PENDING", "PENDING"), ("COMPLETED", "COMPLETED"), 
                                                       ("DELEAYED", "DELEAYED")], default="PENDING")
    estimated_completion_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
