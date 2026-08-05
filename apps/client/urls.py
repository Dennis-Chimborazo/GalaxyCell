from django.urls import path
from .views import ClientListView,ClientCreateView,ClientUpdateView

app_name = "client"

urlpatterns = [
    path("", ClientListView.as_view(), name="list"),
    path("table/", ClientListView.as_view(), name="table"),
    path("create/", ClientCreateView.as_view(), name="create"),
    path("edit/<int:pk>/", ClientUpdateView.as_view(), name="edit"),
]