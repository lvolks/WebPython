from django.db import models
from django.contrib.auth.models import User

task_status_enum = {
    'pending': 'Pendente',
    'doing': 'Em andamento',
    'done': 'Concluído'
}

class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, default='pending')
    creation_date = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')