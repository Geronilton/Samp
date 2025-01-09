from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Empresas, EmpresaUser, Assinantes, Mensalidades

class EmpresaUserForm(UserCreationForm):
    email = forms.EmailField(max_length=100, help_text='Required. Inform a valid email address.')

    class Meta:
        model = EmpresaUser
        fields = ['username', 'email', 'password1', 'password2']

class EmpresasForm(forms.ModelForm):
    class Meta:
        model = Empresas
        fields = ['nome', 'email']

class AssinantesForm(forms.ModelForm):
    class Meta:
        model = Assinantes
        fields = ['nome', 'email', 'telefone']

class MensalidadesForm(forms.ModelForm):
    class Meta:
        model = Mensalidades
        fields = ['valor', 'vencimento', 'status', 'data_pagamento']

