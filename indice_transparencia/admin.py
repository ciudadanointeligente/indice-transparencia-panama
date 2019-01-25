from django.contrib import admin
from indice_transparencia.models import (Person, Party, JudiciaryProcessRecord,
                                         WorkRecord, EducationalRecord, Benefit,
                                         Contact, Circuit, Topic,
                                         update_mark_and_position_in_ranking)


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
    exclude = ('extra_education',)

    inlines = [
        EducationalRecordInline,
        WorkRecordInline,
        JudiciaryProcessRecordInline,

    ]
    def save_model(self, request, obj, form, change):
        '''
        Jordito querido mi corazón
        acá se recalcula el ranking y la mark cuando un voluntario crea la wea
        '''
        super().save_model(request, obj, form, change)
        update_mark_and_position_in_ranking(obj)

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