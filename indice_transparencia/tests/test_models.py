from django.test import TestCase
from indice_transparencia.models import (Person, Party, JudiciaryProcessRecord,
                                         WorkRecord, EducationalRecord, Benefit,
                                         Contact, Circuit, Topic,RankingData,
                                         update_positions_in_ranking,
                                         update_mark_and_position_in_ranking)
from django.core import mail
from django.urls import reverse
import datetime
from django.db import transaction
from django.core.management import call_command


class TestModelos(TestCase):

    def test_instanciate_person(self):
        p = Person.objects.create(name=u'Fiera')
        assert p.name == 'Fiera'
        assert hasattr(p, 'name')
        assert hasattr(p, 'email')
        assert hasattr(p, 'web')
        assert hasattr(p, 'party')
        assert hasattr(p, 'circuit')
        assert p.created
        assert p.modified
        assert p.slug
        assert p.ranking_data

    def test_a_person_can_have_a_list_of_fields(self):
        '''El modelo persona puede guardar un arreglo de campos guardados por las voluntarias'''
        p = Person.objects.create(name=u'Fiera', volunteer_changed=['name', 'email'])
        p.refresh_from_db()
        assert len(p.volunteer_changed) == 2

    def test_instanciate_partido(self):
        p = Party.objects.create(name=u'Partido Feroz',
                                 initials='PF')
        assert p.name == 'Partido Feroz'
        assert p.initials == 'PF'
        assert bool(p.slug)

    def test_instanciate_judiciary_record(self):
        p = Person.objects.create(name=u'Fiera')
        record = JudiciaryProcessRecord(number='1-2', date='13/04/2015', kind='judicial', person=p)
        assert record

    def test_instanciate_judiciary_record(self):
        p = Person.objects.create(name=u'Fiera')
        record = JudiciaryProcessRecord(number='1-2', date='13/04/2015', kind='judicial', person=p)
        assert record
        assert record.date

    def test_instanciate_work_record(self):
        p = Person.objects.create(name=u'Fiera')
        record = WorkRecord(name='Junior de la empresa', institution='FCI', start='04/07/2011', end='31/01/2018', person=p)
        assert record
        assert record.start
        assert record.end

    def test_instanciate_educational_record(self):
        p = Person.objects.create(name=u'Fiera')
        record = EducationalRecord(name='Junior de la empresa', institution='FCI', start='04/07/2011', end='31/01/2018', person=p)
        assert record
        assert record.start
        assert record.end

    def test_instanciate_benefit(self):
        p = Person.objects.create(name=u'Fiera')
        b = Benefit.objects.create(name="El beneficio")
        p.benefits.add(b)
        assert p.benefits.count() > 0
        
    def test_instanciate_circuit(self):
        p = Person.objects.create(name=u'Fiera')
        c = Circuit.objects.create(name="9-9")
        p.circuit = c
        assert p.circuit.name == "9-9"
        
    def test_instanciate_topic(self):
        topic = Topic.objects.create(name="tematica")
        assert topic.name == "tematica"
        p = Person.objects.create(name=u'Fiera')
        p.topics.add(topic)
        assert p.topics.count() == 1
        assert p in topic.person_set.all()
        
    def test_instanciate_ranking_data(self):
        p = Person.objects.create(name=u'Fiera')
        EducationalRecord.objects.create(name='Junior de la empresa', institution='FCI', start='04/07/2011', end='31/01/2018', person=p)
        p.update_mark()
        p2 = Person.objects.create(name=u'Fiera2')
        # EducationalRecord.objects.create(name='Junior de la empresa', institution='FCI', start='04/07/2011', end='31/01/2018', person=p2)
        # EducationalRecord.objects.create(name='Junior de la empresa', institution='FCI', start='04/07/2011', end='31/01/2018', person=p2)
        p2.update_mark()
        update_positions_in_ranking()
        
        r1 = RankingData.objects.get(id=p.ranking_data.id)
        assert p.ranking_data.id == r1.id
        assert p.ranking_data.ranking_mark
        assert r1.ranking_mark
        # assert p.ranking_data.position_in_ranking
        assert r1.position_in_ranking == 1
    
    def test_limit_topics_per_person(self):
        p = Person.objects.create(name=u'Fiera')
        t1 = Topic.objects.create(name="t1")
        t2 = Topic.objects.create(name="t2")
        t3 = Topic.objects.create(name="t3")
        t4 = Topic.objects.create(name="t4")
        p.topics.add(t1)
        p.topics.add(t2)
        p.topics.add(t3)
        
        with self.assertRaises(Exception) as e:
            with transaction.atomic():
                p.topics.add(t4)
        assert p.topics.count() == 3
        

class AddingAContactSendsAnEmailWhereCandidatesCanUpdate(TestCase):
    def test_instanciate_contact(self):
        p = Person.objects.create(name=u'Fiera')
        contact = Contact.objects.create(person=p, email='jordi@cidadaniai.org')
        assert contact
        assert contact.identifier

    def test_sends_an_email_every_time_one_is_created(self):
        p = Person.objects.create(name=u'Fiera')
        original_amount_of_mails = len(mail.outbox)
        contact = Contact.objects.create(person=p, email='jordi@cidadaniai.org')
        assert len(mail.outbox) == original_amount_of_mails + 1
        # Se envía un solo email, sólo cuando se crea
        contact.save()
        assert len(mail.outbox) == original_amount_of_mails + 1
        p.refresh_from_db()
        assert p.email == contact.email

    def test_update_url_method(self):
        p = Person.objects.create(name=u'Fiera')
        original_amount_of_mails = len(mail.outbox)
        contact = Contact.objects.create(person=p, email='jordi@cidadaniai.org')
        expected_url = reverse('update-person-data', kwargs={'identifier': contact.identifier})
        assert contact.update_url() == expected_url


class RankingCalculation(TestCase):
    def test_it_calculates_a_mark_not_currently_deputy(self):
        ## querido hermanito Jordi:
        ## Este es para el caso de que no sea un no incumbente, es decir que aún no es electo
        ## Aquí está el test que te calcula toda la volá, recuerda que se pilla en el siguiente link:
        ## https://docs.google.com/spreadsheets/d/1BNHTKEoLTuExGr8v-Ec0_7DE_bdZl36YmblhMeUoJtk/edit#gid=201033095
        ## te quiero.
        p = Person.objects.create(name=u'Fiera')
        ed_record = EducationalRecord.objects.create(name='Junior de la empresa', institution='FCI', start='04/07/2011', end='31/01/2018', person=p)
        p.update_mark()
        assert p.ranking_data.ranking_mark == 5.9, 'en realidad da: ' + str(p.get_mark())
        work_record = WorkRecord(name='Junior de la empresa', institution='FCI', start='04/07/2011', end='31/01/2018', person=p)
        work_record.save()
        p.update_mark()
        assert p.ranking_data.ranking_mark == 11.8, 'en realidad da: ' + str(p.get_mark())
        p.political_proposal_link = 'https://ellinkalprogramapuntocom.com'
        p.update_mark()
        assert p.ranking_data.ranking_mark == 35.3

    def test_person_has_a_update_mark_method(self):
        p = Person.objects.create(name=u'Fiera')
        ed_record = EducationalRecord.objects.create(name='Junior de la empresa', institution='FCI', start='04/07/2011', end='31/01/2018', person=p)
        ed_record.save()
        p.update_mark()
        # p.refresh_from_db()
        assert p.ranking_data.ranking_mark == 5.9, 'en realidad da: ' + str(p.get_mark())

    def test_it_calculates_a_mark_currently_deputy(self):
        p = Person.objects.create(name=u'Fiera', is_deputy=True) ## <======== incumbente por que is_deputy=True
        p.update_mark()
        ed_record = EducationalRecord.objects.create(name='Junior de la empresa', institution='FCI', start='04/07/2011', end='31/01/2018', person=p)
        p.update_mark()
        assert p.ranking_data.ranking_mark == 5.9, 'en realidad da: ' + str(p.get_mark())
        work_record = WorkRecord(name='Junior de la empresa', institution='FCI', start='04/07/2011', end='31/01/2018', person=p)
        work_record.save()
        p.update_mark()
        assert p.ranking_data.ranking_mark == 11.8, 'en realidad da: ' + str(p.get_mark())
        p.political_proposal_link = 'https://ellinkalprogramapuntocom.com'
        p.update_mark()
        assert p.ranking_data.ranking_mark == 35.3, 'en realidad da: ' + str(p.get_mark())
        ## Este es para el caso de que sea un incumbente, es decir que está llendo a la reelección.

    def test_ranking(self):
        pdo = Person.objects.create(name=u'ultima')
        p1 = Person.objects.create(name=u'penultima')
        # Le creo un educational record que suma 2.5 al p1
        EducationalRecord.objects.create(name='Junior de la empresa', institution='FCI', start='04/07/2011', end='31/01/2018', person=p1)
        p2 = Person.objects.create(name=u'Primera')
        # p2 tiene dos tipos de recors que hace que sumen 5 por lo tanto aparecerá más arriba que el resto
        EducationalRecord.objects.create(name='Junior de la empresa', institution='B', start='04/07/2011', end='31/01/2018', person=p2)
        WorkRecord.objects.create(name='Junior de la empresa', institution='FCI', start='04/07/2011', end='31/01/2018', person=p2)
        # deberiamos tener algo que devuelva el ranking
        p1.update_mark()
        p2.update_mark()
        pdo.update_mark()
        update_positions_in_ranking()
        personas = Person.ranking.all()
        assert personas[0] == p2
        assert personas[1] == p1
        assert personas[2] == pdo

    def test_update_position_in_ranking(self):
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

        p1.update_mark()
        p2.update_mark()
        pdo.update_mark()

        ## Ejecuto la funcion

        update_positions_in_ranking()

        pdo.refresh_from_db()
        p1.refresh_from_db()
        p2.refresh_from_db()
        assert p2.ranking_data.position_in_ranking == 1
        assert p1.ranking_data.position_in_ranking == 2
        assert pdo.ranking_data.position_in_ranking == 3

    def test_update_mark_and_position_in_ranking(self):
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
        p2.update_mark()
        pdo.update_mark()

        update_mark_and_position_in_ranking(p1)
        p1.refresh_from_db()
        assert p1.ranking_data.position_in_ranking == 2
    
    def test_deputy_100(self):
        p = Person.objects.create(name=u'Fiera', is_deputy=True)
        EducationalRecord.objects.create(name='Junior de la empresa', institution='FCI', start='04/07/2011', end='31/01/2018', person=p)
        WorkRecord.objects.create(name='Junior de la empresa', institution='FCI', start='04/07/2011', end='31/01/2018', person=p)
        p.political_proposal_link = 'http://perrito.com'
        p.declared_intention_to_transparent_judiciary_records = True
        p.benefits_link = 'http://perrito.com'
        p.eth_001_link = 'http://perrito.com'
        p.eth_002_link = 'http://perrito.com'
        p.eth_080_link = 'http://perrito.com'
        p.eth_172_link = 'http://perrito.com'
        
        p.patrimony_link = 'http://perrito.com'
        p.interests_link = 'http://perrito.com'
        assert p.get_mark() == 100, 'en realidad da: ' + str(p.get_mark())
    
    def test_not_deputy_100(self):
        p = Person.objects.create(name=u'Fiera', is_deputy=False)
        EducationalRecord.objects.create(name='Junior de la empresa', institution='FCI', start='04/07/2011', end='31/01/2018', person=p)
        WorkRecord.objects.create(name='Junior de la empresa', institution='FCI', start='04/07/2011', end='31/01/2018', person=p)
        p.political_proposal_link = 'http://perrito.com'
        p.declared_intention_to_transparent_judiciary_records = True
        p.patrimony_link = 'http://perrito.com'
        p.interests_link = 'http://perrito.com'
        assert p.get_mark() == 100, 'en realidad da: ' + str(p.get_mark())
    
    def test_deputy_55(self):
        p = Person.objects.create(name=u'Fiera',
                                  is_deputy=True,
                                  volunteer_changed=[
                                      'declared_intention_to_transparent_judiciary_records',
                                      'patrimony',
                                      'interests',
                                      'judiciary_records',
                                      'benefits',
                                      'eth_001',
                                      'eth_002',
                                      'eth_080',
                                      'eth_172',
                                        ])
        EducationalRecord.objects.create(name='Junior de la empresa', institution='FCI', start='04/07/2011', end='31/01/2018', person=p)
        WorkRecord.objects.create(name='Junior de la empresa', institution='FCI', start='04/07/2011', end='31/01/2018', person=p)
        p.political_proposal_link = 'http://perrito.com'
        p.declared_intention_to_transparent_judiciary_records = True
        p.benefits_link = 'http://perrito.com'
        p.eth_001_link = 'http://perrito.com'
        p.eth_002_link = 'http://perrito.com'
        p.eth_080_link = 'http://perrito.com'
        p.eth_172_link = 'http://perrito.com'
        
        p.patrimony_link = 'http://perrito.com'
        p.interests_link = 'http://perrito.com'
        assert p.get_mark() == 100, 'en realidad da: ' + str(p.get_mark())
    
    def test_not_deputy_57_5(self):
        p = Person.objects.create(name=u'Fiera', is_deputy=False,
                                  volunteer_changed=[
                                      'declared_intention_to_transparent_judiciary_records',
                                      'patrimony',
                                      'interests',
                                      'political_proposal',
                                      'benefits',
                                      'eth_001',
                                      'eth_002',
                                      'eth_080',
                                      'eth_172',
                                        ])
        EducationalRecord.objects.create(name='Junior de la empresa', institution='FCI', start='04/07/2011', end='31/01/2018', person=p)
        WorkRecord.objects.create(name='Junior de la empresa', institution='FCI', start='04/07/2011', end='31/01/2018', person=p)
        p.political_proposal_link = 'http://perrito.com'
        p.declared_intention_to_transparent_judiciary_records = True
        p.patrimony_link = 'http://perrito.com'
        p.interests_link = 'http://perrito.com'
        assert p.get_mark() == 100, 'en realidad da: ' + str(p.get_mark())