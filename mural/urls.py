from django.urls import path
from . import views

app_name = 'mural'

urlpatterns = [
    # Lista principal (feed)
    path('',              views.mural_lista,    name='lista'),
    # Detalhe de um aviso
    path('<int:pk>/',     views.aviso_detalhe,  name='detalhe'),
    # CRUD — restrito a ADMIN via @admin_required
    path('novo/',         views.aviso_criar,    name='criar'),
    path('<int:pk>/editar/',  views.aviso_editar,   name='editar'),
    path('<int:pk>/deletar/', views.aviso_deletar,  name='deletar'),
]