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
                    "label": "Oled",
                    "url": resolve_url("cooperative:list"),
                },
                {
                    "label": "Incell",
                    "url": resolve_url("office:list"),
                },
                # {
                #     "label": "Permisos",
                #     "url": resolve_url("permission:list"),
                # },
                # {
                #     "label": "Segmento",
                #     "url": resolve_url("segment:list"),
                # },
                # {
                #     "label": "Usuarios",
                #     "url": resolve_url("user:list"),
                # },
            ],
        },
        {
            "label": "Resumen",
            "name": "sincronizar",
            "submenu": [
                {
                    "label": "Pantallas vendidas",
                    "url": resolve_url("sync:debito"),
                },
                {
                    "label": "Articulos",
                    "url": resolve_url("migratedata:list"),
                },
                {
                    "label": "Ganancias",
                    "url": resolve_url("chartaccounts:list"),
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