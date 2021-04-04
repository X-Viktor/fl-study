from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(max_length=254, verbose_name='Email')

    def __str__(self):
        return self.username
