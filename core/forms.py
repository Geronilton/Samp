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

    valor = forms.DecimalField(
        max_digits=10,  # Número total de dígitos, incluindo os decimais
        decimal_places=2,  # Número de casas decimais
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite o valor (somente números)',
            'type': 'number',  # Garante entrada numérica no frontend
            'step': '0.01',  # Permite valores decimais no campo
        }),
    )
    class Meta:
        model = Mensalidades
        fields = ['valor', 'vencimento', 'status', 'data_pagamento']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'valor': forms.TextInput(attrs={'class': 'form-control'}),
            'vencimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'data_pagamento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

