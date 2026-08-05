from django.db.models import Sum, Q
from django.db import DatabaseError
from .models import Screen
from django.db.models.functions import Coalesce

def get_screen_list(search_name=None):
    try:
        queryset = Screen.objects.all()

        if search_name:
            queryset = queryset.filter(name__icontains=search_name)
        return queryset.annotate(
            oled=Coalesce(
                Sum(
                    'inventory_records__quantity', 
                    filter=Q(inventory_records__screen_type__name__iexact="oled")), 0),
            oled_con_marco=Coalesce(
                Sum(
                    'inventory_records__quantity', 
                    filter=Q(inventory_records__screen_type__name__iexact="oled con marco")), 0),
            incell=Coalesce(
                Sum(
                    'inventory_records__quantity', 
                    filter=Q(inventory_records__screen_type__name__iexact="incell")),0),
            incell_con_marco=Coalesce(
                Sum(
                    'inventory_records__quantity', 
                    filter=Q(inventory_records__screen_type__name__iexact="incell con marco")), 0)
        ).order_by('name')
        
    except DatabaseError:
        return Screen.objects.none()
    
def exists_screen(name, exclude_pk=None):

    try:
        queryset = Screen.objects.filter(name__iexact=name)
        
        if exclude_pk:
            queryset = queryset.exclude(pk=exclude_pk)
            
        return queryset.exists() # .exists() devuelve True o False eficientemente
    except DatabaseError:
        return False
def get_screen_by_id(screen_id):
    try:
        return Screen.objects.get(pk=screen_id)
    except Screen.DoesNotExist:
        return None
    except DatabaseError:
        return None