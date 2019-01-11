from django.test import TestCase
from indice_transparencia.models import Person, Party
from indice_transparencia.forms import PersonForm
import datetime


class TestFormularios(TestCase):
    def test_crear_un_formulario(self):
        partido = Party.objects.create(name=u'Partido Feroz',
                                       initials='PF')
        data = {
            'birth_date': datetime.date(day=2, month=2, year=2018),
            'image': None,
            'web': 'https://jordipresidente.pa',
            'declared_intention_to_transparent': True,
            'party': partido.id,
            'circuit': 'Panama',
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
        p = Person.objects.create(name=u'Fiera',
                                  specific_type='parlamentario')
        form = PersonForm(instance=p, data=data)
        assert form.is_valid()
        form.save()
        p.refresh_from_db()
        assert p.web
        assert p.birth_date