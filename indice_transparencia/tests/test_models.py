from django.test import TestCase
from indice_transparencia.models import Person, Party, JudiciaryProcessRecord, WorkRecord, EducationalRecord, Benefit, Contact
from django.core import mail
from django.urls import reverse
import datetime


class TestModelos(TestCase):

    def test_instanciate_person(self):
        p = Person.objects.create(name=u'Fiera',
                                  specific_type='parlamentario')
        assert p.name == 'Fiera'
        assert p.specific_type == 'parlamentario'
        assert hasattr(p, 'name')
        assert hasattr(p, 'email')
        assert hasattr(p, 'web')
        assert hasattr(p, 'party')
        assert hasattr(p, 'circuit')
        assert hasattr(p, 'period')
        assert hasattr(p, 'reelection')
        assert p.slug

    def test_instanciate_partido(self):
        p = Party.objects.create(name=u'Partido Feroz',
                                 initials='PF')
        assert p.name == 'Partido Feroz'
        assert p.initials == 'PF'
        assert bool(p.slug)

    def test_instanciate_judiciary_record(self):
        p = Person.objects.create(name=u'Fiera',
                                  specific_type='parlamentario')
        record = JudiciaryProcessRecord(number='1-2', date='13/04/2015', kind='judicial', person=p)
        assert record

    def test_instanciate_judiciary_record(self):
        p = Person.objects.create(name=u'Fiera',
                                  specific_type='parlamentario')
        record = JudiciaryProcessRecord(number='1-2', date='13/04/2015', kind='judicial', person=p)
        assert record
        assert record.date

    def test_instanciate_work_record(self):
        p = Person.objects.create(name=u'Fiera',
                                  specific_type='parlamentario')
        record = WorkRecord(name='Junior de la empresa', institution='FCI', start='04/07/2011', end='31/01/2018', person=p)
        assert record
        assert record.start
        assert record.end

    def test_instanciate_educational_record(self):
        p = Person.objects.create(name=u'Fiera',
                                  specific_type='parlamentario')
        record = EducationalRecord(name='Junior de la empresa', institution='FCI', start='04/07/2011', end='31/01/2018', person=p)
        assert record
        assert record.start
        assert record.end

    def test_instanciate_benefit(self):
        p = Person.objects.create(name=u'Fiera',
                                  specific_type='parlamentario')
        b = Benefit.objects.create(name="El beneficio")
        p.benefits.add(b)
        assert p.benefits.count() > 0


class AddingAContactSendsAnEmailWhereCandidatesCanUpdate(TestCase):
    def test_instanciate_contact(self):
        p = Person.objects.create(name=u'Fiera',
                                  specific_type='parlamentario')
        contact = Contact.objects.create(person=p, email='jordi@cidadaniai.org')
        assert contact
        assert contact.identifier

    def test_sends_an_email_every_time_one_is_created(self):
        p = Person.objects.create(name=u'Fiera',
                                  specific_type='parlamentario')
        original_amount_of_mails = len(mail.outbox)
        contact = Contact.objects.create(person=p, email='jordi@cidadaniai.org')
        assert len(mail.outbox) == original_amount_of_mails + 1
        # Se envía un solo email, sólo cuando se crea
        contact.save()
        assert len(mail.outbox) == original_amount_of_mails + 1
        p.refresh_from_db()
        assert p.email == contact.email

    def test_update_url_method(self):
        p = Person.objects.create(name=u'Fiera',
                                  specific_type='parlamentario')
        original_amount_of_mails = len(mail.outbox)
        contact = Contact.objects.create(person=p, email='jordi@cidadaniai.org')
        expected_url = reverse('update-person-data', kwargs={'identifier': contact.identifier})
        assert contact.update_url() == expected_url


class RankingCalculation(TestCase):
    def test_it_calculates_a_mark(self):
        p = Person.objects.create(name=u'Fiera',
                                  specific_type=u'candidato',
                                  birth_date=datetime.date(day=2, month=2, year=2012))
        assert p.mark == 2012

    def test_ranking(self):
        pdo = Person.objects.create(name=u'ultima',
                                     specific_type=u'candidato')
        p1 = Person.objects.create(name=u'penultima',
                                     specific_type=u'candidato',
                                     birth_date=datetime.date(day=2, month=2, year=2012))
        p2 = Person.objects.create(name=u'Primera',
                                     specific_type=u'candidato',
                                     birth_date=datetime.date(day=2, month=2, year=2014))
        # deberiamos tener algo que devuelva el ranking
        personas = Person.ranking.all()
        assert personas[0] == p2
        assert personas[1] == p1
        assert personas[2] == pdo
