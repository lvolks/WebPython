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

    return HttpResponse(template.render({
        'tasks': tasks,
        'user': request.user,
    }, request))