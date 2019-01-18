from django.db import models
from autoslug import AutoSlugField
import uuid
from templated_email import send_templated_mail
from django.contrib.sites.models import Site
from django.conf import settings
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.db.models.signals import m2m_changed


class Party(models.Model):
    name = models.CharField(max_length=255, verbose_name=u"Nombre")
    initials = models.CharField(max_length=255, verbose_name=u"Iniciales")
    slug = AutoSlugField(populate_from='name', null=True)
    image = models.ImageField(verbose_name=u"Logo del partido", upload_to='party_logos/%Y/%m/%d/',
                                     null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Partido"
        
class Circuit(models.Model):
    name = models.CharField(max_length=255, verbose_name=u"Nombre", null=True)
    province = models.CharField(max_length=255, verbose_name=u"Provincia", default="", null=True, blank=True)
    district = models.CharField(max_length=255, verbose_name=u"Distritos", default="", null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Circuito"
        
class Topic(models.Model):
    name = models.CharField(max_length=255, verbose_name=u"Nombre", null=True)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Tema Prioritario"


class EducationalRecord(models.Model):
    name = models.CharField(max_length=255, verbose_name=u"Nombre Programa")
    institution = models.CharField(max_length=255, verbose_name=u"Institución")
    start = models.CharField(max_length=255, verbose_name=u"Fecha de ingreso")
    end = models.CharField(max_length=255, verbose_name=u"Fecha de término")
    person = models.ForeignKey('Person', on_delete=models.CASCADE, related_name="educational_records", null=True)


class WorkRecord(models.Model):
    name = models.CharField(max_length=255, verbose_name=u"Cargo")
    institution = models.CharField(max_length=255, verbose_name=u"Institución")
    start = models.CharField(max_length=255, verbose_name=u"Fecha de ingreso")
    end = models.CharField(max_length=255, verbose_name=u"Fecha de término")
    person = models.ForeignKey('Person', on_delete=models.CASCADE, related_name="work_records", null=True)


class JudiciaryProcessRecord(models.Model):
    number = models.CharField(max_length=255, verbose_name=u"Número")
    date = models.DateField(max_length=255, verbose_name=u"Fecha")
    kind = models.CharField(max_length=255, verbose_name=u"Tipo")
    result = models.TextField(max_length=255, verbose_name=u"Fallo")
    person = models.ForeignKey('Person', on_delete=models.CASCADE, related_name="judiciary_records", null=True)


class Benefit(models.Model):
    name = models.CharField(max_length=255, verbose_name='Nombre del beneficio')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Beneficio"

class RankingManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        return sorted(qs.all(),  key=lambda m: m.mark, reverse=True)

TYPES_OF_PERSON = (('parlamentario', 'Parlamentario'), ('candidato', 'Candidato'), )


class Person(models.Model):
    #datos personales
    name = models.CharField(max_length=255, verbose_name=u"Nombre Completo")
    birth_date = models.DateField(verbose_name=u"Fecha de nacimiento", null=True, blank=True)
    email = models.EmailField(verbose_name=u"Correo electrónico de contacto", null=True, blank=True)
    web = models.URLField(max_length=512, verbose_name=u"Link al sitio web personal (o cuenta oficial en redes sociales)", null=True, blank=True)
    twitter = models.URLField(max_length=255, verbose_name=u"Cuenta de twitter", null=True, blank=True)
    instagram = models.URLField(max_length=255, verbose_name=u"Cuenta de instagram", null=True, blank=True)
    facebook = models.URLField(max_length=255, verbose_name=u"Cuenta de facebook", null=True, blank=True)
    image = models.ImageField(verbose_name=u"Foto para tu perfil", upload_to='profile_images/%Y/%m/%d/',
                                     null=True, blank=True)
    
    #perfil político
    declared_intention_to_transparent_political_profile = models.BooleanField(default=False, verbose_name=u"¿Desea Ud. compartir información sobre sus afiliaciones políticas?", blank=True)
    party = models.ForeignKey(Party, null=True, on_delete=models.SET_NULL, related_name="persons", blank=True, verbose_name=u"Partido político o movimiento al que representa")
    circuit = models.ForeignKey(Circuit, null=True, on_delete=models.SET_NULL, related_name="persons", blank=True, verbose_name=u"Circuito al que representa o busca representar")
    has_changed_party = models.BooleanField(default=False, verbose_name=u"¿Ha pertenecido ud. a otros partidos o movimientos políticos?", blank=True)
    previous_parties = models.ManyToManyField(Party, related_name="ex_members", verbose_name=u"Si respondió \"sí\", seleccione a qué otros partidos ha pertenecido en el pasado", blank=True)    
    topics = models.ManyToManyField(Topic, related_name="person_set", blank=True, verbose_name="Por favor indique los tres temas o problemáticas en las que le gustaría enfocarse durante su gestión (2019-2024).")
    
    #formación académica
    declared_intention_to_transparent_education = models.BooleanField(default=False, verbose_name=u"¿Desea Ud. compartir información sobre su formación/educación?", blank=True)
    extra_education = models.TextField(max_length=1024,
                                       null=True,
                                       verbose_name=u"¿Desea compartir alguna otra experiencia relevante de formación? Puede escribirlas a continuación:", blank=True)
    
    
    
    #experiencia_profesional
    declared_intention_to_transparent_work = models.BooleanField(default=False, verbose_name=u"¿Desea Ud. compartir información sobre su experiencia laboral?", blank=True)
    
    
    
    #propuesta polítical
    declared_intention_to_transparent_political_proposal = models.BooleanField(default=False, verbose_name=u"¿Desea Ud. compartir su propuesta política de diputado(a) o candidato(a)?", blank=True)
    has_political_proposal = models.BooleanField(default=False, verbose_name=u"Ya sea diputado(a) o candidato(a), ¿Cuenta ud. con una propuesta política para su gestión (2019-2024)?", null=True, blank=True)
    political_proposal_link = models.URLField(null=True, max_length=255, verbose_name=u"Si respondió \"sí\", indique en qué link se puede acceder a su propuesta política", blank=True)
    political_proposal_doc = models.FileField(upload_to='political_proposals/%Y/%m/%d/',
                                     null=True,
                                     verbose_name=u"Si respondió \"sí\" pero no tiene su propuesta política online, acá tiene la posibilidad de adjuntar el archivo", blank=True)    
    
    
    #delaracion de patrimonio e intereses
    intention_to_transparent_patrimony = models.BooleanField(default=False, null=True, verbose_name=u"¿Desea Ud. compartir sus declaraciones de Patrimonio e Intereses", blank=True)
    existing_patrimony_declaration = models.BooleanField(default=False, null=True, verbose_name=u"¿Cuenta ud. con una declaración de intereses actualizada?", blank=True)
    patrimony_link = models.URLField(null=True,
                                     verbose_name=u"Si respondió 'sí' por favor indique a continuación el link para acceder a su declaración de patrimonio", blank=True)
    patrimony_doc = models.FileField(upload_to='patrimony/%Y/%m/%d/',
                                     null=True,
                                     verbose_name=u"Si respondió 'sí' pero no tiene su declaración de patrimonio publicada online, acá tiene la oportunidad de adjuntar el archivo", blank=True)
    existing_interests_declaration = models.BooleanField(default=False, null=True, verbose_name=u"¿Cuenta ud. con una declaración de intereses actualizada?", blank=True)
    interests_link = models.CharField(max_length=255, null=True,
                                      verbose_name=u"Si respondió 'sí' por favor indique a continuación el link para acceder a su declaración de Intereses", blank=True)
    interests_doc = models.FileField(upload_to='patrimony/%Y/%m/%d/',
                                     null=True,
                                     verbose_name=u"Si respondió 'sí' pero no tiene su declaración de intereses publicada online, acá tiene la oportunidad de adjuntar el archivo", blank=True)
    
    
    #procesos judiciales    
    declared_intention_to_transparent_judiciary_records = models.BooleanField(default=False,
                                                verbose_name=u"¿Desea Ud. compartir información sobre los procesos judiciales en los que ha estado involucrado(a)?", blank=True)
    judiciary_processes_involved = models.IntegerField(null=True, blank=True, verbose_name=u"¿En cuántos procesos judiciales ud. se ha visto involucrado en los últimos 10 años?")
    extra_judiciary_declaration = models.TextField(max_length=255,null=True, verbose_name=u"¿Se ha visto involucrado en más procesos judiciales en los últimos 10 años?", blank=True)
    judiciary_link = models.URLField(null=True, verbose_name=u"Si respondió 'sí', por favor indique dónde se puede acceder a esta información (facilite un link u otro recurso)", blank=True)
    judiciary_description = models.TextField(null=True, verbose_name=u"¿Desea agregar comentarios o notas aclaratorias sobre uno o más de los procesos judiciales declarados? Puede hacerlo a continuación", blank=True)


    #etica presupuestaria
    is_deputy = models.BooleanField(default=False, null=True, blank=True, verbose_name=u"¿Eres actualmente diputado/a?")
    declared_intention_to_transparent_public_resources_usage = models.BooleanField(default=False, verbose_name=u"¿Desea Ud. compartir información sobre su uso de recursos públicos?", blank=True)
    benefits = models.ManyToManyField(Benefit, blank=True)
    benefits_link = models.CharField(max_length=512,
                                     verbose_name=u"Por favor, indique en qué link es posible acceder al detalle sobre los montos asociados a su uso de beneficios",
                                     null=True, blank=True)
    benefits_doc = models.FileField(upload_to='benefits/%Y/%m/%d/',
                                     null=True,
                                     verbose_name=u"Si el detalle de su uso de beneficios no se encuentra publicado online, puede subir el archivo a continuación", blank=True)
    
    # declared_intention_to_transparent = models.BooleanField(default=False, verbose_name=u"¿Desea Ud. transparentar su información política general?", blank=True)
    # period = models.CharField(max_length=255, verbose_name=u"¿En qué período legislativo se encuentra actualmente?", null=True, blank=True)
    
    # reelection = models.BooleanField(default=False, verbose_name=u"¿Va a reelección?", null=True, blank=True)

    intention_to_transparent_work_plan = models.BooleanField(default=False, verbose_name=u"¿Desea Ud. transparentar su plan de trabajo de diputado(a) o candidato(a)?", blank=True)

    work_plan_link = models.URLField(null=True, max_length=255, verbose_name=u"Si respondió 'sí', indique en qué link se puede acceder a su programa de trabajo", blank=True)
    work_plan_doc = models.FileField(upload_to='work_plans/%Y/%m/%d/',
                                     null=True,
                                     verbose_name=u"Si respondió 'sí' pero no tiene su plan de trabajo online, acá tiene la posibilidad de adjuntar el archivo", blank=True)
    eth_001_link = models.URLField(verbose_name=u"Indique en qué link es posible acceder al detalle de su planilla 001",
                                   help_text=u"Link a la planilla 001", null=True, blank=True)
    eth_001_doc = models.FileField(upload_to='eth_001/%Y/%m/%d/', null=True, blank=True, 
                                    verbose_name=u"Si su planilla 001 no se encuentra publicada online, puede subir el archivo a continuación")
    eth_002_link = models.URLField(verbose_name=u"Indique en qué link es posible acceder al detalle de su planilla 002",
                                   help_text=u"Link a la planilla 002", null=True, blank=True)
    eth_002_doc = models.FileField(upload_to='eth_002/%Y/%m/%d/', null=True, blank=True, 
                                    verbose_name=u"Si su planilla 002 no se encuentra publicada online, puede subir el archivo a continuación")
    eth_080_link = models.URLField(verbose_name=u"Indique en qué link es posible acceder al detalle de su planilla 080",
                                   help_text=u"Link a la planilla 080", null=True, blank=True)
    eth_080_doc = models.FileField(upload_to='eth_080/%Y/%m/%d/',
                                  verbose_name=u"Si su planilla 080 no se encuentra publicada online, puede subir el archivo a continuación",
                                  help_text=u"Link a la planilla 080", null=True, blank=True)
    eth_172_link = models.URLField(verbose_name=u"Indique en qué link es posible acceder al detalle de su planilla 172",
                                   help_text=u"Link a la planilla 172", null=True, blank=True)
    eth_172_doc = models.FileField(upload_to='eth_172/%Y/%m/%d/',
                                  verbose_name=u"Si su planilla 172 no se encuentra publicada online, puede subir el archivo a continuación",
                                  help_text=u"Link a la planilla 172", null=True, blank=True)
    attendance = models.FloatField(verbose_name="Indique su porcentaje de asistencia a la Asamblea Nacional durante este período legislativo", null=True, blank=True)
    laws_worked_on = models.IntegerField(verbose_name="Indique el número de leyes que ud. ha sancionado en el último período legislativo", null=True, blank=True)

                                  


    slug = AutoSlugField(populate_from='name', null=True)

    objects = models.Manager() # The default manager.
    ranking = RankingManager() # The Dahl-specific manager.

    def get_mark_non_deputy(self):
        current_mark = 0
        if self.work_plan_link or self.work_plan_doc:
            current_mark += 10
        return current_mark

    def get_mark_deputy(self):
        current_mark = 0
        if self.work_plan_link or self.work_plan_doc:
            current_mark += 5
        return current_mark

    @property
    def mark(self):
        ## Jordito querido hermano
        ## Aquí se calcula el mark, pensé que sería bacán que uno fuera sumando cosas en la medida en que se van
        ## calculando. Con el operador += sumas y eso.
        ## Besito.
        final_mark = 0
        if self.educational_records.exists():
            final_mark += 2.5
        if self.work_records.exists():
            final_mark += 2.5
        ## Cacha que se calculan de manera distinta
        ## las mark si son diputados o si no lo son:
        ## Fíjate en los tests por que son dos distintos
        if self.is_deputy:
            final_mark += self.get_mark_deputy()
        else:
            final_mark += self.get_mark_non_deputy()
        return final_mark
        
    def get_absolute_url(self):
        return reverse('candidate-profile', kwargs={'slug': self.slug})


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Persona"

def topics_changed(sender, **kwargs):
    if kwargs['instance'].topics.count() > 3:
        raise ValidationError("You can't assign more than three topics")


m2m_changed.connect(topics_changed, sender=Person.topics.through)



class Contact(models.Model):
    person = models.ForeignKey(Person, related_name='contact', on_delete=models.CASCADE)
    email = models.EmailField(max_length=255)
    identifier = models.UUIDField(default=uuid.uuid4, editable=False)

    def save(self, *args, **kwargs):
        creating = False
        if self.id is None:
            creating = True
        super(Contact, self).save(*args, **kwargs)
        if creating:
            site = Site.objects.get_current()
            send_templated_mail(
                                template_name='bienvenido',
                                from_email=settings.DEFAULT_FROM_EMAIL,
                                recipient_list=[self.email],
                                context={
                                    'contact': self,
                                    'person': self.person,
                                    'site': site,
                                },
                                # Optional:
                                # cc=['cc@example.com'],
                                # bcc=['bcc@example.com'],
                                # headers={'My-Custom-Header':'Custom Value'},
                                # template_prefix="my_emails/",
                                # template_suffix="email",
                        )
            self.person.email = self.email
            self.person.save()

    def update_url(self):
        return reverse('update-person-data', kwargs={'identifier': self.identifier})

    class Meta:
        verbose_name = "Contacto"


