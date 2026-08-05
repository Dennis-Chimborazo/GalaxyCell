from django import forms
from django.core.exceptions import ValidationError
from .models import Client
from core.utils.validators import (
    validate_only_numbers, 
    validate_alphanumeric_special
)

class ClientSearchForm(forms.Form):
    search_client = forms.CharField(
        required=False,
        label="Buscar Cliente",
        widget=forms.TextInput(attrs={
            "placeholder": "Ej: Juan o 0102030405",
            "class": "form-control"
        })
    )

    def clean_search_client(self):
        value = self.cleaned_data.get("search_client", "").strip()
        if not value:
            return ""
        try:
            # Permite letras, números y caracteres especiales comunes en cédulas o nombres
            return validate_alphanumeric_special(value, caracteres="-/ ")
        except ValidationError:
            raise
        except Exception:
            raise ValidationError("Ingresó valores no permitidos en la búsqueda")


class ClientForm(forms.ModelForm):
    id_card = forms.CharField(
        label="Cédula",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Ingrese cédula"}),
        required=True
    )
    name = forms.CharField(
        label="Nombre",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Ingrese nombre"}),
        required=True
    )
    address = forms.CharField(
        label="Dirección",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Ingrese dirección"}),
        required=True
    )

    class Meta:
        model = Client
        fields = ['id_card', 'name', 'address']

    def clean_id_card(self):
        id_card = self.cleaned_data.get("id_card", "").strip()
        try:
            return validate_only_numbers(id_card)
        except ValidationError:
            raise
        except Exception:
            raise ValidationError("Ingresó valores no permitidos en la cédula")

    def clean_name(self):
        name = self.cleaned_data.get("name", "").strip()
        try:
            return validate_alphanumeric_special(name, caracteres=" -")
        except ValidationError:
            raise
        except Exception:
            raise ValidationError("Ingresó valores no permitidos en el nombre")

    def clean_address(self):
        address = self.cleaned_data.get("address", "").strip()
        try:
            return validate_alphanumeric_special(address, caracteres="-/#°.")
        except ValidationError:
            raise
        except Exception:
            raise ValidationError("Ingresó valores no permitidos en la dirección")