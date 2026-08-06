from django.views.generic import UpdateView
from django.template.response import TemplateResponse
from ..forms import ScreenUpdateForm
from ..models import Screen
from ..services import update_screen
from .mixins import ScreenFormMixin

class ScreenUpdateView(ScreenFormMixin, UpdateView):
    model = Screen
    form_class = ScreenUpdateForm
    template_name = "partials/screen-update.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        
        # Si es una petición HTMX al cambiar el select, devolvemos únicamente el partial con los campos
        if request.headers.get('HX-Request') and 'screen_inventory' in request.GET:
            return TemplateResponse(request, "partials/screen-price-quantity.html", {'form': form, 'object': self.object})
            
        return super().get(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['screen'] = self.get_object()
        
        if self.request.GET and 'screen_inventory' in self.request.GET:
            data = self.request.GET.copy()
            if not data.get('name'):
                data['name'] = self.get_object().name
            kwargs['data'] = data
            
        return kwargs

    def form_valid(self, form):
        try:
            current_obj = self.get_object()
            selected_inventory = form.cleaned_data.get("screen_inventory")
            
            self.object = update_screen(
                screen_id=current_obj.id,
                name=form.cleaned_data.get("name"),
                screens_inventory_id=selected_inventory.id if selected_inventory else None,
                screen_type_id=selected_inventory.screen_type.id if selected_inventory else None,
                quantity=form.cleaned_data.get("quantity"),
                price=form.cleaned_data.get("price"),
            )
            
            response = self.handle_update_success()
            return response if response else super().form_valid(form)
        except Exception as e:
            form.add_error(None, f"Error: {str(e)}")
            return self.form_invalid(form)

    def form_invalid(self, form):
        return self.handle_form_invalid(form=form, obj=self.get_object())