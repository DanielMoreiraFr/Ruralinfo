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
    # Configura as colunas da tabela de listagem incluindo propriedades agregadas do modelo
    list_display  = ('nome', 'media_avaliacoes', 'total_avaliacoes', 'total_comentarios', 'criado_em')
    # Ativa o campo de busca textual mapeando o nome e a descrição do local
    search_fields = ('nome', 'descricao')
    # Protege os campos de data gerenciados automaticamente pelo banco de dados contra edições manuais
    readonly_fields = ('criado_em', 'atualizado_em')
    
    # Vincula o formulário em linha da galeria de imagens na mesma página de edição do LocalRural
    inlines = [ImagemLocalInline]
    # Organiza visualmente os campos do formulário de edição em seções colapsáveis ou agrupadas
    fieldsets = (
        (None, {
            'fields': ('nome', 'descricao', 'imagem_principal')
        }),
        ('Datas', {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',), # Oculta a seção por padrão sob um botão de "Mostrar"
        }),
    )

    # Formata a exibição da média de estrelas calculada no modelo para incluir o caractere '★'
    @admin.display(description='Média ★')
    def media_avaliacoes(self, obj):
        media = obj.media_avaliacoes
        return f'{media} ★' if media else '—'

    # Retorna o total de avaliações recebidas por este local específico
    @admin.display(description='Avaliações')
    def total_avaliacoes(self, obj):
        return obj.total_avaliacoes

    # Retorna o total de comentários vinculados a este local específico
    @admin.display(description='Comentários')
    def total_comentarios(self, obj):
        return obj.total_comentarios


@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    # Configura as colunas exibidas para o gerenciamento de notas atribuídas pelos usuários
    list_display  = ('usuario', 'local', 'nota', 'atualizado_em')
    # Filtros laterais focados na separação por nota numérica e por local físico avaliado
    list_filter   = ('local', 'nota')
    # Permite buscar pelo nome do avaliador (através da relação N:1) ou diretamente pelo nome do local
    search_fields = ('usuario__nome_completo', 'local__nome')
    readonly_fields = ('atualizado_em',)


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    # Exibe as informações do autor, local, relação de resposta (pai), conteúdo limitado e data
    list_display  = ('autor', 'local', 'pai', 'conteudo_resumo', 'criado_em')
    list_filter   = ('local',)
    # Permite fazer buscas textuais filtrando pelo nome do autor ou pelo conteúdo digitado
    search_fields = ('autor__nome_completo', 'conteudo')
    readonly_fields = ('criado_em',)

    # Método para truncar e limitar o tamanho do texto do comentário exibido na listagem principal
    @admin.display(description='Comentário')
    def conteudo_resumo(self, obj):
        """
        Garante que comentários extensos não quebrem as linhas da tabela,
        mostrando apenas os primeiros 80 caracteres seguidos por reticências.
        """
        return obj.conteudo[:80] + '...' if len(obj.conteudo) > 80 else obj.conteudo