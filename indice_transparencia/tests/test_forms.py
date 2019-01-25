from django.test import TestCase
from indice_transparencia.models import Person, Party, Circuit, Topic
from indice_transparencia.forms import PersonForm, EducationalRecordForm
import datetime


class TestFormularios(TestCase):
    def test_crear_un_formulario(self):
        partido = Party.objects.create(name=u'Partido Feroz',
                                       initials='PF')
        
        circuit = Circuit.objects.create(name=u'1-1')
        data = {
            'birth_date': datetime.date(day=2, month=2, year=2018),
            'image': None,
            'web': 'https://jordipresidente.pa',
            'declared_intention_to_transparent': True,
            'party': partido.id,
            'circuit': circuit.id,
            'period': '2018',
            'previous_parties': [],
            'reelection': True,
            'extra_education': 'Me gusta educarme',
            'intention_to_transparent_work_plan': True,
            'work_plan_link': 'https://jordipresidente.pa/transparencia',
            'work_plan_doc': None,
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
            'eth_172_doc': None
        }
        p = Person.objects.create(name=u'Fiera')
        form = PersonForm(instance=p, data=data)
        assert form.is_valid()
        form.save()
        p.refresh_from_db()
        assert p.web
        assert p.birth_date

    def test_form_topics_limit(self):
        topic1 = Topic.objects.create(name="tematica1")
        topic2 = Topic.objects.create(name="tematica2")
        topic3 = Topic.objects.create(name="tematica3")
        topic4 = Topic.objects.create(name="tematica4")
        partido = Party.objects.create(name=u'Partido Feroz',
                                       initials='PF')
        
        circuit = Circuit.objects.create(name=u'1-1')
        data = {
            'birth_date': datetime.date(day=2, month=2, year=2018),
            'image': None,
            'web': 'https://jordipresidente.pa',
            'declared_intention_to_transparent': True,
            'party': partido.id,
            'circuit': circuit.id,
            'period': '2018',
            'previous_parties': [],
            'reelection': True,
            'extra_education': 'Me gusta educarme',
            'intention_to_transparent_work_plan': True,
            'work_plan_link': 'https://jordipresidente.pa/transparencia',
            'work_plan_doc': None,
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
            'topics': [topic1.id,topic2.id,topic3.id,topic4.id,]
        }
        p = Person.objects.create(name=u'Fiera')
        form = PersonForm(instance=p, data=data)
        assert not form.is_valid()

    def test_cuando_se_guarda_el_formulrio_recalcula_el_mark_y_su_ranking(self):
        partido = Party.objects.create(name=u'Partido Feroz',
                                       initials='PF')
        
        circuit = Circuit.objects.create(name=u'1-1')
        data = {
            'birth_date': datetime.date(day=2, month=2, year=2018),
            'image': None,
            'web': 'https://jordipresidente.pa',
            'declared_intention_to_transparent': True,
            'party': partido.id,
            'circuit': circuit.id,
            'period': '2018',
            'previous_parties': [],
            'reelection': True,
            'extra_education': 'Me gusta educarme',
            'intention_to_transparent_work_plan': True,
            'work_plan_link': 'https://jordipresidente.pa/transparencia',
            'work_plan_doc': None,
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
            'eth_172_doc': None
        }
        p = Person.objects.create(name=u'Fiera')
        form = PersonForm(instance=p, data=data)
        assert form.is_valid()
        form.save()
        p.refresh_from_db()
        
        assert p.position_in_ranking is not None
        assert p.ranking_mark is not None

        assert p.ranking_mark
        assert p.position_in_raking

class EducationalRecordFormsTestCase(TestCase):
    def test_create_a_educational_record(self):
        p = Person.objects.create(name=u'Fiera')
        data = {
            'name': "Postgrado en flojeo",
            'institution': 'Fundacao cidadania inteligente',
            'start': '2011',
            'end': '2013',
        }
        form = EducationalRecordForm(person=p, data=data)
        assert form.is_valid()
        record = form.save()
        assert record.person == p
        assert record.name
        assert record.institution
        assert record.start
        assert record.end