from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Empresas

class EmpresasForm(UserCreationForm):
    class Meta:
        model = Empresas
        fields = ['nome', 'email','password1', 'password2']

