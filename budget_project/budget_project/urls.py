from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('budget/', include('budget_app.urls')), # Celuje w plik urls w aplikacji
    path('accounts/', include('django.contrib.auth.urls')), # Celuje we wbudowane logowanie
]