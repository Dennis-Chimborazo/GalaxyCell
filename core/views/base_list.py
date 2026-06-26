# core/views/base_list.py

from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView


class BaseTableListView(ListView):
    full_template = None
    partial_template = None

    list_url_name = None
    table_url_name = None

    search_param = "search"

    refresh_message = "Información actualizada"

    def get_template_names(self):
        if not self.request.headers.get("HX-Request"):
            return [self.full_template]

        if self.request.resolver_match.url_name == "table":
            if self.request.GET.get("action") == "refresh":
                messages.success(
                    self.request,
                    self.refresh_message
                )

            return ["components/data-table.html"]

        return [self.partial_template]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        search_val = self.request.GET.get(
            self.search_param,
            ""
        )

        page_obj = context.get("page_obj")
        queryset = page_obj.object_list if page_obj else []

        context.update(
            self.get_table_context(
                queryset=queryset,
                request=self.request
            )
        )

        context.update({
            "query_params": (
                f"{self.search_param}={search_val}"
                if search_val else ""
            ),
            "list_url": reverse_lazy(self.list_url_name),
            "table_url": reverse_lazy(self.table_url_name),
            "table_id": "table-results",
        })

        return context