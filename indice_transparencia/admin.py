from django.contrib import admin
from indice_transparencia.models import (Person, Party, JudiciaryProcessRecord,
                                         WorkRecord, EducationalRecord, Benefit,
                                         Contact, Circuit, Topic)


class ContactAdmin(admin.ModelAdmin):
    list_display = ('person',
                    'email'
                    )

admin.site.register(Contact, ContactAdmin)

class PartyAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'initials'
                    )
admin.site.register(Party, PartyAdmin)

class BenefitAdmin(admin.ModelAdmin):
    pass
admin.site.register(Benefit, BenefitAdmin)

class WorkRecordInline(admin.TabularInline):
    model = WorkRecord

class JudiciaryProcessRecordInline(admin.TabularInline):
    model = JudiciaryProcessRecord


class EducationalRecordInline(admin.TabularInline):
    model = EducationalRecord

class PersonAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'party',
                    'circuit'
                    )
    search_fields = ['name', 'party__name', 'circuit__name', 'circuit__province', 'circuit__district']
    fields = ('name','birth_date','email','web','twitter','instagram','facebook','image','declared_intention_to_transparent_political_profile','party','circuit','has_changed_party','previous_parties','topics','declared_intention_to_transparent_education','extra_education','declared_intention_to_transparent_work','declared_intention_to_transparent_political_proposal','has_political_proposal','political_proposal_link','political_proposal_doc','intention_to_transparent_patrimony','existing_patrimony_declaration','patrimony_link','patrimony_doc','existing_interests_declaration','interests_link','interests_doc','declared_intention_to_transparent_judiciary_records','judiciary_processes_involved','extra_judiciary_declaration','judiciary_link','judiciary_description','is_deputy','declared_intention_to_transparent_public_resources_usage','benefits','benefits_link','benefits_doc','intention_to_transparent_work_plan','work_plan_link','work_plan_doc','eth_001_link','eth_001_doc','eth_002_link','eth_002_doc','eth_080_link','eth_080_doc','eth_172_link','eth_172_doc','attendance','laws_worked_on')

    inlines = [
        EducationalRecordInline,
        WorkRecordInline,
        JudiciaryProcessRecordInline,

    ]
admin.site.register(Person, PersonAdmin)

class CircuitAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'province',
                    'district'
                    )

admin.site.register(Circuit, CircuitAdmin)


class TopicAdmin(admin.ModelAdmin):
    pass
admin.site.register(Topic, TopicAdmin)