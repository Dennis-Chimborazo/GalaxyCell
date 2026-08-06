from django import forms
from django.core.exceptions import ValidationError
from core.utils.validators import validate_alphanumeric_special, validate_only_numbers

class SalesSearchForm(forms.Form):
    client_id = forms.CharField(
        required=False,
        label="ID del Cliente",
        widget=forms.TextInput(attrs={
            "placeholder": "Buscar por ID de cliente",
            "class": "form-control"
        })
    )
    
    screen_name = forms.CharField(
        required=False,
        label="Nombre de Pantalla",
        widget=forms.TextInput(attrs={
            "placeholder": "Buscar por nombre de pantalla",
            "class": "form-control"
        })
    )

    def clean_client_id(self):
        value = self.cleaned_data.get("client_id", "").strip()
        if not value:
            return ""
        try:
            return validate_only_numbers(value)
        except ValidationError:
            raise
        except Exception:
            raise ValidationError("Ingresó valores no permitidos para el ID")

    def clean_screen_name(self):
        value = self.cleaned_data.get("screen_name", "").strip()
        if not value:
            return ""
        try:
            return validate_alphanumeric_special(value, caracteres="-/")
        except ValidationError:
            raise
        except Exception:
            raise ValidationError("Ingresó valores no permitidos para el nombre")