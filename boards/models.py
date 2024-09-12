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
    shared_with = models.ManyToManyField(User, related_name='shared_tasks', blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')

    @classmethod
    def createTask(cls, title, description, status, user):
        task = cls(title=title, description=description, status=status, user=user)
        task.save()
        return task
    
    @classmethod
    def editTask(cls, task_id, title, description, status, user):
        try:
            task = cls.objects.get(id=task_id, user=user)

            task.title = title
            task.description = description
            task.status = status

            task.save()

            return task

        except Exception:
            raise ValueError(f"Tarefa com id {task_id} não foi encontrada.")