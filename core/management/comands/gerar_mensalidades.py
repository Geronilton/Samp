from django.core.management.base import BaseCommand
from core.models import Assinatura, Mensalidades
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Gera mensalidades para assinaturas ativas'

    def handle(self, *args, **kwargs):
        hoje = timezone.now().date()
        novas = 0

        for assinatura in Assinatura.objects.filter(status='ativo'):
            ultima = Mensalidades.objects.filter(assinatura=assinatura).order_by('-vencimento').first()
            
            if not ultima or ultima.vencimento < hoje:
                nova_venc = hoje if not ultima else ultima.vencimento + timedelta(days=30)

                Mensalidades.objects.create(
                    assinatura=assinatura,
                    valor=assinatura.valor,
                    vencimento=nova_venc,
                    status='pendente'
                )
                novas += 1

        self.stdout.write(self.style.SUCCESS(f'Mensalidades criadas: {novas}'))
