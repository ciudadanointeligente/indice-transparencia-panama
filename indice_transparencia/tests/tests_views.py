from django.test import TestCase
from indice_transparencia.models import Person, Party, Contact, Circuit, EducationalRecord, WorkRecord
from indice_transparencia.forms import PersonForm
from django.urls import reverse
from django.core.management import call_command
import datetime

class IndexViewTestCase(TestCase):
    def test_get_the_index(self):
        url = reverse('index')
        response = self.client.get(url)
        assert response.status_code == 200
        
class AboutViewTestCase(TestCase):
    def test_get_the_about_page(self):
        url = reverse('about')
        response = self.client.get(url)
        assert response.status_code == 200

class ProfileViewTestCase(TestCase):
    def test_get_the_index(self):
        p = Person.objects.create(name=u'Fiera')
        url = reverse('candidate-profile', kwargs={'slug': p.slug})
        response = self.client.get(url)
        assert response.status_code == 200
    
    def test_get_absolute_url(self):
        p = Person.objects.create(name=u'Fiera')
        url = reverse('candidate-profile', kwargs={'slug': p.slug})
        assert p.get_absolute_url() == url


class PersonUpdateView(TestCase):
    def test_get_the_view(self):
        p = Person.objects.create(name=u'Fiera')
        contact = Contact.objects.create(person=p, email='jordi@cidadaniai.org')
        url = reverse('update-person-data', kwargs={'identifier': contact.identifier})
        response = self.client.get(url)
        form = response.context['form']
        assert form.instance == p
        assert isinstance(form, PersonForm)

    def test_post_to_the_view(self):
        partido = Party.objects.create(name=u'Partido Feroz',
                                       initials='PF')
        circuit = Circuit.objects.create(name=u'1-1')
        p = Person.objects.create(name=u'Fiera')
        contact = Contact.objects.create(person=p, email='jordi@cidadaniai.org')
        url = reverse('update-person-data', kwargs={'identifier': contact.identifier})
        data = {
            'birth_date': str(datetime.date(year=2019, day=2, month=2)),
            'image': None,
            'web': 'https://jordipresidente.pa',
            'declared_intention_to_transparent': True,
            'party': partido.id,
            'circuit': circuit.id,
            'period': '2018',
            'previous_parties': [],
            'reelection': True,
            'extra_education': 'Me gusta educarme',
            # 'intention_to_transparent_work_plan': True,
            # 'work_plan_link': 'https://jordipresidente.pa/transparencia',
            # 'work_plan_doc': None,
            'intention_to_transparent_patrimony': True,
            'patrimony_link': 'https://jordipresidente.pa/transparencia',
            'patrimony_doc': None,
            'existing_interests_declaration': True,
            'interests_link': 'https://jordipresidente.pa/transparencia',
            'interests_doc': None,
            'judiciary_declaration': True,
            'extra_judiciary_declaration': 'No tengo nada!!!',
            'judiciary_link': 'https://jordipresidente.pa/transparencia',
            'judiciary_description': 'Judiciary',
            'benefits': [],
            'benefits_link': 'https://jordipresidente.pa/transparencia',
            'eth_080_link': 'https://jordipresidente.pa/transparencia',
            'eth_172_link': 'https://jordipresidente.pa/transparencia',
            'eth_080_doc': None,
            'eth_172_doc': None,
            'educational_records-TOTAL_FORMS': 2,
            'educational_records-INITIAL_FORMS': 0,
            'educational_records-MIN_NUM_FORMS': 0,
            'educational_records-MAX_NUM_FORMS': 1000,
            'educational_records-0-name': "Postgrado en flojeo",
            'educational_records-0-institution': 'Fundacao cidadania inteligente',
            'educational_records-0-start': '2011',
            'educational_records-0-end': '2013',
            'educational_records-1-name': "Master en flojeo",
            'educational_records-1-institution': 'Fundacao cidadania inteligente',
            'educational_records-1-start': '2011',
            'educational_records-1-end': '2013',
            # work_records
            'work_records-TOTAL_FORMS': 1,
            'work_records-INITIAL_FORMS': 0,
            'work_records-MIN_NUM_FORMS': 0,
            'work_records-MAX_NUM_FORMS': 1000,
            'work_records-0-name': "Postgrado en flojeo",
            'work_records-0-institution': 'Fundacao cidadania inteligente',
            'work_records-0-start': '2011',
            'work_records-0-end': '2013',
            # judiciary
            'judiciary_records-TOTAL_FORMS': 1,
            'judiciary_records-INITIAL_FORMS': 0,
            'judiciary_records-MIN_NUM_FORMS': 0,
            'judiciary_records-MAX_NUM_FORMS': 1000,
            'judiciary_records-0-number': "1 raya cuatro",
            'judiciary_records-0-date': str(datetime.date(year=2019, day=2, month=2)),
            'judiciary_records-0-kind': 'penal',
            'judiciary_records-0-result': 'pagué mi condena!',
            
            
        }
        response = self.client.post(url, data=data)
        assert response.status_code in [200, 302]
        call_command('recalcula_ranking')
        p.refresh_from_db()
        assert p.web
        assert p.educational_records.count() == 2
        assert p.work_records.count() == 1
        assert p.judiciary_records.count() == 1

        assert p.position_in_ranking is not None
        assert p.ranking_mark is not None

        assert p.ranking_mark
        assert p.position_in_ranking


    def test_it_removes_fields_from_volunteers_changed(self):
        partido = Party.objects.create(name=u'Partido Feroz',
                                       initials='PF')
        circuit = Circuit.objects.create(name=u'1-1')
        p = Person.objects.create(name=u'Fiera',
                                  volunteer_changed=['birth_date', ## Esta wea va a cambiar por que el candidato la seleccionará
                                                    'web', ## Esta wea va a cambiar por que el candidato la seleccionará
                                                    'judiciary_records', ## Esta wea va a cambiar por que el candidato la seleccionará,
                                                    'eth_080', ## A pesar que sólo está mandando el eth_080_link esto se borrará
                                                    'image', ## Esta wea NOOOOOO va a cambiar por que el candidato la seleccionará
                                                    ])
        contact = Contact.objects.create(person=p, email='jordi@cidadaniai.org')
        url = reverse('update-person-data', kwargs={'identifier': contact.identifier})
        data = {
            'birth_date': str(datetime.date(year=2019, day=2, month=2)),
            'image': None,
            'web': 'https://jordipresidente.pa',
            'declared_intention_to_transparent': True,
            'party': partido.id,
            'circuit': circuit.id,
            'period': '2018',
            'previous_parties': [],
            'reelection': True,
            'extra_education': 'Me gusta educarme',
            # 'intention_to_transparent_work_plan': True,
            # 'work_plan_link': 'https://jordipresidente.pa/transparencia',
            # 'work_plan_doc': None,
            'intention_to_transparent_patrimony': True,
            'patrimony_link': 'https://jordipresidente.pa/transparencia',
            'patrimony_doc': None,
            'existing_interests_declaration': True,
            'interests_link': 'https://jordipresidente.pa/transparencia',
            'interests_doc': None,
            'judiciary_declaration': True,
            'extra_judiciary_declaration': 'No tengo nada!!!',
            'judiciary_link': 'https://jordipresidente.pa/transparencia',
            'judiciary_description': 'Judiciary',
            'benefits': [],
            'benefits_link': 'https://jordipresidente.pa/transparencia',
            'eth_080_link': 'https://jordipresidente.pa/transparencia',
            'eth_172_link': 'https://jordipresidente.pa/transparencia',
            'eth_080_doc': None,
            'eth_172_doc': None,
            ## Jordi Atento aquí!! 
            ## Acá yo sólo dejé los judiciary_records con datos válidos.
            ## Los otros están vacíos
            'educational_records-TOTAL_FORMS': 2,
            'educational_records-INITIAL_FORMS': 0,
            'educational_records-MIN_NUM_FORMS': 0,
            'educational_records-MAX_NUM_FORMS': 1000,
            'educational_records-0-name': "",
            'educational_records-0-institution': '',
            'educational_records-0-start': '',
            'educational_records-0-end': '',
            'educational_records-1-name': "",
            'educational_records-1-institution': '',
            'educational_records-1-start': '',
            'educational_records-1-end': '',
            # work_records
            'work_records-TOTAL_FORMS': 1,
            'work_records-INITIAL_FORMS': 0,
            'work_records-MIN_NUM_FORMS': 0,
            'work_records-MAX_NUM_FORMS': 1000,
            'work_records-0-name': "",
            'work_records-0-institution': '',
            'work_records-0-start': '',
            'work_records-0-end': '',
            # judiciary
            'judiciary_records-TOTAL_FORMS': 1,
            'judiciary_records-INITIAL_FORMS': 0,
            'judiciary_records-MIN_NUM_FORMS': 0,
            'judiciary_records-MAX_NUM_FORMS': 1000,
            'judiciary_records-0-number': "1 raya cuatro",
            'judiciary_records-0-date': str(datetime.date(year=2019, day=2, month=2)),
            'judiciary_records-0-kind': 'penal',
            'judiciary_records-0-result': 'pagué mi condena!',
            
            
        }
        response = self.client.post(url, data=data)
        p.refresh_from_db()
        assert 'image' in p.volunteer_changed
        assert 'birth_date' not in p.volunteer_changed
        assert 'web' not in p.volunteer_changed
        assert 'judiciary_records' not in p.volunteer_changed
        assert 'eth_080' not in p.volunteer_changed


class RankingListViweTestCase(TestCase):
    def test_get_the_list(self):
        url = reverse('ranking')
        response = self.client.get(url)
        assert response.status_code == 200
        
    def test_the_list_has_several_persons(self):
        p1 = Person.objects.create(name="perro")
        # Perro aún está bien atrás y mark devuelve 0
        p2 = Person.objects.create(name="gato")
        # Gato sólo tiene un tipo de record por lo que sólo suma 2.5
        EducationalRecord.objects.create(name='Junior de la empresa', institution='B', start='04/07/2011', end='31/01/2018', person=p2)
        p3 = Person.objects.create(name="chimuelo")
        # Chimuelo tiene dos tipos de recors que hace que sumen 5 por lo tanto aparecerá más arriba que el resto
        EducationalRecord.objects.create(name='Junior de la empresa', institution='B', start='04/07/2011', end='31/01/2018', person=p3)
        WorkRecord.objects.create(name='Junior de la empresa', institution='FCI', start='04/07/2011', end='31/01/2018', person=p3)

        call_command('recalcula_ranking')
        url = reverse('ranking')
        response = self.client.get(url)
        persons = response.context['persons']
        assert len(persons) == 3
        assert p1 in persons
        # assert p3 == persons[0]
        