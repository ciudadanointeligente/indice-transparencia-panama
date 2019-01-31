from django.core.management.base import BaseCommand, CommandError
from indice_transparencia.digesters import EmailDigest


class Command(BaseCommand):
    help = 'Envia mails del digest'
    
    def handle(self, *args, **options):
        digester = EmailDigest()
        digester.send_mail()