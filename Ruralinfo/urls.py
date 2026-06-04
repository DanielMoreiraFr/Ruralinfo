from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect



urlpatterns = [
    path('admin/',     admin.site.urls),
    path('accounts/',  include('accounts.urls', namespace='accounts')),
    path('mural/',     include('mural.urls',    namespace='mural')),
    path('',           lambda r: redirect('mural:index'), name='home'), # lambda simplfica o redirect
]
