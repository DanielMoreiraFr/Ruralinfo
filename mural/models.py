from django.db import models
from django.conf import settings


class Aviso(models.Model):
    """
    Representa as publicações oficiais enviadas por Administradores no mural.
    """

    CATEGORIA_CHOICES = [
        ('aviso_geral',  'Aviso Geral'),
        ('evento',       'Evento'),
        ('academico',    'Acadêmico'),
        ('oportunidade', 'Oportunidade'),
        ('extensao',     'Extensão'),
        ('pesquisa',     'Pesquisa'),
        ('manutencao',   'Manutenção'),
        ('urgente',      'Urgente'),
    ]

    CATEGORIA_BADGE = {
        'aviso_geral':  'secondary',
        'evento':       'primary',
        'academico':    'info',
        'oportunidade': 'success',
        'extensao':     'teal',
        'pesquisa':     'purple',
        'manutencao':   'warning',
        'urgente':      'danger',
    }

    titulo = models.CharField(
        verbose_name='Título',
        max_length=150,
        blank=False,
        null=False,
        default=''
    )

    conteudo = models.TextField(
        verbose_name='Conteúdo',
        blank=False,
    )

    categoria = models.CharField(
        verbose_name='Categoria',
        max_length=20,
        choices=CATEGORIA_CHOICES,
        default='aviso_geral',
    )

    # Configura o upload de mídias estruturando pastas dinâmicas por Ano/Mês no servidor
    imagem = models.ImageField(
        verbose_name='Imagem',
        upload_to='mural/%Y/%m/', 
        null=True,
        blank=True,
    )

    alt_texto = models.CharField(
        verbose_name='Texto Alternativo (acessibilidade)',
        max_length=255,
        null=True,
        blank=True,
        help_text='Descreva a imagem para leitores de tela.',
    )

    # Chave estrangeira (N:1): PROTECT impede a exclusão do administrador se ele tiver avisos vinculados
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Autor',
        on_delete=models.PROTECT,
        related_name='avisos',
    )

    # Grava o timestamp exato de forma automática apenas no momento de inserção do registro
    data_criacao = models.DateTimeField(
        verbose_name='Criado em',
        auto_now_add=True,
    )

    # Atualiza o timestamp de forma automática toda vez que o método save() for acionado
    data_atualizacao = models.DateTimeField(
        verbose_name='Atualizado em',
        auto_now=True,
    )

    publicado = models.BooleanField(
        verbose_name='Publicado',
        default=True,
        help_text='Desmarque para ocultar o aviso sem deletá-lo.',
    )

    # Configurações de metadados internos e ordenação padrão da tabela no banco
    class Meta:
        verbose_name = 'Aviso'
        verbose_name_plural = 'Avisos'
        # Traz as publicações mais recentes primeiro no topo do mural
        ordering = ['-data_criacao']

    # Define a visualização textual curta do objeto no painel de administração do Django
    def __str__(self):
        status = '✓' if self.publicado else '○'
        # get_categoria_display() traduz o valor do banco para o rótulo amigável legível
        return f"[{status}] {self.get_categoria_display()} — {self.titulo}"

    # Cria um método acessível como se fosse um atributo comum do objeto para facilitar o uso no HTML
    @property
    def badge_class(self):
        """Retorna a classe Bootstrap correspondente ao badge de cor da categoria."""
        return self.CATEGORIA_BADGE.get(self.categoria, 'secondary')
    

class Sugestao(models.Model):
    """
    Representa as propostas enviadas por usuários para análise prévia da moderação.
    """

    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('aceita',   'Aceita'),
        ('negada',   'Negada'),
    ]

    CATEGORIA_CHOICES = [
        ('aviso_geral',  'Aviso Geral'),
        ('evento',       'Evento'),
        ('academico',    'Acadêmico'),
        ('oportunidade', 'Oportunidade'),
        ('extensao',     'Extensão'),
        ('pesquisa',     'Pesquisa'),
        ('manutencao',   'Manutenção'),
        ('urgente',      'Urgente'),
    ]

    # Chave estrangeira (N:1): CASCADE remove todas as sugestões do usuário caso ele exclua a conta
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sugestoes',
        verbose_name='Autor',
    )

    texto = models.TextField(
        verbose_name='Texto da Sugestão',
        help_text='Descreva o acontecimento ou pauta que deseja sugerir.',
    )

    categoria = models.CharField(
        verbose_name='Categoria Sugerida',
        max_length=20,
        choices=CATEGORIA_CHOICES,
        default='aviso_geral',
    )

    status = models.CharField(
        verbose_name='Status',
        max_length=10,
        choices=STATUS_CHOICES,
        default='pendente',
    )

    criado_em = models.DateTimeField(
        verbose_name='Enviado em',
        auto_now_add=True,
    )

    # Armazena o momento exato em que a sugestão foi arquivada para possibilitar rotinas automáticas de expiração
    arquivado_em = models.DateTimeField(
        verbose_name='Arquivado em',
        null=True,
        blank=True,
        help_text='Preenchido automaticamente ao negar.',
    )

    # Configurações de exibição de nomes e organização das listagens
    class Meta:
        verbose_name = 'Sugestão'
        verbose_name_plural = 'Sugestões'
        ordering = ['-criado_em']

    # Define a exibição reduzida limitando a string do conteúdo para não quebrar tabelas do Admin
    def __str__(self):
        return f"[{self.get_status_display()}] {self.autor.nome_completo} — {self.texto[:60]}"