from django import template
from django.urls import reverse, NoReverseMatch

register = template.Library()


def resolve_url(name):
    """Resuelve la URL de Django de forma segura, evitando fallos si no existe."""
    try:
        return reverse(name)
    except NoReverseMatch:
        return name if name.startswith("/") else "#"


def build_raw_menu():
    """Retorna la estructura completa del menú sin restricciones de acceso."""
    return [
        {
            "label": "Pantallas",
            "name": "archivo",
            "submenu": [
                {
                    "label": "Registro",
                    "url": resolve_url("screen:list"),
                },
                {
                    "label": "Ventas",
                    "url": resolve_url("sales:list"),
                },
            ],
        },
        {
            "label": "Clientes",
            "name": "clients",
            "submenu": [
                {
                    "label": "Registro",
                    "url": resolve_url("client:list"),
                },
            ],
        },
        {
            "label": "Configuración",
            "name": "configuracion",
            "submenu": [
                {
                    "label": "Datos personales",
                    "url": resolve_url("user:info"),
                },
            ],
        },
    ]


@register.simple_tag
def get_menu_items(user):
    """Retorna el menú completo si el usuario está autenticado, sin discriminar roles."""
    if not user or not user.is_authenticated:
        return []

    return build_raw_menu()