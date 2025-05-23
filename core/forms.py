from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Empresas, Usuario, Assinantes, Mensalidades,Servico

class UserForm(UserCreationForm):
    email = forms.EmailField(max_length=100, help_text='Required. Inform a valid email address.')

    class Meta:
        model = Usuario
        fields = ['username','email','telefone','password1', 'password2']

class EmpresasForm(forms.ModelForm):
    class Meta:
        model = Empresas
        fields = ['nome', 'email','categoria', 'endereco','instagram','whatsapp']
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder':' Nome da empresa'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'categoria': forms.TextInput(attrs={'placeholder': 'Categoria. ex: esporte, lazer,transporte... '}),
            'endereco': forms.TextInput(attrs={'placeholder': 'Endereço. ex: Rua da Escola, 10, Goianinha'}),
            'instagram': forms.URLInput(attrs={'placeholder': 'Opcional:Link do Instagram'}),
            'whatsapp': forms.URLInput(attrs={'placeholder': 'Opcional:Link do WhatsApp'}),
        }


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

class ServicoForm(forms.ModelForm):
    class Meta:
        model = Servico
        fields = ['nome', 'descricao', 'valor']

# -------------------------------------------------

class PesquisaEmpresaForm(forms.Form):
    busca = forms.CharField(label='Pesquisar', required=False,
            widget=forms.TextInput(attrs={
            'placeholder': 'Buscar por nome, categoria ou endereço...',
            'class': 'input-busca' 
        }))
 
 
class PesquisaForm(forms.Form):
    busca = forms.CharField(label='Pesquisar', required=False,
            widget=forms.TextInput(attrs={
            'placeholder': 'Buscar...',
            'class': 'input-busca' 
        }))
 