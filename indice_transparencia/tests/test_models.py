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
        assert hasattr(p, 'name')
        assert hasattr(p, 'gender')
        assert hasattr(p, 'birth_date')
        assert hasattr(p, 'email')
        assert hasattr(p, 'web')
        assert hasattr(p, 'party')
        assert hasattr(p, 'circuit')
        assert hasattr(p, 'period')
        assert hasattr(p, 'reelection')
        assert hasattr(p, 'cv_educ')
        assert hasattr(p, 'cv_educ_detail')
        assert hasattr(p, 'cv_experpro')
        assert hasattr(p, 'cv_experpro_detail')
        assert hasattr(p, 'cv_experpol')
        assert hasattr(p, 'cv_experpol_detail')
        assert hasattr(p, 'cv_transfu')
        assert hasattr(p, 'wor_attendance')
        assert hasattr(p, 'wor_proposals')
        assert hasattr(p, 'wor_vote')
        assert hasattr(p, 'eth_080')
        assert hasattr(p, 'eth_080_link')
        assert hasattr(p, 'eth_172')
        assert hasattr(p, 'eth_172_link')
        assert hasattr(p, 'eth_trav_N')
        assert hasattr(p, 'eth_trav_exp')
        assert hasattr(p, 'eth_trav_link')
        assert hasattr(p, 'eth_exo')
        assert hasattr(p, 'eth_exo_link')
