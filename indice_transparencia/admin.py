from django.contrib import admin
from indice_transparencia.models import (Person, Party, JudiciaryProcessRecord,
                                         WorkRecord, EducationalRecord, Benefit,
                                         Contact, Circuit, Topic,
                                         update_mark_and_position_in_ranking)
from indice_transparencia import normalize_field_name


class ContactAdmin(admin.ModelAdmin):
    list_display = ('person',
                    'email'
                    )
    raw_id_fields = ('person', )

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
        Además, antes de que se calcule el ranking y se guarde la persona, se ven cuales son los campos modificados
        y se agregan al campo volunteer_changed.
        Se debe hacer un truco diferente para los inlines, este sólo funciona para los campos planos,
        es decir, no para los inlines.
        '''
        ## Esto es una marquita para entender el flujo
        # print('save_model')
        for field_name in form.changed_data:
            field_name = normalize_field_name(field_name)
            if field_name not in obj.volunteer_changed:
                obj.volunteer_changed.append(field_name)
        super().save_model(request, obj, form, change)
        

    def save_formset(self, request, form, formset, change):
        '''
        Jordito: mira acá se hace el mismo truco para los inlines.
        qué es qué aquí:
        * formset es el inline, y formset_prefix es el nombre que le damos en la base de datos.
        Por ejemplo: judiciary_records, work_records o educational_records.

        * form.instance es la persona.
        * formset.has_changed() me dice si la wea cambió o no cambió.
        '''
        ## Esto es una marquita para entender el flujo
        # print('save_formset')
        field_name = formset.prefix
        field_name = normalize_field_name(field_name)
        if formset.has_changed() and field_name not in form.instance.volunteer_changed:
            form.instance.volunteer_changed.append(field_name)
        super().save_formset(request, form, formset, change)

    def save_related(self, request, form, formsets, change):
        '''En este se hace el calculo del ranking.
        Esto es por que en el super() de la clase superior se hace un for
        sobre todos los inlines.
        Pero después del super está todo bien.'''
        super().save_related(request, form, formsets, change)
        ## Esto es una marquita para entender el flujo
        # print('save_related')
        update_mark_and_position_in_ranking(form.instance)

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