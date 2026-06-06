from django.contrib import admin
from .models import LocalRural, ImagemLocal, Avaliacao, Comentario


class ImagemLocalInline(admin.TabularInline):
    """
    Permite adicionar várias fotos da galeria diretamente
    na página de edição do local — sem precisar entrar em outra tela.
    """
    model = ImagemLocal
    extra = 3          # exibe 3 linhas vazias prontas para preenchimento
    fields = ('imagem', 'legenda', 'ordem')
    ordering = ('ordem',)


@admin.register(LocalRural)
class LocalRuralAdmin(admin.ModelAdmin):
    list_display  = ('nome', 'media_avaliacoes', 'total_avaliacoes', 'total_comentarios', 'criado_em')
    search_fields = ('nome', 'descricao')
    readonly_fields = ('criado_em', 'atualizado_em')
    inlines = [ImagemLocalInline]

    fieldsets = (
        (None, {
            'fields': ('nome', 'descricao', 'imagem_principal')
        }),
        ('Datas', {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',),
        }),
    )

    @admin.display(description='Média ★')
    def media_avaliacoes(self, obj):
        media = obj.media_avaliacoes
        return f'{media} ★' if media else '—'

    @admin.display(description='Avaliações')
    def total_avaliacoes(self, obj):
        return obj.total_avaliacoes

    @admin.display(description='Comentários')
    def total_comentarios(self, obj):
        return obj.total_comentarios


@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display  = ('usuario', 'local', 'nota', 'atualizado_em')
    list_filter   = ('local', 'nota')
    search_fields = ('usuario__nome_completo', 'local__nome')
    readonly_fields = ('atualizado_em',)


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display  = ('autor', 'local', 'pai', 'conteudo_resumo', 'criado_em')
    list_filter   = ('local',)
    search_fields = ('autor__nome_completo', 'conteudo')
    readonly_fields = ('criado_em',)

    @admin.display(description='Comentário')
    def conteudo_resumo(self, obj):
        return obj.conteudo[:80] + '...' if len(obj.conteudo) > 80 else obj.conteudo