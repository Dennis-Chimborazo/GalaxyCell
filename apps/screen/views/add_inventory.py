from django.views.generic import CreateView
from ..forms import ScreenInventoryForm
from ..models import Screen, ScreensInventory
from ..services import add_screen_inventory
from .mixins import ScreenFormMixin

class ScreenAddInventoryView(ScreenFormMixin, CreateView):
    model = ScreensInventory
    form_class = ScreenInventoryForm
    template_name = "partials/screen-add.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.pop('instance', None)
        return kwargs

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        screen_obj = Screen.objects.get(pk=self.kwargs.get('pk'))
        
        if self.request.method != 'POST':
            form.initial = {
                'name': screen_obj.name,
                'quantity': '',
                'price': '',
                'screen_type': None
            }
            form.data = {}
        return form

    def get_initial(self):
        initial = super().get_initial()
        screen_obj = Screen.objects.get(pk=self.kwargs.get('pk'))
        initial['name'] = screen_obj.name
        initial['quantity'] = ''
        initial['price'] = ''
        initial['screen_type'] = None
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        screen_obj = Screen.objects.get(pk=self.kwargs.get('pk'))
        context['subtitle'] = f"Añadir inventario para: {screen_obj.name}"
        context['screen'] = screen_obj  # <-- IMPORTANTE: Esto resuelve el error de URL
        return context

    def form_valid(self, form):
        try:
            screen_id = self.kwargs.get('pk')
            
            self.object = add_screen_inventory(
                screen_id=screen_id,
                screen_type_id=form.cleaned_data["screen_type"].id,
                quantity=form.cleaned_data.get("quantity"),
                price=form.cleaned_data.get("price"),
            )

            if not self.object:
                form.add_error(None, "No se pudo registrar el nuevo inventario.")
                return self.form_invalid(form)

            response = self.handle_create_success()
            if response:
                return response

            return super().form_valid(form)

        except Exception as e:
            form.add_error(None, f"Error al registrar inventario: {str(e)}")
            return self.form_invalid(form)

    def form_invalid(self, form):
        return self.handle_form_invalid(
            form=form,
            obj=None,
        )