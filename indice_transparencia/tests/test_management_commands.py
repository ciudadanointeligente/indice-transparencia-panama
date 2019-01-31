from django.core.management import call_command
from django.test import TestCase
from indice_transparencia.models import (Person, Party, JudiciaryProcessRecord,
                                         WorkRecord, EducationalRecord, Benefit,
                                         Contact, Circuit, Topic,
                                         update_positions_in_ranking,
                                         update_mark_and_position_in_ranking)
from django.utils import timezone
import datetime


class TestManagementCommands(TestCase):
    def test_hay_un_comando_que_calcula_el_mark_y_recalcula_la_wea(self):
        '''
        Jordito manito querido
        Quiero que uno haga:
        ./manage.py recalcula_ranking
        y ocurra chocapic.
        '''
        ### CREANDO DATOS
        pdo = Person.objects.create(name=u'ultima')
        p1 = Person.objects.create(name=u'penultima')
        # Le creo un educational record que suma 2.5 al p1
        EducationalRecord.objects.create(name='Junior de la empresa', institution='FCI', start='04/07/2011', end='31/01/2018', person=p1)
        p2 = Person.objects.create(name=u'Primera')
        # p2 tiene dos tipos de recors que hace que sumen 5 por lo tanto aparecerá más arriba que el resto
        EducationalRecord.objects.create(name='Junior de la empresa', institution='B', start='04/07/2011', end='31/01/2018', person=p2)
        WorkRecord.objects.create(name='Junior de la empresa', institution='FCI', start='04/07/2011', end='31/01/2018', person=p2)
        # deberiamos tener algo que devuelva el ranking

        call_command('recalcula_ranking')
        pdo.refresh_from_db()
        p1.refresh_from_db()
        p2.refresh_from_db()

        assert p2.position_in_ranking == 1
        assert p2.ranking_mark
        assert p1.position_in_ranking == 2
        assert p1.ranking_mark
        assert pdo.position_in_ranking == 3
        assert pdo.ranking_mark == 0

    def test_hay_un_comando_q_envia_un_mail_digest(self):
        p1 = Person.objects.create(name='perrito')
        now = timezone.now()
        una_semana_atras = now - datetime.timedelta(days=7)
        Person.objects.filter(id=p1.id).update(modified=una_semana_atras) ## Esto es un hack!
        p1.refresh_from_db()
        assert p1.modified.day != now.day
        '''Jordito mira eso de arriba es un culo hacerlo y no aporta mucho, además de los
        tests, por eso te lo escribí. Y lo que hace es setearle el modified a 1
        semana atrás a p1.'''
        
        p2 = Person.objects.create(name='gatito')
        
        '''
        Yo creo que hay que crear una clase que tenga dos métodos
        1 que devuelva los candidatos que fueron modificados (context)
        y
        2 que envíe el mail al info@nosequepunto.com con la lista de candidatos
        seleccionados en el método anterior.
        '''
        
        digester = EmailDigest()
        assert p1 not in digester.get_context()
        assert p2 in digester.get_context()
        