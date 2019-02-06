from indice_transparencia.models import Person
from django.utils import timezone
from templated_email import send_templated_mail
from django.conf import settings
from django.contrib.sites.models import Site
import datetime

class EmailDigest(object):
    def get_context(self):
        context = {}
        now = timezone.now()
        una_semana_atras = now - datetime.timedelta(days=settings.DIGEST_MAIL_DAYS_REPORT)
        context['persons'] = Person.objects.filter(modified__gte=una_semana_atras)
        return context
        
    def send_mail(self):
        site = Site.objects.get_current()
        send_templated_mail(
                        template_name='digest_mail',
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[settings.DIGEST_MAIL_RECEIVER],
                        context={
                            'last_date': timezone.now() - datetime.timedelta(days=settings.DIGEST_MAIL_DAYS_REPORT),
                            'persons': self.get_context()['persons'],
                            'site': site,
                            'report_url': 'media/reports/report_'+str(timezone.now()).split(" ")[0]+'.csv'
                            }
                        )
