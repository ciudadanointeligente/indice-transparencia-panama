import pytest
from indice_transparencia.models import Person

pytestmark = pytest.mark.django_db

@pytest.mark.django_db
class TestPerrito(object):
    pytestmark = pytest.mark.django_db

    def test_perrito(self):
        p = Person.objects.create(name=u'Fiera',
                                  specific_type='parlamentario')
        assert p.name == 'Fiera'
        assert p.specific_type == 'parlamentario'
