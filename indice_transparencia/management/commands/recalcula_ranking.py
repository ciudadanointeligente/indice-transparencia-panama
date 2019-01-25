from django.core.management.base import BaseCommand, CommandError
from indice_transparencia.models import Person, update_positions_in_ranking


class Command(BaseCommand):
    help = 'Recalcula las notas y el ranking de los candidatos'
    
    def handle(self, *args, **options):
        """ Do your work here """
        self.stdout.write("Recalculando Ranking")
        for p in Person.objects.all():
            p.update_mark()

        update_positions_in_ranking()