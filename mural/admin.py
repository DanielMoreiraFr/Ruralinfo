from django.contrib import admin
from .models import Aviso


@admin.register(Aviso)
class AvisoAdmin(admin.ModelAdmin):
    list_display  = ('titulo', 'categoria', 'autor', 'data_criacao')
    list_filter   = ('categoria', 'data_criacao')
    search_fields = ('titulo', 'conteudo', 'autor__email')
    readonly_fields = ('data_criacao', 'data_atualizacao')
    date_hierarchy = 'data_criacao'

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Somente na criação via admin
            obj.autor = request.user
        super().save_model(request, obj, form, change)