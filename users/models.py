from django.db import models
from django.contrib.auth.models import User
from .ImageManipulation import ImageManipulation as MyCustomImageManipulation

class Profile(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    image = models.ImageField(default="profile_pics/default/Male_default.png" , upload_to='profile_pics')
    role = (('male' , 'Male'),
            ('female' , 'Female'))
    gender = models.CharField(max_length=10, choices=role , default='male')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        MyCustomImageManipulation(self.image.path)


    def __str__(self):
        return "{} Profile".format(self.user.username)



class Report(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    file = models.FileField(upload_to="Reports")