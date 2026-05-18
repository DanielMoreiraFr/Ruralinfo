import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class Usuario(AbstractUser):
    """
    Substitui a tabela `contas_usuarios` do SQLite legado.

    EQUIVALÊNCIA COM O LEGADO:
        nome      → nome_completo
        email     → email (sem unique isolado)
        senha     → gerenciada pelo AbstractUser com hashing
        tipoConta → tipo_conta ('COMUM' | 'ADMIN')

    O campo `username` é invisível ao usuário e gerado automaticamente
    no save() combinando email + tipo_conta, exatamente como a função
    `validação_login` do legado buscava por tipo antes de comparar o email.
    """

    TIPO_CONTA_CHOICES = [
        ('COMUM', 'Comum'),
        ('ADMIN', 'Administrador'),
    ]

    # Removemos unique=True isolado do email — a unicidade real
    # é garantida pelo unique_together abaixo (email + tipo_conta)
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

    # Desativamos first_name e last_name do AbstractUser —
    # usamos nome_completo no lugar, igual ao campo `nome` do legado
    first_name = None  # type: ignore
    last_name = None   # type: ignore

    REQUIRED_FIELDS = ['email', 'nome_completo']

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        # Equivalente ao check `usuario_existe(email, tipoC)` do legado:
        # impede duplicata da mesma combinação no banco
        unique_together = [('email', 'tipo_conta')]

    def save(self, *args, **kwargs):
        """
        Gera o username composto automaticamente.
        Equivale à lógica de `validação_login` que buscava por tipoConta
        antes de comparar emails — aqui tornamos isso uma chave explícita.
        """
        self.email = self.email.strip().lower()
        self.username = f"{self.email}_{self.tipo_conta}"
        # Hierarquia de permissão: ADMIN sempre tem acesso ao painel
        self.is_staff = (self.tipo_conta == 'ADMIN')
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nome_completo} ({self.get_tipo_conta_display()})"


class CodigoConvite(models.Model):
    """
    Controla a criação de novas contas ADMIN via código UUID.
    O primeiro admin é criado via `python manage.py shell` (ver README).
    """

    codigo = models.UUIDField(
        verbose_name='Código',
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )

    criado_por = models.ForeignKey(
        Usuario,
        verbose_name='Criado por',
        on_delete=models.SET_NULL,
        null=True,
        related_name='convites_gerados',
    )

    usado_por = models.OneToOneField(
        Usuario,
        verbose_name='Usado por',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='convite_utilizado',
    )

    foi_usado = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Código de Convite'
        verbose_name_plural = 'Códigos de Convite'
        ordering = ['-criado_em']

    def __str__(self):
        status = 'Usado' if self.foi_usado else 'Disponível'
        return f"Convite {str(self.codigo)[:8]}... [{status}]"