from django.db import models
from django.conf import settings

class Aviso(models.Model):
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

    # Novo campo adicionado aqui
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

    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Autor',
        on_delete=models.PROTECT,
        related_name='avisos',
    )

    data_criacao = models.DateTimeField(
        verbose_name='Criado em',
        auto_now_add=True,
    )

    data_atualizacao = models.DateTimeField(
        verbose_name='Atualizado em',
        auto_now=True,
    )

    publicado = models.BooleanField(
        verbose_name='Publicado',
        default=True,
        help_text='Desmarque para ocultar o aviso sem deletá-lo.',
    )

    class Meta:
        verbose_name = 'Aviso'
        verbose_name_plural = 'Avisos'
        ordering = ['-data_criacao']

    def __str__(self):
        status = '✓' if self.publicado else '○'
        # Atualizado para mostrar o título no painel admin
        return f"[{status}] {self.get_categoria_display()} — {self.titulo}"

    @property
    def badge_class(self):
        """Retorna a classe Bootstrap do badge de categoria."""
        return self.CATEGORIA_BADGE.get(self.categoria, 'secondary')
    

class Sugestao(models.Model):
    """
    Sugestão de pauta enviada por usuários logados (COMUM ou ADMIN).
    Admins podem aceitar (leva para criar post) ou negar (arquiva).

    O campo `arquivado_em` é preenchido automaticamente ao negar,
    servindo de base para uma futura limpeza automática por tempo.
    """

    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('aceita',   'Aceita'),
        ('negada',   'Negada'),
    ]

    # Reutiliza as mesmas categorias do Aviso para consistência
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

    arquivado_em = models.DateTimeField(
        verbose_name='Arquivado em',
        null=True,
        blank=True,
        help_text='Preenchido automaticamente ao negar.',
    )

    # campo de manipulçao dos nomes do painel de admin
    class Meta:
        verbose_name = 'Sugestão'
        verbose_name_plural = 'Sugestões'
        ordering = ['-criado_em']

    def __str__(self):
        return f"[{self.get_status_display()}] {self.autor.nome_completo} — {self.texto[:60]}"