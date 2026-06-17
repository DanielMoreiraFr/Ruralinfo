from django.urls import path
from . import views

app_name = 'circular'

urlpatterns = [
    path('horarios/', views.horarios, name='horarios'),
    path('api/ao-vivo/', views.api_circular_ao_vivo, name='api_circular_ao_vivo'),
]