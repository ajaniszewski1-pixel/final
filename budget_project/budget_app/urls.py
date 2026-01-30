from django.urls import path
from . import views
from .views import BudgetSummaryAPI, BudgetTrendsAPI

urlpatterns = [
    path('api/budget/summary/', BudgetSummaryAPI.as_view(), name='api-summary'),
    path('api/budget/trends/', BudgetTrendsAPI.as_view(), name='api-trends'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('wydatek/usun/<int:pk>/', views.usun_wydatek, name='usun_wydatek'),
]