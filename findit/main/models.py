
from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('worker', 'Работник'),
        ('employer', 'Работодатель'),
        ('admin', 'Админ'),
    ]

    role = models.CharField(
        choices=ROLE_CHOICES,
        default='worker',
        max_length=10
    )
