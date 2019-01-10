from django.forms import ModelForm
from indice_transparencia.models import Person, Party, JudiciaryProcessRecord, WorkRecord, EducationalRecord, Benefit, Contact

class PersonForm(ModelForm):
    class Meta:
        model = Person
        fields = [ 'image','birth_date', 'web', 'declared_intention_to_transparent', 'party',
                  'circuit', 'period', 'previous_parties', 'reelection', 'extra_education', 'intention_to_transparent_work_plan',
                  'work_plan_link', 'work_plan_doc', 'intention_to_transparent_patrimony', 'patrimony_link', 'patrimony_doc',
                  'existing_interests_declaration', 'interests_link', 'interests_doc', 'judiciary_declaration', 'extra_judiciary_declaration',
                  'judiciary_link', 'judiciary_description', 'reelection', 'benefits', 'benefits_link', 'eth_080_link', 'eth_172_link', 'eth_080_doc',
                  'eth_172_doc']
