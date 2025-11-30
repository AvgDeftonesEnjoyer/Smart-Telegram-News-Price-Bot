from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    telegram_id = models.CharField(max_length=128, unique=True)
    username = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.username