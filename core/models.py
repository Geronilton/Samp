from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Empresas(AbstractUser):
    nome = models.CharField('Nome',max_length=100)
    email = models.EmailField('Email',max_length=100)

    USERNAME_FIELD = 'email'

class Assinantes(models.Model):
    nome = models.CharField('Nome',max_length=100)
    email = models.EmailField('Email',max_length=100)
    telefone = models.CharField('Telefone', max_length=20, blank=True, null=True)
    empresa = models.ForeignKey(Empresas, on_delete=models.PROTECT)

class Mensalidades(models.Model):
    valor = models.DecimalField('Valor da Mensalidade', max_digits=5, decimal_places=2)
    vencimento = models.DateField('Vencimento')
    status = models.BooleanField()
    data_pagamento = models.DateField()
    data_criado = models.DateField(auto_now_add=True)
    assinantes = models.ManyToManyField(Assinantes)