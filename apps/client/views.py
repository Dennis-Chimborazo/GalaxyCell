from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.views.generic import CreateView, UpdateView

from core.views.base_form import BaseFormMixin
from core.views.base_list import BaseTableListView
from core.views.base_table import BaseTableMixin

from .forms import ClientForm, ClientSearchForm
from .models import Client
from .selectors import get_client_list
from .services import create_client, update_client


class ClientTableMixin(BaseTableMixin):
    headers = [
        "Cédula",
        "Nombre",
        "Dirección",
    ]

    fields = [
        "id_card",
        "name",
        "address",
    ]

    list_url = "client:list"
    table_url = "client:table"
    edit_url_name = "client:edit"

    def get_table_context(self, queryset=None, request=None):
        if queryset is None:
            queryset = get_client_list()[:10]

        context = super().get_table_context(
            queryset=queryset,
            request=request,
        )

        context.update({
            "clients": queryset,
            "client_create_url": self.get_create_url(),
        })

        return context

    def get_create_url(self):
        from django.urls import reverse_lazy
        return reverse_lazy("client:create")


class ClientListView(
    ClientTableMixin,
    BaseTableListView,
):
    model = Client
    context_object_name = "clients"
    paginate_by = 10

    full_template = "client.html"
    partial_template = "partials/client-content.html"

    list_url_name = "client:list"
    table_url_name = "client:table"

    search_param = "search_client"

    refresh_message = (
        "Se actualizó la información de clientes"
    )

    def get_queryset(self):
        form = ClientSearchForm(self.request.GET)
        query = ""

        if form.is_valid():
            query = form.cleaned_data.get("search_client", "")

        return get_client_list(search_query=query)


class ClientFormMixin(BaseFormMixin):
    module_name = "Cliente"

    create_success_message = (
        "El cliente se registró correctamente"
    )

    update_success_message = (
        "El cliente se actualizó correctamente"
    )


class ClientCreateView(ClientFormMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = "partials/client-form.html"

    def form_valid(self, form):
        try:
            # Llamamos al servicio de creación pasando el cleaned_data completo
            self.object = create_client(form.cleaned_data)

            if not self.object:
                form.add_error(
                    None,
                    "No se pudo guardar el cliente."
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


class ClientUpdateView(ClientFormMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = "partials/client-form.html"

    def form_valid(self, form):
        try:
            current_obj = self.get_object()

            # Llamamos al servicio de actualización pasándole el ID y los datos limpios
            self.object = update_client(
                client_id=current_obj.id,
                cleaned_data=form.cleaned_data
            )

            if not self.object:
                form.add_error(
                    None,
                    "No se pudo actualizar el cliente."
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