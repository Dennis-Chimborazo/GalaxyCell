from core.views.base_list import BaseTableListView
from ..forms import ScreenSearchForm
from ..models import Screen
from ..selectors import get_screen_list
from .mixins import ScreenTableMixin


class ScreenListView(
    ScreenTableMixin,
    BaseTableListView,
):
    model = Screen
    context_object_name = "screens"
    paginate_by = 10

    full_template = "screen.html"
    partial_template = "partials/screen-content.html"

    list_url_name = "screen:list"
    table_url_name = "screen:table"

    search_param = "search_screen"

    refresh_message = (
        "Se actualizó la información de pantallas e inventario"
    )

    def get_queryset(self):
        form = ScreenSearchForm(self.request.GET)
        query = ""

        if form.is_valid():
            query = form.cleaned_data.get("search_screen", "")

        return get_screen_list(search_name=query)