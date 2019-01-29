import django_filters
from indice_transparencia.models import Person

class PersonFilter(django_filters.FilterSet):
    
    CHOICES = (
        ('asc','de menor a mayor'), 
        ('desc','de mayor a menor')
        )
    
    ordering = django_filters.ChoiceFilter(label='Puntaje', choices=CHOICES, method='filter_by_order')
    
    class Meta:
        model = Person
        fields = {'circuit', 'party', 'is_deputy'}
        
    def filter_by_order(self, queryset, name, value):
        expression = '-position_in_ranking' if value == 'desc' else 'position_in_ranking'
        
        return queryset.order_by(expression)
        # return queryset
        