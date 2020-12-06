from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User , on_delete=models.CASCADE)

    def __str__(self):
        return self.title
#   this method define witch url to go after createView post creation
    def get_absolute_url(self):
#   reverse function return a url string with self.pk variable for the urls.py , and the url.py set the <int:pk>
        return reverse('post-details' , kwargs= {'pk': self.pk} )
