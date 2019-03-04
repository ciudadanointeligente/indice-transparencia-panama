from django.core.management.base import BaseCommand, CommandError
from indice_transparencia.digesters import EmailDigest
from indice_transparencia.models import Contact
from django.core.management import call_command
from django.contrib.sites.models import Site
from templated_email import send_templated_mail
from django.conf import settings


class Command(BaseCommand):
    help = 'Envia mails a contactos'
    
    def handle(self, *args, **options):
        # call_command('generate_report')
        # digester = EmailDigest()
        # digester.send_mail()
        contacts = Contact.objects.all()
        counter = 0
        for contact in contacts:
            email = contact.email
            person = contact.person
            uuid = contact.identifier
            site = Site.objects.get_current()
            send_templated_mail(
                                template_name='initial_2',
                                from_email=settings.DEFAULT_FROM_EMAIL,
                                recipient_list=[email],
                                context={
                                    'contact': contact,
                                    'person': person,
                                    'site': site,
                                },
                        )
            print('send email to contact: ' + email)
            counter += 1;
        print('total mails sent: ' + str(counter))