from django.contrib import admin
from indice_transparencia.models import Person, Party, JudiciaryProcessRecord, WorkRecord, EducationalRecord, Benefit, Contact, Circuit


class ContactAdmin(admin.ModelAdmin):
    pass

admin.site.register(Contact, ContactAdmin)

class PartyAdmin(admin.ModelAdmin):
    pass
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
    inlines = [
        EducationalRecordInline,
        WorkRecordInline,
        JudiciaryProcessRecordInline,

    ]
admin.site.register(Person, PersonAdmin)

class CircuitAdmin(admin.ModelAdmin):
    pass

admin.site.register(Circuit, CircuitAdmin)