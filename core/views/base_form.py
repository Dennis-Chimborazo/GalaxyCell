# core/views/base_form.py

import json

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render


class BaseFormMixin:

    module_name = None

    create_success_message = (
        "Registro creado correctamente."
    )

    update_success_message = (
        "Registro actualizado correctamente."
    )

    def is_htmx(self):
        return self.request.headers.get(
            "HX-Request"
        )

    def get_form_context(
        self,
        form,
        obj=None,
    ):
        return {
            "form": form,
            "object": obj,
        }

    def render_htmx_form(
        self,
        form,
        obj=None,
    ):
        return render(
            self.request,
            self.template_name,
            self.get_form_context(
                form,
                obj,
            ),
        )

    def get_htmx_success_response(self):

        response = HttpResponse()

        response["HX-Trigger"] = json.dumps(
            {
                "refreshTable": True,
                "close-modal": True,
            }
        )

        return response

    def handle_form_invalid(
        self,
        form,
        obj=None,
    ):
        if self.is_htmx():
            return self.render_htmx_form(
                form=form,
                obj=obj,
            )

        return super().form_invalid(form)

    def handle_create_success(self):

        messages.success(
            self.request,
            self.create_success_message,
        )

        if self.is_htmx():
            return self.get_htmx_success_response()

        return None

    def handle_update_success(self):

        messages.success(
            self.request,
            self.update_success_message,
        )

        if self.is_htmx():
            return self.get_htmx_success_response()

        return None