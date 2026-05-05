from django.db import models
from django.conf import settings


class Aviso(models.Model):
    """
    Model central do app Mural — representa uma publicação no feed.

    POR QUE ForeignKey para settings.AUTH_USER_MODEL e não para Usuario diretamente?
    Usar settings.AUTH_USER_MODEL é a forma recomendada pelo Django para referenciar
    o model de usuário customizado. Se referenciarmos 'accounts.Usuario' diretamente,
    criamos um acoplamento forte entre apps. Usando settings, o app mural fica
    desacoplado — poderia ser usado em outro projeto com outro model de usuário.

    RASTREIO VIA ID:
    A FK garante o rastreio por ID (chave primária), não por nome ou email.
    Se o usuário mudar o nome ou email, o aviso continua vinculado à mesma
    pessoa. O on_delete=PROTECT impede que um admin seja deletado enquanto
    tiver avisos associados — forçando uma decisão consciente (reatribuir ou
    deletar os avisos primeiro).
    """

    CATEGORIA_CHOICES = [
        ('evento',       'Evento'),
        ('aviso_geral',  'Aviso Geral'),
        ('oportunidade', 'Oportunidade'),
        ('manutencao',   'Manutenção'),
        ('urgente',      'Urgente'),
    ]

    titulo = models.CharField(
        verbose_name='Título',
        max_length=200,
        blank=False,
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
        upload_to='mural/imagens/%Y/%m/',  # Organiza por ano/mês para evitar pastas gigantes
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
        on_delete=models.PROTECT,   # Não deixa deletar o usuário se tiver avisos
        related_name='avisos',
    )

    data_criacao = models.DateTimeField(
        verbose_name='Publicado em',
        auto_now_add=True,  # Definido apenas na criação, nunca alterável
    )

    data_atualizacao = models.DateTimeField(
        verbose_name='Atualizado em',
        auto_now=True,  # Atualizado automaticamente em cada save()
    )

    class Meta:
        verbose_name = 'Aviso'
        verbose_name_plural = 'Avisos'
        ordering = ['-data_criacao']  # Mais recentes primeiro

    def __str__(self):
        return f"[{self.get_categoria_display()}] {self.titulo}"

    @property
    def categoria_badge_class(self):
        """
        Retorna a classe Bootstrap para o badge de categoria.
        Usado diretamente nos templates: {{ aviso.categoria_badge_class }}
        """
        mapa = {
            'evento':       'bg-primary',
            'aviso_geral':  'bg-secondary',
            'oportunidade': 'bg-success',
            'manutencao':   'bg-warning text-dark',
            'urgente':      'bg-danger',
        }
        return mapa.get(self.categoria, 'bg-secondary')