import csv
from django.core.management.base import BaseCommand, CommandError
from indice_transparencia.models import Person, Party, Circuit


class Processor(object):
    def process_row(self, row, printer):
        nombre = row[1]
        
        partido, partido_created = Party.objects.get_or_create(name=row[4])
        
        try:
            circuito = Circuit.objects.get(name=row[0].strip())
        except:
            printer( 'La persona ' + nombre + " NO FUE CREADA por que su circuito no se encontró")
            return
        
        # email = row[5].strip() or None
        twitter = row[5].strip() or None
        facebook = row[6].strip() or None
        instagram = row[8].strip() or None
        web = row[9].strip() or None
        
        #printer(nombre + circuito +partido + email+ twitter+ facebook+instagram+web)
        
        person, person_created= Person.objects.get_or_create(name=nombre, circuit=circuito)
        person.party = partido
        person.twitter = twitter
        person.facebook = facebook
        person.instagram = instagram
        person.web = web
        person.save()
        if person_created:
            printer('Cree a ' + person.name + " en " + str(circuito))
        else:
            printer('Actualicé a ' + person.name + " en " + str(circuito))

    

class Command(BaseCommand):
    help = 'Import candidates from csv file'
    

    def handle(self, *args, **options):
        """ Do your work here """
        self.stdout.write("running load_csv command")
        self.stdout.write("initial person count: " + str(Person.objects.count()))
        self.stdout.write("circuits count: " + str(Circuit.objects.count()))
        with open('candidates.csv', 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            next(reader)
            counter =0
            processor = Processor()
            for row in reader:
                processor.process_row(row, self.stdout.write)
        self.stdout.write("final person count: " + str(Person.objects.count()))
        #('There are {} things!'.format(MyModel.objects.count()))