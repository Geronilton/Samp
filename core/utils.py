from datetime import date, timedelta
from .models import Mensalidades

def criar_mensalidade_para_assinatura(assinatura):
    vencimento = date.today() + timedelta(days=30)  # vencimento 30 dias após assinatura
    Mensalidades.objects.create(
        assinatura=assinatura,
        valor=assinatura.valor,
        vencimento=vencimento,
        status='pendente'
    )