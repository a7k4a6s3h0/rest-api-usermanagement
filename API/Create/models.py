from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager
# Create your models here.


class User(AbstractUser):
    profile_photo = models.ImageField(upload_to='images/')
    username = models.CharField(max_length=30,unique=True)
    mobile_no = models.IntegerField(null=True)
    
    objects = UserManager()

    def __str__(self):
        return self.username

        