from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Empresas(models.Model):
    nome = models.CharField('Nome', max_length=100)
    email = models.EmailField('Email', max_length=100, unique=True)
    categoria = models.CharField('Categoria', max_length=100)
    endereco = models.CharField('Endereço', max_length=200)
    cidade = models.CharField('Cidade', max_length=200)
    instagram = models.URLField('Instagram', max_length=200, blank=True, null=True)
    whatsapp = models.URLField('WhatsApp', max_length=200, blank=True, null=True)
    chave_pix = models.CharField('Chave Pix', max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nome


class Usuario(AbstractUser):
    
    TIPO_USUARIO_CHOICES = (
        ('admin', 'Administrador de Empresa'),
        ('assinante', 'Assinante'),
    )

    email = models.EmailField('Email', unique=True) 
    telefone = models.CharField('Telefone', max_length=20, blank=True, null=True)
    tipo_usuario = models.CharField(max_length=10, choices=TIPO_USUARIO_CHOICES, default='assinante')
    empresa = models.ForeignKey(Empresas, on_delete=models.CASCADE, blank=True, null=True)
    
    USERNAME_FIELD = 'email'  
    REQUIRED_FIELDS = []
    def __str__(self):
        empresa_nome = self.empresa.nome if self.empresa else "Sem empresa"
        return f'{self.email} - {empresa_nome}'

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
    status = models.CharField('Status', max_length=10, choices=STATUS_CHOICES, default='pendente',)
    data_pagamento = models.DateField(blank=True, null=True)
    data_criado = models.DateField(auto_now_add=True)
    assinatura = models.ForeignKey('Assinatura', on_delete=models.CASCADE, related_name='mensalidades')

class Servico(models.Model):
    nome = models.CharField('Nome do Serviço', max_length=100)
    descricao = models.TextField('Descrição', blank=True)
    valor = models.DecimalField('Valor do Serviço', max_digits=7, decimal_places=2)
    empresa = models.ForeignKey(Empresas, on_delete=models.CASCADE, related_name='servicos')

    def __str__(self):
        return f'{self.nome} - {self.empresa.nome}'


class Assinatura(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('ativa', 'Ativa'),
        ('cancelada', 'Cancelada'),
    ]

    assinante = models.ForeignKey(Assinantes, on_delete=models.CASCADE, related_name='assinaturas')
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE, related_name='assinaturas')
    data_assinatura = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pendente')
    valor = models.DecimalField('Valor da Assinatura', max_digits=7, decimal_places=2)

    def __str__(self):
        return f'{self.assinante.nome} - {self.servico.nome} ({self.status})'