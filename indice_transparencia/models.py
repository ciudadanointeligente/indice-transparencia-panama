from django.db import models

TYPES_OF_PERSON = (('parlamentario', 'Parlamentario'), ('candidato', 'Candidato'), )


class Person(models.Model):
    name = models.CharField(max_length=255, verbose_name=u"Nombre")
    specific_type = models.CharField(max_length=255,
                                     choices=TYPES_OF_PERSON,
                                     verbose_name=u"Tipo de persona",
                                     help_text=u"Parlamentario o candidato")
    gender = models.CharField(max_length=255, null=True)
    birth_date = models.DateField(verbose_name=u"Fecha de nacimiento", null=True)
    email = models.EmailField(verbose_name=u"Correo electrónico", null=True)
    web = models.URLField(verbose_name=u"Página web personal", null=True)
    party = models.CharField(max_length=255, verbose_name=u"Partido", null=True)
    circuit = models.CharField(max_length=255, verbose_name=u"Circuito", null=True)
    period = models.CharField(max_length=255, verbose_name=u"Periodo", null=True)
    reelection = models.BooleanField(default=False, verbose_name=u"¿Va a reelección?", null=True)
    cv_educ = models.BooleanField(default=False, verbose_name=u"¿Publica su formación académica?", null=True)
    cv_educ_detail = models.TextField(verbose_name=u"Detalle de su formación académica", null=True)
    cv_experpro = models.BooleanField(default=False, verbose_name=u"¿Publica su experiencia profesional?", null=True)
    cv_experpro_detail = models.URLField(verbose_name=u"Link a CV con detalles.", null=True)
    cv_experpol = models.BooleanField(default=False, verbose_name=u"¿Publica su experiencia en otros cargos políticos?", null=True)
    cv_experpol_detail =  models.TextField(verbose_name=u"Texto con resumen de su experiencia política previa", null=True)
    cv_transfu = models.IntegerField(verbose_name=u"Transfuguismo",
                                     help_text=u"número de veces que ha cambiado de afiliación política (partido o movimientos)",
                                     default=0)
    wor_attendance = models.FloatField(verbose_name=u"Trabajo legislativo / Asistencia",
                                       help_text=u"porcentaje de asistencia a la Asamblea en el período",
                                     default=0)
    wor_proposals = models.IntegerField(verbose_name=u"Trabajo legislativo / Propuestas",
                                       help_text=u"número de propuestas (de discusión, proyectos de ley, etc) realizadas durante el período",
                                     default=0)
    wor_vote = models.IntegerField(verbose_name=u"Trabajo legislativo / Votaciones",
                                   help_text=u"número de participaciones en votaciones durante el último período",
                                     default=0)
    eth_080 = models.BooleanField(default=False, verbose_name=u"Ética presupuestaria / planilla 080",
                                   help_text=u"¿publica planilla 080?")
    eth_080_link = models.URLField(verbose_name=u"Ética presupuestaria / planilla 080",
                                   help_text=u"Link a la planilla 080", null=True)
    eth_172 = models.BooleanField(default=False)
    eth_172_link = models.URLField(verbose_name=u"Ética presupuestaria / planilla 172",
                                   help_text=u"Link a la planilla 172", null=True)
    eth_trav_N = models.IntegerField(verbose_name=u"Ética presupuestaria / Número de viajes",
                                   help_text=u"Número de viajes realizados por concepto de beneficios.",
                                     default=0)
    eth_trav_exp = models.BigIntegerField(verbose_name=u"Ética presupuestaria / Dinero gastado en viajes",
                                   help_text=u"Monto gastado en viáticos en viajes realizados por concepto de beneficios.",
                                     default=0)
    eth_trav_link = models.URLField(verbose_name=u"Link al documento con el detalle de número y viáticos en viajes", null=True)
    eth_exo = models.BigIntegerField(verbose_name=u"Ética presupuestaria / Exoneración",
                               help_text=u"monto total de las exoneraciones de vehículos por concepto de beneficios",
                                     default=0)
    eth_exo_link = models.URLField(verbose_name=u"Ética presupuestaria / Link a Exoneración",
                               help_text=u"link al documento con el detalle de los montos por exoneración de vehículos", null=True)
