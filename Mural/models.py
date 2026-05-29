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