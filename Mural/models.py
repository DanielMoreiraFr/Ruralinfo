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

    # pre declaração das cores dos tipos de avisos
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
        upload_to='mural/%Y/%m/', # mudar o formato da data pra ficar mais organizado br
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

    # config da FK pro user, usa AUTH_USER_MODEL pra ser compatível com o modelo customizado
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Autor',
        on_delete=models.PROTECT,  # não deixa deletar admin com posts
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
    # Permite ocultar sem deletar o aviso
    # pra poder editar com calma e publicar depois
    publicado = models.BooleanField(
        verbose_name='Publicado',
        default=True,
        help_text='Desmarque para ocultar o aviso sem deletá-lo.',
    )

    # validação pra garantir que alt_texto seja obrigatório se imagem for fornecida
    class Meta:
        verbose_name = 'Aviso'
        verbose_name_plural = 'Avisos'
        ordering = ['-data_criacao']

    def __str__(self):
        status = '✓' if self.publicado else '○'
        return f"[{status}] {self.get_categoria_display()} — {self.conteudo[:60]}"

    # prop pra estabilizar categoria do badge mesmo que o nome da categoria mude
    @property
    def badge_class(self):
        """Retorna a classe Bootstrap do badge de categoria."""
        return self.CATEGORIA_BADGE.get(self.categoria, 'secondary')