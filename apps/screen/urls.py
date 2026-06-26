from django.urls import path
from .views import ScreenListView,ScreenCreateView,ScreenUpdateView

app_name = "screen"

urlpatterns = [
    path("", ScreenListView.as_view(), name="list"),
    path("table/", ScreenListView.as_view(), name="table"),
    path("create/", ScreenCreateView.as_view(), name="create"),
    path("edit/<uuid:pk>/", ScreenUpdateView.as_view(), name="edit"),
]