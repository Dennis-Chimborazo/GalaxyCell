from django.urls import path

from .views import (
 SalesListView
)

app_name = "sales"

urlpatterns = [
    path("", SalesListView.as_view(), name="list"),
    path("table/", SalesListView.as_view(), name="table"),
]