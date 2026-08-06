import uuid
from django.db import models

class ScreenType(models.Model):
    id = models.BigAutoField(db_column='id', primary_key=True, editable=False)
    name = models.CharField(db_column='nombre', max_length=20, blank=False, null=False)

    class Meta:
        db_table = 'screen_type'
        
    def __str__(self):
        return self.name or "name"


class Screen(models.Model):
    id = models.BigAutoField(db_column='id', primary_key=True, editable=False)
    name = models.CharField(db_column='nombre', max_length=20, blank=False, null=False)

    class Meta:
        db_table = 'screen'


class ScreensInventory(models.Model):
    id = models.BigAutoField(db_column='id', primary_key=True, editable=False)
    screen_type = models.ForeignKey('ScreenType',on_delete=models.CASCADE, db_column='id_screen_type', related_name='screens' )
    price = models.DecimalField(db_column='price', max_digits=18, decimal_places=2) 
    quantity = models.PositiveIntegerField(db_column='quantity') 
    
    screen = models.ForeignKey(
        'Screen',
        on_delete=models.CASCADE, 
        db_column='id_screen', 
        related_name='inventory_records'
    )

    class Meta:
        db_table = 'screens_inventory'
        
    def __str__(self):
        # Aquí defines cómo quieres que se muestre por defecto en cualquier select o template
        return f"{self.screen_type.name} - {self.quantity} - ${self.price}"