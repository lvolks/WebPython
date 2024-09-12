from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from boards.models import Task, task_status_enum
from django.db.models import Q

# Create your views here.
@login_required(login_url='/login')
def index(request):
    if not request.user.is_authenticated:
        return redirect("/login")
    template = loader.get_template("index.html")

    tasks = Task.objects.filter(Q(user=request.user) | Q(shared_with=request.user))

    pending = tasks.filter(status='pending')
    doing = tasks.filter(status='doing')
    done = tasks.filter(status='done')

    return HttpResponse(template.render({
        'pending': pending,
        'doing': doing,
        'done': done,
        'user': request.user,
    }, request))

task_status_color = {
    'pending': 'yellow',
    'doing': 'blue',
    'done': 'green'
}

def task(request, task_id):
    if not request.user.is_authenticated:
        return redirect("/login")
    try:

        task = Task.objects.get(id=task_id)
        status = task_status_enum[task.status]
        status_color = task_status_color[task.status]
        return render(request, 'details.html', {
            'task': task,
            'status': status,
            'status_color': status_color
        })
    except Task.DoesNotExist:
        return HttpResponse("Task não encontrada", status=404)

@login_required(login_url='/login')
def createTask(request):
    template = loader.get_template("createTask.html")

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        status = request.POST.get('status') or 'pending'
        shared_user_ids = request.POST.getlist('shared_with')

        if not title or not description:
            return HttpResponse(template.render({
                'error_message': 'Preencha todos os campos!',
                'title': title,
                'description': description,
                'status': status,
                'users': User.objects.exclude(id=request.user.id)
            }, request))

        existing_task = Task.objects.filter(title=title).exists()
        if existing_task:
            return HttpResponse(template.render({
                'error_message': 'Já existe uma tarefa com esse nome!',
                'title': title,
                'description': description,
                'status': status,
                'users': User.objects.exclude(id=request.user.id)
            }, request))

        try:
            task = Task.createTask(title=title, description=description, status=status, user=request.user)
            shared_users = User.objects.filter(id__in=shared_user_ids)
            task.shared_with.set(shared_users)
            return redirect("/")
        except Exception as ex:
            print(ex)
            return HttpResponse(template.render({
                'error_message': 'Ocorreu um erro inesperado: ' + str(ex),
                'title': title,
                'description': description,
                'status': status,
                'users': User.objects.exclude(id=request.user.id)
            }, request))

    return render(request, 'createTask.html', {
        'users': User.objects.exclude(id=request.user.id)
    })



@login_required(login_url='/login')
def editTask(request, task_id):
    template = loader.get_template("editTask.html")

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        status = request.POST.get('status') or 'pending'
        shared_user_ids = request.POST.getlist('shared_with')

        if not title or not description:
            return HttpResponse(template.render({
                'error_message': 'Preencha todos os campos!',
                'title': title,
                'description': description,
                'status': status,
                'users': User.objects.exclude(id=request.user.id),
                'task_id': task_id
            }, request))

        try:
            task = Task.editTask(task_id=task_id, title=title, description=description, status=status, user=request.user)
            
            shared_users = User.objects.filter(id__in=shared_user_ids)
            
            task.shared_with.set(shared_users)
            
            return redirect("/tasks/" + str(task.id))
        except ValueError as ex:
            return HttpResponse(template.render({
                'error_message': str(ex),
                'title': title,
                'description': description,
                'status': status,
                'users': User.objects.exclude(id=request.user.id),
                'task_id': task_id
            }, request))
        except Exception as ex:
            print(ex)
            return HttpResponse(template.render({
                'error_message': 'Ocorreu um erro inesperado: ' + str(ex),
                'title': title,
                'description': description,
                'status': status,
                'users': User.objects.exclude(id=request.user.id),
                'task_id': task_id
            }, request))
        
    try:
        task = Task.objects.get(id=task_id, user=request.user)
        return HttpResponse(template.render({
            'title': task.title,
            'description': task.description,
            'status': task.status,
            'shared_with': task.shared_with.values_list('id', flat=True),
            'users': User.objects.exclude(id=request.user.id),
            'task_id': task_id
        }, request))
    except Task.DoesNotExist:
        return HttpResponse("Task não encontrada", status=404)
    


def deleteTask(request, task_id):
    
    try:
        task = Task.objects.get(id=task_id, user=request.user)
        task.delete()
        return redirect("/")
    except Exception as ex:
        print(f"Erro ao tentar deletar a task: {ex}")
        return HttpResponse("Ocorreu um erro ao deletar a task.")
