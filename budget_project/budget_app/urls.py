from django.urls import path
from . import views

urlpatterns = [
    # Zmień 'views.welcome' na 'views.dashboard'
    path('', views.dashboard, name='dashboard'), 
    path('dashboard/', views.dashboard, name='dashboard'),
]