from django.contrib import admin
from .models import Aviso


# Registra o modelo Aviso no site de administração do Django utilizando o decorador de classe
@admin.register(Aviso)
class AvisoAdmin(admin.ModelAdmin):
    # Define quais colunas serão exibidas na tabela de listagem do painel
    list_display    = ('conteudo_resumo', 'categoria', 'autor', 'publicado', 'data_criacao')
    # Adiciona uma barra lateral de filtros para segmentar os registros rapidamente
    list_filter     = ('categoria', 'publicado', 'data_criacao')
    # Ativa uma barra de pesquisa que busca no texto do conteúdo ou pelo e-mail do autor (relacionamento N:1)
    search_fields   = ('conteudo', 'autor__email')
    # Bloqueia a edição destes campos no formulário do admin, pois são gerenciados automaticamente pelo banco
    readonly_fields = ('data_criacao', 'data_atualizacao')
    # Permite alterar o status de publicação diretamente pela tabela de listagem, sem precisar abrir o registro
    list_editable   = ('publicado',)  # toggle rápido no painel

    # Define um método customizado para exibir um texto amigável na coluna do admin
    @admin.display(description='Conteúdo')
    def conteudo_resumo(self, obj):
        """
        Garante que textos muito longos não quebrem o layout da tabela,
        limitando a exibição aos primeiros 80 caracteres seguidos de reticências.
        """
        return obj.conteudo[:80] + '...' if len(obj.conteudo) > 80 else obj.conteudo