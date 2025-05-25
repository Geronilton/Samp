from datetime import date, timedelta
from ..models import Mensalidades
from django.utils.timezone import now


def criar_mensalidade_para_assinatura(assinatura):
    vencimento = date.today() + timedelta(days=30)  
    Mensalidades.objects.create(
        assinatura=assinatura,
        valor=assinatura.valor,
        vencimento=vencimento,
        status='pendente'
    )

def primeira_mensalidade_para_assinatura(assinatura):
    vencimento = date.today() + timedelta(days=30)  
    Mensalidades.objects.create(
        assinatura=assinatura,
        valor=assinatura.valor,
        vencimento=vencimento,
        data_pagamento=now(),
        status='pago'
    )