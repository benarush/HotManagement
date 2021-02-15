from django.http import Http404
from django.shortcuts import render , redirect , get_object_or_404
from .serializers import *
from .forms import CreateTaskForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
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
            elif True: # file.name.split(".")[-1] check type of file, only email files allowed
                # messages.error(request ,"Bad File Format")
                #return render(request, "Tasks/task_create.html", {'form': task_form})
                pass
        if task_form.is_valid():
            task = task_form.save(commit=False)
            task.author = request.user
#           the replace in the problem field is to avoid bugs at calendar app :(, "`" char is not allowed here
            task.problem = task.problem.replace("`", "") if "`" in task.problem else task.problem
            task.save()
            messages.success(request, "Task Created!")
            return redirect('task-details', task.id)
        else:
            messages.warning(request, "Task Creation failed - Whats Wrong Dude?")
    else:
        task_form = CreateTaskForm(instance=request.user)

    context = {
        'form': task_form,
    }
    return render(request, "Tasks/task_create.html", context)


class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    fields = ['problem', 'days', 'description', 'email_attached_file', 'start_date']

    def get_context_data(self, **kwargs):
        context = super(TaskUpdateView, self).get_context_data(**kwargs)  # get the default context data
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
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

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class TaskDetailsView(LoginRequiredMixin, DetailView):
    model = Task

    def get_context_data(self, **kwargs):
        context = super(TaskDetailsView, self).get_context_data(**kwargs)  # get the default context data
        if context['task'].author != self.request.user:
            raise Http404("Task does not exist or permission denied")
        context['task_details'] = TaskDetail.objects.filter(task=context['task'])
        context["open_task_details_num"] = context['task_details'].filter(status=1).count()
        context["close_task_details_num"] = context['task_details'].filter(status=0).count()
        context["stuck_task_details_num"] = context['task_details'].filter(status=2).count()
        return context


def home(request):
    context = {'title': 'About Me!',
               }
    task = Task.objects.all().prefetch_related('taskdetail_set')
    for t in task:
        print(t.taskdetail_set.all())
    return render(request, 'Tasks/home.html', context)

