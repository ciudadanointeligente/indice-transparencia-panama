from django.forms import ModelForm
from django import forms
from indice_transparencia.models import (Person, Party, JudiciaryProcessRecord, WorkRecord, EducationalRecord,
                                         Benefit, Contact)
from django.core.exceptions import ValidationError
from indice_transparencia import normalize_field_name

class PersonForm(ModelForm):
    class Meta:
        model = Person
        fields = [ 'image','birth_date','web','twitter','instagram','facebook','declared_intention_to_transparent_political_profile',
                   'party','circuit','has_changed_party','previous_parties','declared_intention_to_transparent_education',
                #   'extra_education',
                   'declared_intention_to_transparent_work','declared_intention_to_transparent_political_proposal','has_political_proposal',
                   'political_proposal_link','political_proposal_doc','intention_to_transparent_patrimony','existing_patrimony_declaration',
                   'patrimony_link','patrimony_doc','existing_interests_declaration','interests_link','interests_doc',
                   'declared_intention_to_transparent_judiciary_records','judiciary_processes_involved',
                   'extra_judiciary_declaration','judiciary_link','judiciary_description','is_deputy','declared_intention_to_transparent_public_resources_usage',
                   'benefits','benefits_link','benefits_doc',
                #   'intention_to_transparent_work_plan','work_plan_link', 'work_plan_doc',
                   'eth_001_link','eth_001_doc','eth_002_link','eth_002_doc','eth_080_link','eth_080_doc','eth_172_link','eth_172_doc','attendance',
                   'laws_worked_on','topics', 'other_topic']
        # widgets = {
        #     'birth_date': forms.DateInput(attrs={'class':'datepicker'}),
        # }

    def clean(self):
        cleaned_data = super(PersonForm, self).clean()
        if len(self.cleaned_data['topics']) > 3:
            raise forms.ValidationError({'topics':'No se puede tener más de 3 temas'})
        return cleaned_data
        
    def save(self, commit=False):
        person = super(PersonForm, self).save(commit=True)
        person.volunteer_changed = []
        return person


class EducationalRecordForm(ModelForm):
    class Meta:
        model = EducationalRecord
        fields = ['name', 'institution', 'start', 'end']

    def __init__(self, *args, **kwargs):
        self.person = kwargs.pop('person')
        super(EducationalRecordForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        record = super(EducationalRecordForm, self).save(commit=False)
        record.person = self.person
        if commit:
            record.save()
        return record
