from django.core.management.base import BaseCommand, CommandError
from indice_transparencia.digesters import EmailDigest
from indice_transparencia.models import Person
from django.utils import timezone
import csv


class Command(BaseCommand):
    help = 'Envia informe de datos'
    
    def handle(self, *args, **options):
        
        model = Person
        outfile_path = 'media/reports/report_'+str(timezone.now()).split(" ")[0]+'.csv'
        writer = csv.writer(open(outfile_path, 'w'))
        
        headers = []
        for field in model._meta.fields:
        	headers.append(field.name)
        writer.writerow(headers)
        
        for obj in Person.objects.all():
        	row = []
        	for field in headers:
        		val = getattr(obj, field)
        		if callable(val):
        			val = val()
        		#if type(val) == unicode:
                # val = val.encode("utf-8")
        		row.append(val)
        	writer.writerow(row)