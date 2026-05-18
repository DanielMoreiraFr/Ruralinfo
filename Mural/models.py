from django.db import models
from django.conf import settings


class Aviso(models.Model):
    """
    Substitui a tabela `infos` do SQLite legado.

    EQUIVALÊNCIA COM O LEGADO:
        mensagem  → conteudo (TextField)
        img_url   → imagem   (ImageField — upload real, melhor prática)
        alt       → alt_texto
        data      → data_criacao (auto_now_add)
        estado    → publicado (BooleanField)

    NOVIDADES EM RELAÇÃO AO LEGADO:
        categoria → organização por tipo de aviso (não havia no legado)
        autor     → ForeignKey para auditoria interna (não havia no legado)
        data_atualizacao → registra edições (não havia no legado)
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

    # Cores Bootstrap associadas a cada categoria — usadas diretamente
    # nos templates sem precisar de lógica extra
    CATEGORIA_BADGE = {
        'aviso_geral':  'secondary',
        'evento':       'primary',
        'academico':    'info',
        'oportunidade': 'success',
        'extensao':     'teal',     # via CSS customizado
        'pesquisa':     'purple',   # via CSS customizado
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
        upload_to='mural/%Y/%m/',  # organiza por ano/mês — melhor prática
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

    # ForeignKey para auditoria — equivale ao campo `id` que o legado
    # associava manualmente na sessão após o login
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Autor',
        on_delete=models.PROTECT,  # não deixa deletar admin com posts
        related_name='avisos',
    )

    data_criacao = models.DateTimeField(
        verbose_name='Criado em',
        auto_now_add=True,  # equivale ao `datetime.now()` do legado
    )

    data_atualizacao = models.DateTimeField(
        verbose_name='Atualizado em',
        auto_now=True,
    )

    # Equivale ao campo `estado` do legado (1=ativo, 0=inativo)
    # Permite ocultar sem deletar — lógica solicitada
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
        return f"[{status}] {self.get_categoria_display()} — {self.conteudo[:60]}"

    @property
    def badge_class(self):
        """Retorna a classe Bootstrap do badge de categoria."""
        return self.CATEGORIA_BADGE.get(self.categoria, 'secondary')