from django.urls import reverse_lazy
from core.views.base_table import BaseTableMixin
from ..selectors import get_sales_list

class SalesTableMixin(BaseTableMixin):
    headers = [
        "Cliente",
        "Pantalla",
        "Tipo de Pantalla",
        "Precio Venta",
        "Cantidad",
    ]

    fields = [
        "client_name",
        "screen_name",
        "screen_type_name",
        "price_sales",
        "quantity",
    ]

    list_url = "sales:list"
    table_url = "sales:table"
    
    # Si requieres acciones de edición o creación para ventas, puedes agregarlas aquí
    has_actions = False 
    has_actions_create = False

    def get_table_context(self, queryset=None, request=None):
        if queryset is None:
            queryset = get_sales_list()[:10]

        context = super().get_table_context(
            queryset=queryset,
            request=request,
        )

        context.update({
            "sales_details": queryset,
            "sales_create_url":  None,
            "has_actions": self.has_actions,
            "has_actions_create": self.has_actions_create,
        })

        return context

    def get_create_url(self):
        return reverse_lazy("sales:create")