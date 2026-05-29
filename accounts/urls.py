from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/',    views.login_view,    name='login'),
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('logout/',   views.logout_view,   name='logout'),
    path('perfil/',   views.perfil_view,   name='perfil'),
    path('perfil/deletar/', views.deletar_conta_view, name='deletar_conta'),
]