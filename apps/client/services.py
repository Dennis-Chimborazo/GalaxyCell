from django.db import DatabaseError, transaction
from django.core.exceptions import ValidationError
from .models import Client

def create_client(cleaned_data):
    """
    Crea un nuevo registro de cliente en la base de datos.
    """
    try:
        with transaction.atomic():
            client = Client.objects.create(
                id_card=cleaned_data.get('id_card'),
                name=cleaned_data.get('name'),
                address=cleaned_data.get('address')
            )
            return client
    except DatabaseError as e:
        # Puedes registrar el error en los logs si lo deseas
        raise ValidationError("Ocurrió un error en la base de datos al intentar crear el cliente.")
    except Exception as e:
        raise ValidationError(f"Error inesperado al crear el cliente: {str(e)}")


def update_client(client_id, cleaned_data):
    """
    Actualiza un registro de cliente existente en la base de datos.
    """
    try:
        with transaction.atomic():
            # Buscamos el cliente o lanzamos error si no existe
            client = Client.objects.select_for_update().get(pk=client_id)
            
            client.id_card = cleaned_data.get('id_card', client.id_card)
            client.name = cleaned_data.get('name', client.name)
            client.address = cleaned_data.get('address', client.address)
            
            client.save()
            return client
            
    except Client.DoesNotExist:
        raise ValidationError("El cliente que intenta actualizar no existe.")
    except DatabaseError as e:
        raise ValidationError("Ocurrió un error en la base de datos al intentar actualizar el cliente.")
    except Exception as e:
        raise ValidationError(f"Error inesperado al actualizar el cliente: {str(e)}")