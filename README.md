Índice de Transparencia de Panamá
==============
Este proyecto genera un índice que evalúa candidatos y parlamentarios panameños, según variables ...


Para cargar datos de ejemplo:
-----------------------------
```
python manage.py loaddata datos_de_ejemplo.yaml
```


Para generarlos datos de ejemplo:
-------------
```
python manage.py dumpdata indice_transparencia.party indice_transparencia.benefit indice_transparencia.circuit indice_transparencia.topic indice_transparencia.person indice_transparencia.workrecord indice_transparencia.educationalrecord indice_transparencia.judiciaryprocessrecord --format=yaml >> datos_de_ejemplo.yaml
 ```
