from django.test import TestCase
from indice_transparencia.models import Person, Party
from indice_transparencia.filters import PersonFilter

class PersonFilterTestCase(TestCase):
    def setUp(self):
        super(PersonFilterTestCase, self).setUp()
        self.party_1 = Party.objects.create(name='party1')
        self.party_2 = Party.objects.create(name='party2')
        self.person_1 = Person.objects.create(name='person1', party=self.party_1)
        self.person_2 = Person.objects.create(name='person2', party=self.party_2)
        self.person_3 = Person.objects.create(name='person3', party=self.party_2)
    
    def test_filter_with_party(self):
        data = {'party': self.party_1.id}
        f = PersonFilter(data=data)
        self.assertIn(self.person_1, f.qs)
        self.assertNotIn(self.person_2, f.qs)
        self.assertNotIn(self.person_3, f.qs)