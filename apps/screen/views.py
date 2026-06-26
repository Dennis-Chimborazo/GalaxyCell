from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.views.generic import CreateView, UpdateView

from core.views.base_form import BaseFormMixin
from core.views.base_list import BaseTableListView
from core.views.base_table import BaseTableMixin

from .forms import ScreenForm, ScreenSearchForm
from .models import Screen, ScreensInventory
from .selectors import get_screen_list
from .services import create_screen, update_screen


class ScreenTableMixin(BaseTableMixin):
    headers = [
        "Nombre",
        "Oled",
        "Oled con marco",
        "Incell",
        "Incell con marco",
    ]

    # CORREGIDO: Coinciden con el transform `.annotate()` de tu selector por texto
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

    def get_table_context(self, queryset=None, request=None):
        if queryset is None:
            # CORREGIDO: Consistencia usando el selector por defecto
            queryset = get_screen_list()[:10]

        context = super().get_table_context(
            queryset=queryset,
            request=request,
        )

        context.update({
            "screens": queryset,
            "screen_create_url": self.get_create_url(),
        })

        return context

    def get_create_url(self):
        from django.urls import reverse_lazy
        return reverse_lazy("screen:create")


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

    # CORREGIDO: Ahora conecta el buscador con tu selector de agregaciones reales
    def get_queryset(self):
        form = ScreenSearchForm(self.request.GET)
        query = ""

        if form.is_valid():
            query = form.cleaned_data.get("search_screen", "")

        # Retornamos el query construido de forma centralizada en el selector
        return get_screen_list(search_name=query)


class ScreenFormMixin(BaseFormMixin):
    module_name = "Pantalla"

    create_success_message = (
        "La pantalla y su inventario se registraron correctamente"
    )

    update_success_message = (
        "La pantalla y su inventario se actualizaron correctamente"
    )


class ScreenCreateView(
    ScreenFormMixin,
    CreateView,
):
    model = Screen
    form_class = ScreenForm
    template_name = "partials/screen-form.html"

    def form_valid(self, form):
        try:
            self.object = create_screen(
                name=form.cleaned_data["name"],
                screen_type_id=form.cleaned_data["screen_type"].id,
                quantity=form.cleaned_data["quantity"],
                price=form.cleaned_data["price"],
            )

            if not self.object:
                form.add_error(
                    None,
                    "No se pudo guardar la pantalla."
                )
                return self.form_invalid(form)

            response = self.handle_create_success()

            if response:
                return response

            return super().form_valid(form)

        except Exception as e:
            form.add_error(
                None,
                f"Error al guardar: {str(e)}"
            )
            return self.form_invalid(form)

    def form_invalid(self, form):
        return self.handle_form_invalid(
            form=form,
            obj=None,
        )


class ScreenUpdateView(ScreenFormMixin, UpdateView,):
    model = Screen
    form_class = ScreenForm
    template_name = "partials/screen-form.html"

    # AJUSTADO: Dado que ahora manejas múltiples inventarios/precios acumulados, 
    # obtenemos de forma segura el registro más reciente o el primero para rellenar el formulario.
    def get_initial(self):
        initial = super().get_initial()

        try:
            inventory = ScreensInventory.objects.filter(
                screen=self.object
            ).order_by('-id').first()

            if inventory:
                initial["price"] = inventory.price
                initial["quantity"] = inventory.quantity
                initial["screen_type"] = inventory.screen_type

        except Exception:
            pass

        return initial

    def form_valid(self, form):
        try:
            current_obj = self.get_object()

            self.object = update_screen(
                screen_id=current_obj.id,
                name=form.cleaned_data.get("name"),
                screen_type_id=(
                    form.cleaned_data["screen_type"].id
                    if form.cleaned_data.get("screen_type")
                    else None
                ),
                quantity=form.cleaned_data.get("quantity"),
                price=form.cleaned_data.get("price"),
            )

            if not self.object:
                form.add_error(
                    None,
                    "No se pudo actualizar la pantalla."
                )
                return self.form_invalid(form)

            response = self.handle_update_success()

            if response:
                return response

            return super().form_valid(form)

        except Exception as e:
            form.add_error(
                None,
                f"Error al actualizar: {str(e)}"
            )
            return self.form_invalid(form)

    def form_invalid(self, form):
        return self.handle_form_invalid(
            form=form,
            obj=self.get_object(),
        )