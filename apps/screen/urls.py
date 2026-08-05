from django.urls import path

# Correcto: se importa directamente desde la carpeta/paquete views
from .views import (
    ScreenListView,
    ScreenCreateView,
    ScreenUpdateView,
    ScreenAddInventoryView,
)

app_name = "screen"

urlpatterns = [
    path("", ScreenListView.as_view(), name="list"),
    path("table/", ScreenListView.as_view(), name="table"),
    path("create/", ScreenCreateView.as_view(), name="create"),
    path("edit/<int:pk>/", ScreenUpdateView.as_view(), name="edit"),
    path("add-inventory/<int:pk>/", ScreenAddInventoryView.as_view(), name="add-inventory"),
]