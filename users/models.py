from django.db import models
from django.contrib.auth.models import User
from PIL import Image
class Profile(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    image = models.ImageField(default="profile_pics/default/Male_default.png" , upload_to='profile_pics')
    role = (('male' , 'Male'),
            ('female' , 'Female'))
    gender = models.CharField(max_length=10 , choices=role , default='male')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        ORIENT = {
            # exif_val: (rotate degrees cw, mirror 0=no 1=horiz 2=vert); see http://www.sno.phy.queensu.ca/~phil/exiftool/TagNames/EXIF.html
            2: (0, 1),
            3: (180, 0),
            4: (0, 2),
            5: (90, 1),
            6: (270, 0),
            7: (270, 1),
            8: (90, 0),
        }

        img_format = img.format

        # fix imageManipulate orientation (issue with jpegs taken by cams; phones in particular):
        try:
            orient = img._getexif()[274]
        except (AttributeError, KeyError, TypeError, ValueError):
            orient = 1  # default (normal)
        if orient in ORIENT:
            (rotate, mirror) = ORIENT[orient]
            if rotate:
                img = img.rotate(rotate)
            if mirror == 1:
                img = img.transpose(Image.FLIP_LEFT_RIGHT)
            elif mirror == 2:
                img = img.transpose(Image.FLIP_TOP_BOTTOM)

        if img.height > 300 or img.width > 300:
            resize = (300 , 300)
            img.thumbnail(resize)
            img.save(self.image.path)

    def __str__(self):
        return "{} Profile".format(self.user.username)