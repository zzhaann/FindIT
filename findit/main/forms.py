# forms.py
from django import forms
from .models import CustomUser

class CustomUserCreationForm(forms.ModelForm):
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'role')  # Убедитесь, что вы указали нужные поля
