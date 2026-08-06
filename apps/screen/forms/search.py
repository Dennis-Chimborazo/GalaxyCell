from django import forms
from django.core.exceptions import ValidationError
from core.utils.validators import (validate_alphanumeric_special)

class ScreenSearchForm(forms.Form):
    search_screen = forms.CharField(
        required=False,
        label="Nombre",
        widget=forms.TextInput(attrs={
            "placeholder": "Buscar Pantalla",
            "class": "form-control"
        })    
    )

    def clean_search_screen(self):
        # Corrección: Nombre del campo corregido ('search_screen')
        value = self.cleaned_data.get("search_screen", "").strip()
        if not value:
            return ""
        try:
            return validate_alphanumeric_special(value, caracteres="-/")
        except ValidationError:
            raise
        except Exception:
            raise ValidationError("Ingresó valores no permitidos")
