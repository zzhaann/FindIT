from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth import get_user_model






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
        ('', 'Выберите город'),
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
    company_name = models.CharField(max_length=255)
    company_description = models.TextField()
    company_logo = models.ImageField(upload_to='company_logos/', null=True, blank=True)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)

    title = models.CharField(max_length=255)
    task = models.TextField()
    city = models.CharField('City', max_length=100, choices=CITY_CHOICES, blank=False)
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
        verbose_name = 'Job'
        verbose_name_plural = 'Jobs'





class Application(models.Model):
    job = models.ForeignKey('Jobs', on_delete=models.CASCADE, related_name='applications')
    worker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Обеспечивает уникальность отклика работника на одну вакансию
        constraints = [
            models.UniqueConstraint(fields=['job', 'worker'], name='unique_job_worker_application')
        ]

    def __str__(self):
        return f"{self.worker.username} -> {self.job.title}"



class Resume(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='resume')
    city = models.CharField(max_length=100)
    experience = models.TextField()
    soft_skills = models.TextField()
    programming_languages = models.TextField()
    education = models.CharField(max_length=255)
    portfolio = models.FileField(upload_to='portfolios/', null=True, blank=True)

    def __str__(self):
        return self.user.username






User = get_user_model()

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f'Message from {self.sender} to {self.recipient}'