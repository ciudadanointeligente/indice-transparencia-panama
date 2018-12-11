from django.db import models


TYPES_OF_PERSON = (('parlamentario', 'Parlamentario'), ('candidato', 'Candidato'), )


class Person(models.Model):
    name = models.CharField(max_length=255)
    specific_type = models.CharField(max_length=255,
                                     choices=TYPES_OF_PERSON)
