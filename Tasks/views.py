from django.shortcuts import render , redirect , get_object_or_404
from .serializers import *
from django.contrib.auth.models import User
from django.views.generic import (
    ListView ,
    DetailView,
    CreateView ,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin


class AllTasksViews(LoginRequiredMixin, ListView):
    model = Task
    template_name = "Tasks/tasks.html"
    context_object_name = "tasks"

    def get_queryset(self):
    #      the get_object_or_404 return 404 if the user dont exist , and if he exist it return his user object
        return Task.objects.filter(author=self.request.user)


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


class TaskDetailsView(UserPassesTestMixin, LoginRequiredMixin, DetailView):
    model = Task

    def get_context_data(self, **kwargs):
        context = super(TaskDetailsView, self).get_context_data(**kwargs)  # get the default context data
        task = self.get_object()
        context['task_details'] = TaskDetail.objects.filter(task=task)
        context["open_task_details_num"] = context['task_details'].filter(status=True).count()
        context["close_task_details_num"] = context['task_details'].count()-context["open_task_details_num"]
        return context

    def test_func(self):
#   The get_object() Will Get the object that we want to update.
        task = self.get_object()
        if self.request.user == task.author:
            return True
        return False


def home(request):
    context = {'title': 'About Me!',
               }
    return render(request, 'Tasks/home.html', context)
