from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.functions import datetime
import datetime as py_datetime


class Task(models.Model):
    problem = models.CharField(max_length=40)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    days = models.SmallIntegerField(null=False, blank=False, validators=[MinValueValidator(0)])
    description = models.CharField(max_length=40)
    date_created = models.DateTimeField(default=timezone.now)
    email_attached_file = models.FileField(upload_to="Emails_Files_Tasks", blank=True)
    start_date = models.DateTimeField(blank=False, default= datetime.datetime.now)

    def __str__(self):
        return f"<My Tasks obj -> tasks_name = {self.problem}>"

    def get_absolute_url(self):
    #   reverse function return a url string with self.pk variable for the urls.py , and the url.py set the <int:pk>
        return reverse('task-details', kwargs={'pk': self.pk})

    @property
    def end_date(self):
        return self.start_date + py_datetime.timedelta(days=self.days)


class TaskDetail(models.Model):
    state = ((1, "open"),
             (0, "closed"),
             (2, "stuck"))
    problem = models.CharField(max_length=60)
    mission = models.CharField(max_length=60)
    responsibility = models.CharField(max_length=60, blank=True)
    email = models.EmailField(blank=True)
    status = models.SmallIntegerField(default=1, blank=False, choices=state)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self):
        return f"<TaskDetails problem = {self.problem}>"


class FullReport(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=timezone.now)
    file_path = models.CharField(max_length=110)

    def __str__(self):
        return f"file:{self.file_path}"
