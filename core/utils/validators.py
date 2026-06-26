# core/utils/validators.py
import re
from django.core.exceptions import ValidationError
from decimal import Decimal, InvalidOperation

def _normalize_value(value):

    try:
        if value is None:
            raise ValidationError("Este campo es obligatorio.")

        value = str(value).strip()

        if not value:
            raise ValidationError("Este campo es obligatorio.")

        return value

    except ValidationError:
        raise

    except Exception:
        raise ValidationError("Error al procesar el valor ingresado.")


def validate_only_numbers(value):
    try:
        value = _normalize_value(value)

        if not re.fullmatch(r"[0-9]+", value):
            raise ValidationError("Solo se permiten números.")

        return value

    except ValidationError:
        raise

    except Exception:
        raise ValidationError("Error inesperado al validar números.")
    
def validate_and_format_decimal(value):
    try:
        value = _normalize_value(value)
        value_str = str(value).strip()
        if not re.fullmatch(r"^-?\d+([.,]\d+)?$", value_str):
            raise ValidationError("Solo se permiten números enteros o decimales.")
        value_standard = value_str.replace(',', '.')
        return Decimal(value_standard)

    except ValidationError:
        raise
    except (ValueError, InvalidOperation):
        raise ValidationError("El formato numérico no es válido.")
    except Exception:
        raise ValidationError("Error inesperado al validar el decimal.")

def validate_only_letters(value):
    try:
        value = _normalize_value(value)

        if not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+", value):
            raise ValidationError("Solo se permiten letras.")

        return value

    except ValidationError:
        raise

    except Exception:
        raise ValidationError("Error inesperado al validar letras.")

def validate_alphanumeric(value):
    try:
        value = _normalize_value(value)

        if not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñ0-9]+", value):
            raise ValidationError("Solo se permiten letras y números.")

        return value

    except ValidationError:
        raise

    except Exception:
        raise ValidationError("Error inesperado al validar letras y números.")

def validate_alphanumeric_special(value, caracteres="/-"):
    try:
        value = _normalize_value(value)
        value_str = str(value).strip() if value is not None else ""
        if not value_str:
            return value_str

        if caracteres is None:
            caracteres = ""
        else:
            caracteres = str(caracteres)

        caracteres_escape = re.escape(caracteres)

        patron = rf"[A-Za-zÁÉÍÓÚáéíóúÑñ0-9\s{caracteres_escape}]+"

        if not re.fullmatch(patron, value_str):
            msg = "Solo se permiten letras, números y espacios."
            if caracteres:
                msg += f" También se permiten: {caracteres}"
            raise ValidationError(msg)

        return value_str

    except ValidationError:
        raise
    except Exception:
        raise ValidationError("Error inesperado al validar caracteres especiales.")