from django.urls import reverse_lazy


class BaseTableMixin:
    headers = []
    fields = []

    create_url = None
    list_url = None
    table_url = None
    edit_url_name = None

    context_name = None

    def get_table_context(
        self,
        queryset=None,
        request=None,
    ):
        context = {
            "rows": queryset,
            "headers": self.headers,
            "fields": self.fields,
            "table_id": "table-results",
            "has_actions": True,
            "edit_url_name": self.edit_url_name,
        }

        if self.list_url:
            context["list_url"] = reverse_lazy(
                self.list_url
            )

        if self.table_url:
            context["table_url"] = reverse_lazy(
                self.table_url
            )

        if self.create_url:
            context["create_url"] = reverse_lazy(
                self.create_url
            )

        if self.context_name:
            context[self.context_name] = queryset

        return context