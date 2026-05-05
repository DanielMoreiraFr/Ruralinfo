"""
ruralinfo/urls.py — Roteador principal do projeto.

Cada app tem seu próprio urls.py com namespace.
Aqui apenas incluímos esses sub-roteadores e configuramos
o serving de mídia em desenvolvimento.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    # Painel administrativo do Django
    path('admin/', admin.site.urls),

    # App de autenticação — /accounts/login/, /accounts/cadastro/, etc.
    path('accounts/', include('accounts.urls', namespace='accounts')),

    # App do mural — /mural/ (lista), /mural/novo/, /mural/<pk>/editar/, etc.
    path('mural/', include('mural.urls', namespace='mural')),

    # Redireciona a raiz do site para o mural (ou login se não autenticado)
    path('', lambda req: redirect('mural:lista'), name='home'),
]

# ============================================================
# SERVING DE MÍDIA EM DESENVOLVIMENTO
#
# Em produção, o Nginx/Apache serve os arquivos de /media/ diretamente.
# Em desenvolvimento, o servidor embutido do Django precisa servir
# esses arquivos — o static() abaixo configura isso automaticamente
# quando DEBUG=True.
# ============================================================
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)