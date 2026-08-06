from django.views.generic import CreateView, UpdateView
from ..forms import ScreenForm
from ..models import Screen
from ..services import create_screen
from .mixins import ScreenFormMixin

class ScreenCreateView(ScreenFormMixin, CreateView):
    model = Screen
    form_class = ScreenForm
    template_name = "partials/screen-form.html"

    def form_valid(self, form):
        try:
            self.object = create_screen(
                name=form.cleaned_data.get("name"),
                screen_type_id=form.cleaned_data.get("screen_type").id if form.cleaned_data.get("screen_type") else None,
                quantity=form.cleaned_data.get("quantity"),
                price=form.cleaned_data.get("price"),
            )

            if not self.object:
                form.add_error(
                    None,
                    "No se pudo guardar la pantalla y su inventario."
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
