from django.urls import reverse_lazy
from core.views.base_form import BaseFormMixin
from core.views.base_table import BaseTableMixin
from ..selectors import get_screen_list


class ScreenTableMixin(BaseTableMixin):
    headers = [
        "Nombre",
        "Oled",
        "Oled con marco",
        "Incell",
        "Incell con marco",
    ]

    fields = [
        "name",
        "oled",
        "oled_con_marco",
        "incell",
        "incell_con_marco",
    ]

    list_url = "screen:list"
    table_url = "screen:table"
    edit_url_name = "screen:edit"
    add_inventory_url_name = "screen:add-inventory"
    
    has_actions = True
    has_actions_create = True

    def get_table_context(self, queryset=None, request=None):
        if queryset is None:
            queryset = get_screen_list()[:10]

        context = super().get_table_context(
            queryset=queryset,
            request=request,
        )

        context.update({
            "screens": queryset,
            "screen_create_url": self.get_create_url(),
            "has_actions": self.has_actions,
            "has_actions_create": self.has_actions_create,
            "add_inventory_url_name": self.add_inventory_url_name,
            "edit_url_name": self.edit_url_name,
        })

        return context

    def get_create_url(self):
        return reverse_lazy("screen:create")


class ScreenFormMixin(BaseFormMixin):
    module_name = "Pantalla"

    create_success_message = (
        "La pantalla y su inventario se registraron correctamente"
    )

    update_success_message = (
        "La pantalla y su inventario se actualizaron correctamente"
    )