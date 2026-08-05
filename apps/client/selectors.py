from django.db import DatabaseError
from django.db.models import Q
from .models import Client

def get_client_list(search_query=None):
    try:
        queryset = Client.objects.all()
        
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) | 
                Q(id_card__icontains=search_query)
            )
            
        return queryset
    except DatabaseError:
        return Client.objects.none()