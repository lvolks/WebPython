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

    # TODO

