from django.urls import path
from . import views

app_name = 'mural'

urlpatterns = [
    path('', views.index, name='index'),
    path('novo/', views.criar, name='criar'),
    path('<int:pk>/editar/', views.editar, name='editar'),
    path('<int:pk>/deletar/', views.deletar, name='deletar'),
    path('<int:pk>/toggle/', views.toggle_publicado, name='toggle'),
    path('horarios/', views.horarios, name='horarios'),
]