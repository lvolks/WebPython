"""
URL configuration for trelle project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

import auth.views
import boards.views

urlpatterns = [
    path('admin/', admin.site.urls),
    # auth
    path('login/',auth.views.login),
    path('register/',auth.views.register),

    # boards
    path('',boards.views.index),
    path('tasks/<int:task_id>', boards.views.task, name='details'),

    path('createtask/', boards.views.createTask),
    path('edittask/<int:task_id>', boards.views.editTask),
    path('tasks/delete/<int:task_id>/', boards.views.deleteTask, name='delete_task'),
]
