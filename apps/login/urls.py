from django.urls import path
from .views import LoginScreenView, LoginProcessView,LogoutView

app_name = 'login'

urlpatterns = [
    path('', LoginScreenView.as_view(), name='login'),
    path('process/', LoginProcessView.as_view(), name='login-process'),
    path('logout/', LogoutView.as_view(), name='logout'),
]