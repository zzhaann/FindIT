from django import forms
from .models import CustomUser, Jobs
from django.forms import ModelForm, TextInput
from django import forms
from django.contrib.auth.forms import UserCreationForm



class JobsForm(forms.ModelForm):
    class Meta:
        model = Jobs
        fields = ["title", "task", "city", "price"]
        widgets = {
            "title": forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название'
            }),
            "task": forms.Textarea(attrs={
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
