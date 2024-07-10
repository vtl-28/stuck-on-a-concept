from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from cloudinary.models import CloudinaryField


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=1000, blank=True)
    city = models.CharField(max_length=100, blank=True, default="Johannesburg")
    image = CloudinaryField('image', default='https://res.cloudinary.com/dd1jqwp94/image/upload/v1720597929/default_dktxl8.jpg', transformation={"width": 300, "height": 300, "crop": "limit"})

    def __str__(self):
        return f'{self.user.username} - Profile'

