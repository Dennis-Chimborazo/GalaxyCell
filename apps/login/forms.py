from django import forms
from django.contrib.auth.forms import AuthenticationForm

class AuthForm(AuthenticationForm):
    """Formulario de autenticación limpio delegando el diseño a los componentes UI."""
    
    username = forms.CharField(
        label="Usuario",
        widget=forms.TextInput()
    )
    
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput()
    )