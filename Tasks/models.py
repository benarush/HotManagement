from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.


class Task(models.Model):
    problem = models.CharField(max_length=40)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    weeks = models.SmallIntegerField(null=False, blank=False ,validators=[MaxValueValidator(100), MinValueValidator(1)])
    description = models.CharField(max_length=40)
    date_created = models.DateTimeField(default=timezone.now)
    email_attached_file = models.FileField(upload_to="Emails_Files_Tasks", blank=True)
    start_date = models.DateTimeField(blank=False)

    def __str__(self):
        return f"<My Tasks obj -> tasks_name = {self.problem}>"

    def get_absolute_url(self):
    #   reverse function return a url string with self.pk variable for the urls.py , and the url.py set the <int:pk>
        return reverse('task-details', kwargs={'pk': self.pk})


class TaskDetail(models.Model):
    state = ((True, "open"),
             (False, "closed"))
    problem = models.CharField(max_length=60)
    mission = models.CharField(max_length=60)
    responsibility = models.CharField(max_length=60, blank=True)
    email = models.EmailField(blank=True)
    status = models.BooleanField(default=True, blank=False, choices=state)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self):
        return f"<TaskDetails problem = {self.problem}>"



