from django.db import DatabaseError
from .models import DetailSales

def get_sales_list(client_id=None, screen_name=None):
    try:
        # Consultamos directamente sobre DetailSales para listar cada ítem vendido
        queryset = DetailSales.objects.select_related(
            'sales', 
            'sales__client', 
            'screen', 
            'screen_type'
        ).all()

        # Filtro por ID de cliente si se proporciona
        if client_id:
            queryset = queryset.filter(sales__client_id=client_id)

        # Filtro por nombre de pantalla si se proporciona
        if screen_name:
            queryset = queryset.filter(screen__name__icontains=screen_name)

        # Anotamos o exponemos campos amigables si tu BaseTableMixin los requiere directamente como atributos del objeto, 
        # o bien puedes acceder a ellos en tu template mediante la relación (ej: detail.sales.client.name)
        return queryset.order_by('-sales__date', '-id')
        
    except DatabaseError:
        return DetailSales.objects.none()