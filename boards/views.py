from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.contrib.auth.models import User

from boards.models import Task
from django.db.models import Q

# Create your views here.

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

def task(request, task_id):
    if not request.user.is_authenticated:
        return redirect("/login")
    try:
        task = Task.objects.get(id=task_id)
        return render(request, 'details.html', {'task': task})
    except Task.DoesNotExist:
        return HttpResponse("Task não encontrada", status=404)

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
            # Cria a tarefa
            task = Task.createTask(title=title, description=description, status=status, user=request.user)
            # Converte os IDs dos usuários para instâncias de User
            shared_users = User.objects.filter(id__in=shared_user_ids)
            # Define os usuários compartilhados
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
        'users': User.objects.exclude(id=request.user.id)  # Lista de usuários excluindo o próprio usuário
    })




def editTask(request, task_id):
    template = loader.get_template("editTask.html")

    if request.method == 'POST':  # Usar POST para enviar os dados do formulário
        title = request.POST.get('title')
        description = request.POST.get('description')
        status = request.POST.get('status') or 'pending'  # Padrão 'pending' se não for fornecido
        shared_user_ids = request.POST.getlist('shared_with')  # IDs dos usuários compartilhados

        if not title or not description:
            return HttpResponse(template.render({
                'error_message': 'Preencha todos os campos!',
                'title': title,
                'description': description,
                'status': status,
                'users': User.objects.exclude(id=request.user.id),
                'task_id': task_id  # Para repopular o formulário em caso de erro
            }, request))

        try:
            # Edita a task existente com o task_id fornecido
            task = Task.editTask(task_id=task_id, title=title, description=description, status=status, user=request.user)
            
            # Converte os IDs dos usuários para instâncias de User
            shared_users = User.objects.filter(id__in=shared_user_ids)
            
            # Define os usuários compartilhados
            task.shared_with.set(shared_users)
            
            return redirect("/")
        except ValueError as ex:  # Caso task não seja encontrada
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
        # Pré-popular o formulário com os dados atuais da task (GET)
        task = Task.objects.get(id=task_id, user=request.user)
        return HttpResponse(template.render({
            'title': task.title,
            'description': task.description,
            'status': task.status,
            'shared_with': task.shared_with.values_list('id', flat=True),  # IDs dos usuários com quem a tarefa é compartilhada
            'users': User.objects.exclude(id=request.user.id),  # Lista de usuários excluindo o próprio usuário
            'task_id': task_id
        }, request))
    except Task.DoesNotExist:
        return HttpResponse("Task não encontrada", status=404)
    

    
def deleteTask(request, task_id):
    
    try:
        task = Task.objects.get(id=task_id, user=request.user)
        task.delete()
        return redirect("/")  # Redireciona para a página inicial após deletar
    except Exception as ex:
        print(f"Erro ao tentar deletar a task: {ex}")
        return HttpResponse("Ocorreu um erro ao deletar a task.")


def details(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
        return render(request, 'details.html', {'task': task})
    except Task.DoesNotExist:
        return HttpResponse("Task não encontrada", status=404)

