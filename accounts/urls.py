from django.urls import path
from . import views
 
app_name = 'accounts'
 
urlpatterns = [
    path('login/',          views.login_view,           name='login'),
    path('logout/',         views.logout_view,          name='logout'),
    path('cadastro/',       views.cadastro_view,        name='cadastro'),
    path('verificar/',      views.verificar_codigo_view, name='verificar_codigo'),
    path('perfil/',         views.perfil_view,          name='perfil'),
    path('deletar-conta/',  views.deletar_conta_view,   name='deletar_conta'),
]