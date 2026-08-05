from django.db import transaction, DatabaseError
from .models import Screen, ScreensInventory, ScreenType

def create_screen(*, name, screen_type_id, quantity, price):
    try:
        with transaction.atomic():
            # 1. Buscar o crear la pantalla por nombre (Case-Insensitive)
            # Evita crear duplicados de "A03S" con distintos UUIDs
            name_clean = name.strip()
            new_screen = Screen.objects.filter(name__iexact=name_clean).first()
            
            if not new_screen:
                new_screen = Screen.objects.create(name=name_clean)
            
            # 2. Validar que el tipo de pantalla exista
            screen_type_instance = ScreenType.objects.get(id=screen_type_id)
            
            # 3. Regla de negocio: Si coinciden Screen, ScreenType y Precio -> Se acumula la cantidad
            inventory_record = ScreensInventory.objects.filter(
                screen=new_screen,
                screen_type=screen_type_instance,
                price=price
            ).first()
            
            if inventory_record:
                # Si ya existe exactamente igual, sumamos al stock existente
                inventory_record.quantity += int(quantity)
                inventory_record.save()
            else:
                # Si el precio es distinto o no existe, creamos un nuevo desglose de inventario
                ScreensInventory.objects.create(
                    screen=new_screen,
                    screen_type=screen_type_instance,
                    quantity=quantity,
                    price=price
                )
            
            return new_screen
            
    except (DatabaseError, ScreenType.DoesNotExist) as e:
        return None


def create_screen2(*, name):
    try:
        with transaction.atomic():
            name_clean = name.strip()
            new_screen = Screen.objects.filter(name__iexact=name_clean).first()
            
            if not new_screen:
                new_screen = Screen.objects.create(name=name_clean)
            
            return new_screen
            
    except (DatabaseError, ScreenType.DoesNotExist) as e:
        return None

def update_screen(*, screen_id, name=None, screen_type_id=None, quantity=None, price=None):
    try:
        with transaction.atomic():
            # 1. Obtener la pantalla a modificar
            screen = Screen.objects.get(id=screen_id)
            
            # 2. Si viene un nuevo nombre, lo actualizamos
            if name is not None:
                screen.name = name
                screen.save()
            
            # 3. Obtener el registro de inventario de esta pantalla
            # Usamos .select_for_update() para bloquear la fila en Postgres durante la transacción
            inventory = ScreensInventory.objects.select_for_update().get(screen=screen)
            
            # 4. Si viene un nuevo tipo de pantalla, validamos que exista y lo asignamos
            if screen_type_id is not None:
                screen_type_instance = ScreenType.objects.get(id=screen_type_id)
                inventory.screen_type = screen_type_instance
            
            # 5. Actualizar cantidad y precio si vienen en los parámetros
            if quantity is not None:
                inventory.quantity = quantity
                
            if price is not None:
                inventory.price = price
            
            # Guardamos los cambios del inventario si algo cambió
            inventory.save()
            
            return screen
            
    except (Screen.DoesNotExist, ScreensInventory.DoesNotExist):
        # Maneja el caso si el ID de la pantalla o su inventario no existen
        return None
    except ScreenType.DoesNotExist:
        # Maneja el caso si el nuevo tipo de pantalla enviado no es válido
        return None
    except DatabaseError:
        # Maneja cualquier otro error de base de datos en Postgres
        return None