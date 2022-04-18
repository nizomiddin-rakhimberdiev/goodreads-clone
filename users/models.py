from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class CustomUser(AbstractUser):
    profile_picture = models.ImageField(default='default_profile_pic.png')

    def full_name(self):
        return f"{self.first_name} {self.last_name}"