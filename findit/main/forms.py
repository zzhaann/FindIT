from django import forms
from .models import CustomUser, Jobs, Resume
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django import forms
from django.contrib.auth import get_user_model
from .models import Message




User = get_user_model()

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['recipient', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3}),
        }




def worker_profile(request, id):
    worker = CustomUser.objects.get(id=id)  # Получаем пользователя по ID
    resume = Resume.objects.get(user=worker)  # Получаем резюме для этого пользователя
    return render(request, 'worker_profile.html', {'worker': worker, 'resume': resume})



class JobsForm(forms.ModelForm):
    class Meta:
        model = Jobs
        fields = [
            "title", "task", "city", "price",
            "company_name", "company_description", "company_logo", "contact_email", "contact_phone"
        ]
        widgets = {
            "title": forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название работы'
            }),
            "task": forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите описание работы'
            }),
            "city": forms.Select(attrs={
                'class': 'form-control',
            }),
            "price": forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите цену работы'
            }),
            "company_name": forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название компании'
            }),
            "company_description": forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Описание компании'
            }),
            "contact_email": forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Контактный Email'
            }),
            "contact_phone": forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Контактный телефон'
            }),
        }


class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'role')


    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user


class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['city', 'experience', 'soft_skills', 'programming_languages', 'education', 'portfolio']


