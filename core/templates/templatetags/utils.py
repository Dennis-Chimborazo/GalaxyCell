from django import template

register = template.Library()


@register.filter
def is_dict(value):
    return isinstance(value, dict)


@register.filter
def get_item(dictionary, key):
    if isinstance(dictionary, dict):
        value = dictionary.get(key, "")
        return "" if value is None else value

    return ""


@register.filter
def get_id(row):
    if not row:
        return ""

    if isinstance(row, dict):
        return row.get("id") or row.get("pk") or ""

    return getattr(row, "id", getattr(row, "pk", "")) or ""


@register.filter
def get_attr(obj, attr):
    """
    Soporta atributos anidados: 'user.name'.
    Evita romper el template si obj llega como string, None o valor inválido.
    """
    try:
        if not obj or not attr:
            return ""

        for part in str(attr).split("."):
            if isinstance(obj, dict):
                obj = obj.get(part, "")
            else:
                obj = getattr(obj, part, "")

            if obj is None:
                return ""

        return obj

    except Exception:
        return ""


@register.filter
def is_callable(value):
    return callable(value)