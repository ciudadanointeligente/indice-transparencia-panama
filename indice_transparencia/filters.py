import django_filters
from indice_transparencia.models import Person

class PersonFilter(django_filters.FilterSet):
    class Meta:
        model = Person
        fields = {'circuit', 'party', 'is_deputy'}