from django.views.generic import CreateView, UpdateView
from ..forms import ScreenForm, ScreenInventoryForm,ScreenUpdateForm
from ..models import Screen, ScreensInventory
from ..services import create_screen, update_screen, add_screen_inventory
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


class ScreenUpdateView(ScreenFormMixin, UpdateView):
    model = Screen
    form_class = ScreenUpdateForm
    template_name = "partials/screen-form.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['screen'] = self.get_object()
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        try:
            inventory = self.get_object().inventory_records.order_by('-id').first()
            if inventory:
                initial["price"] = inventory.price
                initial["quantity"] = inventory.quantity
                initial["screen_inventory"] = inventory
        except Exception:
            pass
        return initial

    def form_valid(self, form):
        try:
            current_obj = self.get_object()
            selected_inventory = form.cleaned_data.get("screen_inventory")
            quantity = form.cleaned_data.get("quantity")
            price = form.cleaned_data.get("price")

            # Actualizamos pasando el ID del registro de inventario específico seleccionado en el select
            self.object = update_screen(
                screen_id=current_obj.id,
                name=form.cleaned_data.get("name"),
                # Si tu función de servicio acepta el ID del registro de inventario específico:
                screens_inventory_id=selected_inventory.id if selected_inventory else None,
                screen_type_id=selected_inventory.screen_type.id if selected_inventory else None,
                quantity=quantity,
                price=price,
            )

            if not self.object:
                form.add_error(None, "No se pudo actualizar la pantalla y su inventario.")
                return self.form_invalid(form)

            response = self.handle_update_success()
            if response:
                return response

            return super().form_valid(form)

        except Exception as e:
            form.add_error(None, f"Error al actualizar: {str(e)}")
            return self.form_invalid(form)

    def form_invalid(self, form):
        return self.handle_form_invalid(
            form=form,
            obj=self.get_object(),
        )


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