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

    # Gerencia o upload da foto de capa salvando o arquivo físico em uma pasta dedicada
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
        # Define que por padrão a listagem será exibida em ordem alfabética (A-Z)
        ordering = ['nome']

    def __str__(self):
        return self.nome

    @property
    def media_avaliacoes(self):
        """
        Calcula dinamicamente a média aritmética de notas recebidas pelo local.
        Retorna um valor float arredondado para 1 casa decimal ou None caso 
        não existam avaliações registradas.
        """
        # Utiliza o related_name 'avaliacoes' para buscar os registros filhos invertidos
        avaliacoes = self.avaliacoes.all()
        if not avaliacoes.exists():
            return None
        total = sum(a.nota for a in avaliacoes)
        return round(total / avaliacoes.count(), 1)

    @property
    def total_avaliacoes(self):
        """Retorna a contagem total de notas submetidas a este local."""
        return self.avaliacoes.count()

    @property
    def total_comentarios(self):
        """
        Retorna a contagem de comentários principais (raízes),
        desconsiderando as sub-respostas da contagem geral do card.
        """
        return self.comentarios.filter(pai=None).count()


class ImagemLocal(models.Model):
    """
    Fotos adicionais do local — formam a galeria na página de detalhe.
    A imagem principal do LocalRural já aparece como primeira foto.
    """
    # Relacionamento N:1. em cascada garante que se o local for deletado, a galeria se apaga junto
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

    # Controla manualmente o posicionamento das fotos no carrossel/grade visual
    ordem = models.PositiveIntegerField(
        verbose_name='Ordem na galeria',
        default=0,
        help_text='Número menor aparece primeiro.',
    )

    class Meta:
        verbose_name = 'Imagem do Local'
        verbose_name_plural = 'Imagens do Local'
        # Garante que a ordenação respeite estritamente o peso definido no campo ordem
        ordering = ['ordem']

    def __str__(self):
        return f"Foto de {self.local.nome} (ordem {self.ordem})"


class Avaliacao(models.Model):
    """
    Nota de 0 a 5 (em incrementos de 0.5) dada por um usuário a um local.
    Cada usuário só pode ter uma avaliação por local — pode atualizar quando quiser.
    """
    # Cria uma lista de tuplas em tempo de execução mapeando valores numéricos a rótulos textuais
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

    # Aplica validadores numéricos nativos complementando a restrição do campo choices
    nota = models.FloatField(
        verbose_name='Nota',
        validators=[MinValueValidator(0.5), MaxValueValidator(5.0)],
        choices=NOTAS,
    )

    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Avaliação'
        verbose_name_plural = 'Avaliações'
        # Regra de banco impede o mesmo usuário de criar múltiplos registros para o mesmo local
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

    # Auto-relacionamento self: Aponta para a própria tabela de Comentários.
    # Permite nulo para identificar que o comentário original não possui pai.
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

    # Registra o momento da postagem ordenando a linha do tempo de forma decrescente
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Comentário'
        verbose_name_plural = 'Comentários'
        # Exibe os comentários mais recentes primeiro na listagem
        ordering = ['-criado_em']

    def __str__(self):
        tipo = 'Resposta' if self.pai else 'Comentário'
        return f"{tipo} de {self.autor.nome_completo} em {self.local.nome}"

    @property
    def is_resposta(self):
        """Retorna True caso o registro atual seja uma resposta vinculada a um comentário pai."""
        return self.pai is not None