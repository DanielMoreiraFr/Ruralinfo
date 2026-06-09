from django.urls import path
from . import views

app_name = 'mural'

urlpatterns = [
    # Mural Principal
    path('', views.index, name='index'),
    path('novo/', views.criar, name='criar'),
    path('<int:pk>/editar/', views.editar, name='editar'),
    path('<int:pk>/deletar/', views.deletar, name='deletar'),
    path('<int:pk>/toggle/', views.toggle_publicado, name='toggle'),
    path('horarios/', views.horarios, name='horarios'),

    # Sugestões
    path('sugestoes/nova/', views.sugestao_nova, name='sugestao_nova'),
    path('sugestoes/', views.sugestoes_pendentes, name='sugestoes_pendentes'),
    path('sugestoes/arquivadas/', views.sugestoes_arquivadas, name='sugestoes_arquivadas'),
    path('sugestoes/<int:pk>/aceitar/', views.sugestao_aceitar, name='sugestao_aceitar'),
    path('sugestoes/<int:pk>/negar/', views.sugestao_negar, name='sugestao_negar'),
]