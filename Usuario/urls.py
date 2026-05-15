from django.urls import path
from . import views

app_name = 'usuario'

urlpatterns = [
    path('cadastrar/', views.usuario_cadastrar, name='cadastrar'),
]
