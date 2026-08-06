from django import forms
from django.core.exceptions import ValidationError
from ..models import ScreenType
from core.utils.validators import (
    validate_only_numbers, 
    validate_and_format_decimal
)

class ScreenInventoryForm(forms.Form):
    name = forms.CharField(
        label="Nombre de Pantalla",
        widget=forms.TextInput(attrs={"class": "form-control", "readonly": "readonly"}),
        required=False
    )
    price = forms.CharField(
        label="Precio",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "0.00"}),
        required=True,
        initial=""  # Forzamos vacío
    )
    quantity = forms.CharField(
        label="Cantidad",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "0"}),
        required=True,
        initial=""  # Forzamos vacío
    )
    screen_type = forms.ModelChoiceField(
        queryset=ScreenType.objects.all(),
        label="Tipo de pantalla",
        widget=forms.Select(attrs={"class": "form-select"}),
        required=True,
        empty_label="Seleccione un tipo",
        initial=None  # Forzamos vacío
    )

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