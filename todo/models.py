from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Todo(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE , related_name="todos")

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} by {self.user.username}"
    
    class Meta:
        ordering = ["-created_at"]

    
    