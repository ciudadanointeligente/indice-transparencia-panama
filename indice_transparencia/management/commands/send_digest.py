from django.core.management.base import BaseCommand, CommandError
from indice_transparencia.digesters import EmailDigest
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Envia mails del digest'
    
    def handle(self, *args, **options):
        call_command('generate_report')
        digester = EmailDigest()
        digester.send_mail()