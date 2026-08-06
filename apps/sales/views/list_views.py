from core.views.base_list import BaseTableListView
from ..forms import SalesSearchForm  # El formulario que creamos antes para buscar por ID de cliente o nombre de pantalla
from ..models import DetailSales
from ..selectors import get_sales_list
from .mixins import SalesTableMixin


class SalesListView(
    SalesTableMixin,
    BaseTableListView,
):
    model = DetailSales
    context_object_name = "sales_details"
    paginate_by = 10

    full_template = "sales.html"
    partial_template = "partials/sales-content.html"

    list_url_name = "sales:list"
    table_url_name = "sales:table"

    search_param = "screen_name"  # O el parámetro principal que prefieras usar

    refresh_message = (
        "Se actualizó la información de las ventas"
    )

    def get_queryset(self):
        form = SalesSearchForm(self.request.GET)
        client_id = ""
        screen_name = ""

        if form.is_valid():
            client_id = form.cleaned_data.get("client_id", "")
            screen_name = form.cleaned_data.get("screen_name", "")

        return get_sales_list(client_id=client_id, screen_name=screen_name)