from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    path('admin/',     admin.site.urls),
    path('accounts/',  include('accounts.urls', namespace='accounts')),
    path('mural/',     include('mural.urls',    namespace='mural')),
    # Raiz → mural (visitante por padrão, igual ao botão "Visitante" do legado)
    path('',           lambda r: redirect('mural:index'), name='home'),
]

# Serving de mídia em desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)