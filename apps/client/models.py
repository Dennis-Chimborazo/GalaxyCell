from django.db import models

class Client(models.Model):
    id = models.BigAutoField(db_column='id', primary_key=True, editable=False)
    id_card= models.CharField(db_column='cedula', max_length=10, blank=False, null=False)
    name = models.CharField(db_column='nombre', max_length=20, blank=False, null=False)
    address= models.CharField(db_column='direccion', max_length=100, blank=False, null=False)

    class Meta:
        db_table = 'client'
