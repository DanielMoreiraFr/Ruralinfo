import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class Usuario(AbstractUser):
    """
    Model central de autenticação do Ruralinfo.

    POR QUE AbstractUser e não AbstractBaseUser?
    AbstractUser já traz toda a infraestrutura do Django (grupos, permissões,
    is_staff, is_active, date_joined etc.) pronta. AbstractBaseUser seria usado
    apenas se quiséssemos redesenhar o sistema de autenticação do zero.

    ESTRATÉGIA DE USERNAME COMPOSTO:
    O Django exige um campo `username` único para autenticação. Nossa solução
    é tornar o username "invisível" para o usuário e gerá-lo automaticamente
    no save() combinando email + tipo_conta. Assim, o mesmo email pode existir
    duas vezes no banco com usernames distintos:
        joao@ufrpe.br_COMUM
        joao@ufrpe.br_ADMIN
    """

    TIPO_CONTA_CHOICES = [
        ('COMUM', 'Comum'),
        ('ADMIN', 'Administrador'),
    ]

    # Sobrescrevemos email para remover unique=True que o AbstractUser herdaria
    # de algumas versões. A unicidade real é enforçada pelo unique_together abaixo.
    email = models.EmailField(
        verbose_name='E-mail Institucional',
        blank=False,
        null=False,
    )

    nome_completo = models.CharField(
        verbose_name='Nome Completo',
        max_length=255,
        blank=False,
        null=False,
    )

    tipo_conta = models.CharField(
        verbose_name='Tipo de Conta',
        max_length=10,
        choices=TIPO_CONTA_CHOICES,
        default='COMUM',
    )

    # first_name e last_name do AbstractUser não serão usados;
    # usamos nome_completo no lugar.
    first_name = None  # type: ignore
    last_name = None   # type: ignore

    # Campo usado como identificador de login no formulário (exibido ao usuário)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'nome_completo']

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        # Garante no nível do banco de dados que a combinação é única.
        # Isso cria um índice composto (email, tipo_conta) no PostgreSQL/SQLite.
        unique_together = [('email', 'tipo_conta')]

    def save(self, *args, **kwargs):
        """
        Pré-processamento antes de salvar no banco.

        1. Gera o username composto — o usuário nunca digita isso, é interno.
        2. Sincroniza is_staff com tipo_conta, garantindo que um admin
           promovido/rebaixado via código tenha as permissões corretas.
        """
        # Normaliza o email para minúsculas antes de compor o username
        self.email = self.email.strip().lower()
        self.username = f"{self.email}_{self.tipo_conta}"

        self.is_staff = (self.tipo_conta == 'ADMIN')

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nome_completo} [{self.get_tipo_conta_display()}]"


class CodigoConvite(models.Model):
    """
    Sistema de convites para criação de novas contas ADMIN.

    POR QUE UUID?
    UUIDs são praticamente impossíveis de adivinhar por força bruta
    (2^122 combinações possíveis). Um código sequencial (1, 2, 3...) seria
    trivialmente enumerável por um atacante.

    FLUXO:
    1. Um Admin existente gera um código via painel admin ou comando.
    2. Compartilha o UUID com a pessoa que vai virar admin.
    3. A pessoa usa o UUID no formulário de cadastro.
    4. Após uso, foi_usado=True — o código não pode ser reutilizado.
    """

    codigo = models.UUIDField(
        verbose_name='Código UUID',
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )

    criado_por = models.ForeignKey(
        Usuario,
        verbose_name='Criado por',
        on_delete=models.SET_NULL,  # Se o admin for deletado, mantemos o histórico
        null=True,
        related_name='convites_gerados',
    )

    foi_usado = models.BooleanField(
        verbose_name='Foi Usado',
        default=False,
    )

    usado_por = models.OneToOneField(
        Usuario,
        verbose_name='Usado por',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='convite_utilizado',
    )

    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Código de Convite'
        verbose_name_plural = 'Códigos de Convite'
        ordering = ['-criado_em']

    def __str__(self):
        status = "✓ Usado" if self.foi_usado else "Disponível"
        return f"Convite {str(self.codigo)[:8]}... [{status}]"