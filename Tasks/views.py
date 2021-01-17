from django.shortcuts import render , redirect , get_object_or_404
from .serializers import *
from .forms import CreateTaskForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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
        return Task.objects.filter(author=self.request.user).order_by('-date_created')


class AllTasksCalenderViews(LoginRequiredMixin, ListView):
    model = Task
    template_name = "Tasks/task_calender_view.html"
    context_object_name = "tasks"

    def get_queryset(self):
        return Task.objects.filter(author=self.request.user)


# class TaskCreateView(LoginRequiredMixin, CreateView):
#     model = Task
# #   The Field Variable Tell CreateView Class witch field that we want to update on the creation
#     template_name = "Tasks/task_create.html"
#     fields = ['problem', 'weeks', 'description', 'email_attached_file', 'start_date']
#
#     def get_context_data(self, **kwargs):
#         context = super(TaskCreateView, self).get_context_data(**kwargs)  # get the default context data
#         return context
#
#     def form_valid(self, form):
# #       this will set the form instance author to the user that log in , in the request
#         form.instance.author = self.request.user
#         return super().form_valid(form)

@login_required
def create_task(request):
    if request.method == 'POST':
        task_form = CreateTaskForm(request.POST, request.FILES)
        # type = request.FILES['email_attached_file'].name.split(".")[-1]
        file = request.FILES['email_attached_file'] if 'email_attached_file' in request.FILES.keys() else None
        if file:
            if file.size > 25000:
                messages.error(request, "File Size is Big, current Size:{}KB , maxSize 32KB"
                               .format(int(request.FILES['email_attached_file'].size / 1000)))
                return render(request, "Tasks/task_create.html", {'form': task_form})
            elif True: # .name.split(".")[-1] check type of file only mail files allowed
                # messages.error(request ,"Bad File Format")
                #return render(request, "Tasks/task_create.html", {'form': task_form})
                pass
        if task_form.is_valid():
            task = task_form.save(commit=False)
            task.author = request.user
#           the replace in the problem field is to avoid bugs at calendar app :(
            task.problem = task.problem.replace("`", "") if "`" in task.problem else task.problem
            task.save()
            messages.success(request, "Task Created!")
            return redirect('task-details', task.id)
        else:
            messages.warning(request, "Task Creation failed - Whats Wrong Dude?")
    else:
        # Here the instance= will add the data to the fields...
        task_form = CreateTaskForm(instance=request.user)

    context = {
        'form': task_form,
    }
    return render(request, "Tasks/task_create.html", context)


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


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    context_object_name = "task"
    success_url = '/tasks/alltasks/'

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


# def calender(request):
#     context = {'title': 'About Me!',
#                }
#     return render(request, 'Tasks/task_calender_view.html', context)