from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader

from boards.models import Task


# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        return redirect("/login")
    template = loader.get_template("index.html")

    tasks = Task.objects.filter(user=request.user)

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
    print(task_id)

def createTask(request):
    template = loader.get_template("createTask.html")

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        status = request.POST.get('status') or 'pending'  # Padrão 'pending' se não for fornecido

        if not title or not description:
            return HttpResponse(template.render({
                'error_message': 'Preencha todos os campos!',
                'title': title,
                'description': description,
                'status': status,
            }, request))

        existing_task = Task.objects.filter(title=title).exists()
        if existing_task:
            return HttpResponse(template.render({
                'error_message': 'Já existe uma tarefa com esse nome!',
                'title': title,
                'description': description,
                'status': status,
            }, request))

        try:
            Task.createTask(title=title, description=description, status=status, user=request.user)
            print("created")
            return redirect("/")
        except Exception as ex:
            print(ex)
            return HttpResponse(template.render({
                'error_message': 'Ocorreu um erro inesperado: ' + str(ex),
                'title': title,
                'description': description,
                'status': status,
            }, request))

    return HttpResponse(template.render({}, request))



def editTask(request, task_id):
    template = loader.get_template("editTask.html")

    if request.method == 'POST':  # Usar POST para enviar os dados do formulário
        title = request.POST.get('title')
        description = request.POST.get('description')
        status = request.POST.get('status') or 'pending'  # Padrão 'pending' se não for fornecido

        if not title or not description:
            return HttpResponse(template.render({
                'error_message': 'Preencha todos os campos!',
                'title': title,
                'description': description,
                'status': status,
            }, request))

        try:
            # Edita a task existente com o task_id fornecido
            Task.editTask(task_id=task_id, title=title, description=description, status=status, user=request.user)
            print("edited")
            return redirect("/")
        except ValueError as ex:  # Caso task não seja encontrada
            return HttpResponse(template.render({
                'error_message': str(ex),
                'title': title,
                'description': description,
                'status': status,
            }, request))
        except Exception as ex:
            print(ex)
            return HttpResponse(template.render({
                'error_message': 'Ocorreu um erro inesperado: ' + str(ex),
                'title': title,
                'description': description,
                'status': status,
            }, request))

    try:
        # Pré-popular o formulário com os dados atuais da task (GET)
        task = Task.objects.get(id=task_id, user=request.user)
        return HttpResponse(template.render({
            'title': task.title,
            'description': task.description,
            'status': task.status,
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


    # TODO

