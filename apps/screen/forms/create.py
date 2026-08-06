from django import forms
from django.core.exceptions import ValidationError
from ..models import ScreenType, Screen
from core.utils.validators import (
    validate_only_numbers, 
    validate_alphanumeric_special, 
    validate_and_format_decimal
)

class ScreenForm(forms.ModelForm): # Corrección: Cambiado a ModelForm
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
    screen_type = forms.ModelChoiceField(
        queryset=ScreenType.objects.all(),
        label="Tipo de pantalla",
        widget=forms.Select(attrs={"class": "form-select"}),
        required=True,
        empty_label="Seleccione..."
    )

    class Meta:
        model = Screen
        fields = ["name"]
        labels = {
            "name": "Nombre",
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"})
        }

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
