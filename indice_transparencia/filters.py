import django_filters
from indice_transparencia.models import Person

class PersonFilter(django_filters.FilterSet):

    CHOICES = (
        ('desc','de menor a mayor'),
        ('asc','de mayor a menor')
        )

    ordering = django_filters.ChoiceFilter(label='Ordenar según puntaje en índice de transparencia', choices=CHOICES, method='filter_by_order')

    class Meta:
        model = Person
        fields = {'circuit', 'party', 'is_deputy'}

    def filter_by_order(self, queryset, name, value):
        expression = '-ranking_data__position_in_ranking' if value == 'desc' else 'ranking_data__position_in_ranking'

        return queryset.order_by(expression)
        # return queryset
