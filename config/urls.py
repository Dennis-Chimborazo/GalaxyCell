# from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', include('apps.login.urls')),
    path('dashboard/', include('apps.dashboard.urls')),
    path('screen/', include('apps.screen.urls')),
    path('client/', include('apps.client.urls')),
]
