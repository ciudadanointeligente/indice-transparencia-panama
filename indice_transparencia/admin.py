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