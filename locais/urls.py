from django.urls import path
from . import views

app_name = 'locais'

urlpatterns = [
    path('', views.lista_locais, name='lista'), # Grid de todos os locais
    path('<int:pk>/', views.detalhe_local, name='detalhe'), # Página de detalhe de um local
    path('<int:pk>/avaliar/', views.avaliar_local, name='avaliar'),
    path('<int:pk>/comentar/', views.comentar_local, name='comentar'),
    path('<int:pk>/comentar/<int:comentario_pk>/responder/', views.responder_comentario, name='responder'),
    path('<int:pk>/comentar/<int:comentario_pk>/deletar/', views.deletar_comentario, name='deletar_comentario'),
    path('novo/', views.criar_local, name='criar'),
    path('<int:pk>/editar/', views.editar_local, name='editar'),
    path('<int:pk>/deletar/', views.deletar_local, name='deletar'),
]