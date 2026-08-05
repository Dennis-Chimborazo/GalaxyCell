from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login, logout
from django.shortcuts import redirect, render
from django.views import View

from .forms import AuthForm


class LoginScreenView(View):
    form_class = AuthForm
    template_name = "layouts/login.html"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("/dashboard/")

        return render(request, self.template_name, {
            "form": self.form_class()
        })


class LoginProcessView(View):
    form_class = AuthForm
    template_name = "partials/login-form.html"

    def post(self, request):
        # Pasamos request al AuthenticationForm para que gestione la sesión internamente
        form = self.form_class(data=request.POST, request=request)
        
        if form.is_valid():
            # El formulario ya autenticó las credenciales con éxito en is_valid()
            user = form.get_user()
            if user:
                login(request, user)
                messages.success(request, f"Bienvenido {user.username}")
                
                # Respuesta HTMX exitosa para redirección completa de la ventana
                response = HttpResponse()
                response["HX-Redirect"] = "/dashboard/"
                return response

        errors_de_campo = form.errors.get("__all__") or form.errors.get("password") or form.errors.get("username")
        if errors_de_campo:
            messages.error(request, "Usuario o contraseña incorrectos.")

        # Retorna el parcial con el formulario que contiene los errores automáticos de Django
        return render(request, self.template_name, {
            "form": form
        })


class LogoutView(View):
    """Cierra la sesión de forma segura y redirige al login manejando peticiones normales y HTMX."""

    def post(self, request):
        logout(request)
        
        if request.headers.get("HX-Request"):
            response = HttpResponse()
            response["HX-Redirect"] = "/"
            return response
            
        return redirect("/")