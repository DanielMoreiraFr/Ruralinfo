from django.contrib import admin
from .models import Aviso


@admin.register(Aviso)
class AvisoAdmin(admin.ModelAdmin):
    list_display    = ('conteudo_resumo', 'categoria', 'autor', 'publicado', 'data_criacao')
    list_filter     = ('categoria', 'publicado', 'data_criacao')
    search_fields   = ('conteudo', 'autor__email')
    readonly_fields = ('data_criacao', 'data_atualizacao')
    list_editable   = ('publicado',)  # toggle rápido no painel

    @admin.display(description='Conteúdo')
    def conteudo_resumo(self, obj):
        return obj.conteudo[:80] + '...' if len(obj.conteudo) > 80 else obj.conteudo