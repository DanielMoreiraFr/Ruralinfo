from django.urls import path
from . import views

app_name = 'circular'

urlpatterns = [
    path('horarios/', views.horarios, name='horarios'),
]