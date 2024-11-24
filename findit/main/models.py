from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


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



class Jobs(models.Model):
    CITY_CHOICES = [
        ('Almaty', 'Almaty'),
        ('Astana', 'Astana'),
        ('Shymkent', 'Shymkent'),
        ('Karaganda', 'Karaganda'),
        ('Taldykorgan', 'Taldykorgan'),
        ('Pavlodar', 'Pavlodar'),
        ('Semey', 'Semey'),
        ('Aktobe', 'Aktobe'),
        ('Ural', 'Ural'),
        ('Kokshetau', 'Kokshetau'),
        ('Petropavlovsk', 'Petropavlovsk'),
        ('Turkistan', 'Turkistan'),
        ('Aktau', 'Aktau'),
        ('Taraz', 'Taraz'),
        ('Kyzylorda', 'Kyzylorda'),
        ('Zhezkazgan', 'Zhezkazgan'),
        ('Kostanay', 'Kostanay'),
        ('Ekibastuz', 'Ekibastuz'),
        ('Balkhash', 'Balkhash'),
        ('Zalynsk', 'Zalynsk'),
        ('Esik', 'Esik'),
        ('Sergeli', 'Sergeli'),
        ('Zhanaozen', 'Zhanaozen'),
        ('Kandagat', 'Kandagat'),
        ('Shalkar', 'Shalkar'),
        ('Koktal', 'Koktal'),
        ('Yassy', 'Yassy'),
        ('Khromtau', 'Khromtau'),
        ('Nurin', 'Nurin'),
    ]

    title = models.CharField(max_length=255)
    task = models.TextField()
    city = models.CharField('City', max_length=100, choices=CITY_CHOICES)
    price = models.CharField(max_length=100)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_jobs',
        default=1
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name ='Job'
        verbose_name_plural ='Jobs'