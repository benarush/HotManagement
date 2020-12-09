from django.shortcuts import render
from django.shortcuts import render , redirect , get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Task, TaskDetail
from django.contrib.auth.models import User
from django.views.generic import (
    ListView ,
)# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin


class AllTasksViews(LoginRequiredMixin, ListView):
    model = Task
    template_name = "Tasks/tasks.html"
    context_object_name = "tasks"

    # def get_context_data(self, **kwargs):
    #     context = super(EventListHome, self).get_context_data(**kwargs)  # get the default context data
    #     context['event'] = Event.objects.filter(user_id = self.request.user.id).first()
    #     return context
    def get_queryset(self):
    #      the get_object_or_404 return 404 if the user dont exist , and if he exist it return his user object
        return Task.objects.all().filter(author = self.request.user)


def home(request):
    context = {'title': 'About Me!',
               }
    return render(request, 'Tasks/home.html', context)


