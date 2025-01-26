# fuel_optimizer_api/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('optimize_route/', views.optimize_route, name='optimize_route'),
]
