from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class LocalRural(models.Model):
    """
    Representa um local físico da UFRPE cadastrado por um Admin.
    Pode ser um ponto do circular ou qualquer outro espaço do campus.
    """
    nome = models.CharField(
        verbose_name='Nome do Local',
        max_length=150,
    )

    descricao = models.TextField(
        verbose_name='Descrição',
    )

    imagem_principal = models.ImageField(
        verbose_name='Imagem Principal',
        upload_to='locais/capas/',
        help_text='Aparece no card da listagem e como primeira foto da galeria.',
    )

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Local Rural'
        verbose_name_plural = 'Locais Rurais'
        ordering = ['nome']

    def __str__(self):
        return self.nome

    @property
    def media_avaliacoes(self):
        """Retorna a média das avaliações ou None se não houver nenhuma."""
        avaliacoes = self.avaliacoes.all()
        if not avaliacoes.exists():
            return None
        total = sum(a.nota for a in avaliacoes)
        return round(total / avaliacoes.count(), 1)

    @property
    def total_avaliacoes(self):
        return self.avaliacoes.count()

    @property
    def total_comentarios(self):
        return self.comentarios.filter(pai=None).count()


class ImagemLocal(models.Model):
    """
    Fotos adicionais do local — formam a galeria na página de detalhe.
    A imagem principal do LocalRural já aparece como primeira foto.
    """
    local = models.ForeignKey(
        LocalRural,
        on_delete=models.CASCADE,
        related_name='imagens',
        verbose_name='Local',
    )

    imagem = models.ImageField(
        verbose_name='Foto',
        upload_to='locais/galeria/',
    )

    legenda = models.CharField(
        verbose_name='Legenda',
        max_length=200,
        blank=True,
    )

    ordem = models.PositiveIntegerField(
        verbose_name='Ordem na galeria',
        default=0,
        help_text='Número menor aparece primeiro.',
    )

    class Meta:
        verbose_name = 'Imagem do Local'
        verbose_name_plural = 'Imagens do Local'
        ordering = ['ordem']

    def __str__(self):
        return f"Foto de {self.local.nome} (ordem {self.ordem})"


class Avaliacao(models.Model):
    """
    Nota de 0 a 5 (em incrementos de 0.5) dada por um usuário a um local.
    Cada usuário só pode ter uma avaliação por local — pode atualizar quando quiser.
    """
    NOTAS = [(i / 2, f'{i / 2} ★') for i in range(1, 11)]  # 0.5 a 5.0

    local = models.ForeignKey(
        LocalRural,
        on_delete=models.CASCADE,
        related_name='avaliacoes',
        verbose_name='Local',
    )

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='avaliacoes',
        verbose_name='Usuário',
    )

    nota = models.FloatField(
        verbose_name='Nota',
        validators=[MinValueValidator(0.5), MaxValueValidator(5.0)],
        choices=NOTAS,
    )

    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Avaliação'
        verbose_name_plural = 'Avaliações'
        # Garante uma avaliação por usuário por local
        unique_together = [('local', 'usuario')]

    def __str__(self):
        return f"{self.usuario.nome_completo} → {self.local.nome}: {self.nota}★"


class Comentario(models.Model):
    """
    Comentário de um usuário sobre um local.
    Suporta um nível de resposta: um comentário pode ter respostas,
    mas respostas não podem ter sub-respostas.

    pai=None  → comentário raiz
    pai=X     → resposta ao comentário X
    """
    local = models.ForeignKey(
        LocalRural,
        on_delete=models.CASCADE,
        related_name='comentarios',
        verbose_name='Local',
    )

    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comentarios',
        verbose_name='Autor',
    )

    pai = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='respostas',
        verbose_name='Resposta a',
    )

    conteudo = models.TextField(
        verbose_name='Comentário',
        max_length=1000,
    )

    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Comentário'
        verbose_name_plural = 'Comentários'
        ordering = ['-criado_em']

    def __str__(self):
        tipo = 'Resposta' if self.pai else 'Comentário'
        return f"{tipo} de {self.autor.nome_completo} em {self.local.nome}"

    @property
    def is_resposta(self):
        return self.pai is not None