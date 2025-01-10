from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Empresas(models.Model):
    nome = models.CharField('Nome', max_length=100)
    email = models.EmailField('Email', max_length=100, unique=True)

    def __str__(self):
        return self.nome

class EmpresaUser(AbstractUser):
    email = models.EmailField('Email', unique=True)  
    empresa = models.ForeignKey(Empresas, on_delete=models.CASCADE)

    USERNAME_FIELD = 'email'  
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.email} - {self.empresa.nome}'

class Assinantes(models.Model):
    nome = models.CharField('Nome',max_length=100)
    email = models.EmailField('Email',max_length=100)
    telefone = models.CharField('Telefone', max_length=20, blank=True, null=True)
    empresa = models.ForeignKey(Empresas, on_delete=models.PROTECT)

class Mensalidades(models.Model):
    STATUS_CHOICES = [
        ('pago', 'Pago'),
        ('pendente', 'Pendente'),
        ('atrasado', 'Atrasado'),
    ]

    valor = models.DecimalField('Valor da Mensalidade', max_digits=5, decimal_places=2)
    vencimento = models.DateField('Vencimento')
    status = models.CharField(
        'Status',
        max_length=10,
        choices=STATUS_CHOICES,  # Define as opções disponíveis no status
        default='pendente',  # Valor default para o status
    )
    data_pagamento = models.DateField(blank=True, null=True)
    data_criado = models.DateField(auto_now_add=True)
    assinantes = models.ForeignKey(Assinantes, on_delete=models.CASCADE)