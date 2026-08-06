from django.db import models

class Sales(models.Model):
    id = models.BigAutoField(db_column='id', primary_key=True, editable=False)
    date = models.DateField(db_column='fecha', blank=False, null=False)
    client = models.ForeignKey(
        'client.Client',
        on_delete=models.CASCADE, 
        db_column='id_client', 
        related_name='client_sales'
    )
    
    class Meta:
        db_table = 'sales'
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'

    def __str__(self):
        return f"Venta #{self.id} - Cliente: {self.client_id}"


class DetailSales(models.Model):
    id = models.BigAutoField(db_column='id', primary_key=True, editable=False)
    price_shop = models.DecimalField(
        db_column='precio_compra', 
        max_digits=10, 
        decimal_places=2, 
        blank=False, 
        null=False
    )
    price_sales = models.DecimalField(
            db_column='precio_venta', 
            max_digits=10, 
            decimal_places=2, 
            blank=False, 
            null=False
        )
    quantity = models.PositiveIntegerField(
        db_column='cantidad', 
        blank=False, 
        null=False
    )
    sales = models.ForeignKey(
        'Sales',
        on_delete=models.CASCADE, 
        db_column='id_sales', 
        related_name='details'
    )
    screen = models.ForeignKey(
        'screen.Screen',
        on_delete=models.CASCADE, 
        db_column='id_screen', 
        related_name='screen_sales_details'
    )
    screen_type = models.ForeignKey(
        'screen.ScreenType',
        on_delete=models.CASCADE, 
        db_column='id_screen_type', 
        related_name='type_sales_details'
    )
    
    class Meta:
        db_table = 'sales_detail'
        verbose_name = 'Detalle de Venta'
        verbose_name_plural = 'Detalles de Ventas'

    def __str__(self):
        return f"Detalle #{self.id} - Venta #{self.sales_id}"