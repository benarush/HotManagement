from django.shortcuts import render
from django.shortcuts import render , redirect , get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Task, TaskDetail
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *

from django.contrib.auth.models import User
from django.contrib.messages.views import  SuccessMessageMixin

from django.views.generic import (
    ListView ,
    DetailView,
    CreateView ,
    UpdateView,
    DeleteView
)

# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin


class AllTasksViews(LoginRequiredMixin, ListView):
    model = Task
    template_name = "Tasks/tasks.html"
    context_object_name = "tasks"

    def get_queryset(self):
    #      the get_object_or_404 return 404 if the user dont exist , and if he exist it return his user object
        return Task.objects.all().filter(author = self.request.user)


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
#   The Field Variable Tell CreateView Class witch field that we want to update on the creation
    template_name = "Tasks/task_create.html"
    fields = ['problem', 'weeks', 'description', 'email_attached_file', 'start_date']

    def get_context_data(self, **kwargs):
        context = super(TaskCreateView, self).get_context_data(**kwargs)  # get the default context data
        return context

    def form_valid(self, form):
#       this will set the form instance author to the user that log in , in the request
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    fields = ['problem', 'weeks', 'description', 'email_attached_file', 'start_date']
    def get_context_data(self, **kwargs):
        context = super(TaskUpdateView, self).get_context_data(**kwargs)  # get the default context data
        return context

    def form_valid(self, form):
        #       this will set the form instance author to the user that log in , in the request
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
#   The get_object() Will Get the object that we want to update.
        task = self.get_object()
        if self.request.user == task.author:
            return True
        return False


class TaskDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Task
    context_object_name = "task"
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(TaskDeleteView, self).get_context_data(**kwargs)  # get the default context data
        return context

#   this method will check if the user author and the user that log in are same.
    def test_func(self):
#   The get_object() Will Get the object that we want to update.
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class TaskDetailsView(UserPassesTestMixin,LoginRequiredMixin,DetailView):
    model = Task

    def get_context_data(self, **kwargs):
        context = super(TaskDetailsView, self).get_context_data(**kwargs)  # get the default context data
        task = self.get_object()
        context['task_details'] = TaskDetail.objects.filter(task=task)
        return context

    def test_func(self):
#   The get_object() Will Get the object that we want to update.
        task = self.get_object()
        if self.request.user == task.author:
            return True
        return False



class TaskDetailsCreateView(LoginRequiredMixin, CreateView):
    model = TaskDetail
#   The Field Variable Tell CreateView Class witch field that we want to update on the creation
    template_name = "Tasks/task_details/create.html"
    fields = ['problem', 'mission', 'responsibility', 'email', 'status']

    def get_context_data(self, **kwargs):
        context = super(TaskDetailsCreateView, self).get_context_data(**kwargs)  # get the default context data
        return context

    def form_valid(self, form):
#       this will set the form instance author to the user that log in , in the request
        form.instance.task = self.request.GET
        return super().form_valid(form)

@login_required
@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'Get specific task info': '/tasks/alltasks/api/task_info/<str:pk>',
        'Get all sub tasks for a specific task': '/tasks/alltasks/api/sub_tasks/<str>',
    }
    return Response(api_urls)

@login_required
@api_view(['GET'])
def task_info(request,pk):
    try:
        task = Task.objects.get(id=pk)
    except:
        context = {"status": "failed" ,"error": "no such of task", "data": None, "subtasks": None}
        return Response(context)
    if request.user != task.author:
        return Response({"status": "failed" ,"error": "permission denied", "data": None, "subtasks": None})
    task_serializer = TaskSerializer(task, many=False)
    sub_task = SubTaskSerializer(task.taskdetail_set.all(),many=True)
    context = {
        "status": "Success",
        "error": None,
        "data": {"task": task_serializer.data},
        "subtasks": sub_task.data
    }
    return Response(context)


def home(request):
    context = {'title': 'About Me!',
               }
    return render(request, 'Tasks/home.html', context)
