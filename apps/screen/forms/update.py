from django import forms
from django.core.exceptions import ValidationError
from ..models import Screen, ScreensInventory
from core.utils.validators import (
    validate_only_numbers, 
    validate_alphanumeric_special, 
    validate_and_format_decimal
)


class ScreenUpdateForm(forms.ModelForm):
    price = forms.CharField(
        label="Precio",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "0.00"}),
        required=True
    )
    quantity = forms.CharField(
        label="Cantidad",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "0"}),
        required=True
    )
    
    screen_inventory = forms.ModelChoiceField(
        queryset=ScreensInventory.objects.none(),
        label="Tipo e Inventario de Pantalla",
        widget=forms.Select(attrs={"class": "form-select"}),
        required=True,
        empty_label="Seleccione un registro..."
    )

    class Meta:
        model = Screen
        fields = ["name"]
        labels = {
            "name": "Nombre",
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "maxlength": "20", "minlength": "2"})
        }

    def __init__(self, *args, **kwargs):
        self.screen_instance = kwargs.pop('screen', None)
        super().__init__(*args, **kwargs)

        if self.screen_instance:
            inventory_qs = self.screen_instance.inventory_records.select_related('screen_type').all()
            self.fields['screen_inventory'].queryset = inventory_qs
            
            # Formato limpio para que muestre el tipo, cantidad y precio en el select
            self.fields['screen_inventory'].label_from_instance = lambda obj: (
                f"{obj.screen_type.name} - {obj.quantity} - ${obj.price}"
            )

            selected_inventory = None
            
            # Verificamos si se seleccionó un inventario vía GET (HTMX) o data enviada
            if self.data and 'screen_inventory' in self.data:
                try:
                    selected_inventory = inventory_qs.get(pk=self.data.get('screen_inventory'))
                except (ScreensInventory.DoesNotExist, ValueError):
                    pass
            elif self.initial and 'screen_inventory' in self.initial:
                selected_inventory = self.initial.get('screen_inventory')
            elif self.screen_instance.pk:
                selected_inventory = inventory_qs.order_by('-id').first()

            if selected_inventory:
                self.fields['screen_inventory'].initial = selected_inventory
                
                # CORRECCIÓN CLAVE: Asignamos los valores aunque venga self.data (para que HTMX los pinte bien)
                self.fields['price'].initial = selected_inventory.price
                self.fields['quantity'].initial = selected_inventory.quantity
                
                if not self.data or 'screen_inventory' in self.data and 'price' not in self.data:
                    self.data = self.data.copy() if self.data else {}
                    self.data['price'] = str(selected_inventory.price)
                    self.data['quantity'] = str(selected_inventory.quantity)

    def clean_name(self):
        name = self.cleaned_data.get("name", "").strip()
        try:
            return validate_alphanumeric_special(name, caracteres="-/")
        except ValidationError:
            raise
        except Exception:
            raise ValidationError("Ingresó valores no permitidos")
        
    def clean_price(self):
        price = self.cleaned_data.get("price", "").strip()
        try:
            return validate_and_format_decimal(price)
        except ValidationError:
            raise
        except Exception:
            raise ValidationError("Ingresó valores no permitidos")

    def clean_quantity(self):
        quantity = self.cleaned_data.get("quantity", "").strip()
        try:
            return validate_only_numbers(quantity)
        except ValidationError:
            raise
        except Exception:
            raise ValidationError("Ingresó valores no permitidos")