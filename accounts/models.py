import uuid
import random
from django.db import models
from datetime import timedelta
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    """
    Modelo de usuário personalizado que suporta dois tipos de conta: COMUM e ADMIN.

    a exclusividade é garantida pela combinação de email + tipo_conta, permitindo
    que o mesmo email seja usado tanto pra ADMIN quanto para COMUM, mas não duplicado dentro
    do mesmo tipo.
    """

    TIPO_CONTA_CHOICES = [
        ('COMUM', 'Comum'),
        ('ADMIN', 'Administrador'),
    ]

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

    # desativa first_name e last_name do AbstractUser —
    first_name = None
    last_name = None

    REQUIRED_FIELDS = ['email', 'nome_completo']

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        unique_together = [('email', 'tipo_conta')]

    def save(self, *args, **kwargs):
        """
        Gera o username composto automaticamente.
        antes de comparar emails — aqui tornamos isso uma chave explícita.
        """

        self.email = self.email.strip().lower()
        self.username = f"{self.email}_{self.tipo_conta}"

        # Hierarquia de permissão pra adm ter acesso a tudo que o comum tem, só nesse sentido
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
    
class CodigoVerificacao(models.Model):
    usuario = models.OneToOneField(
        'accounts.Usuario',
        on_delete=models.CASCADE,
        related_name='codigo_verificacao',
    )
    codigo = models.CharField(max_length=6)
    criado_em = models.DateTimeField(auto_now_add=True)
 
    class Meta:
        verbose_name = 'Código de Verificação'
        verbose_name_plural = 'Códigos de Verificação'
 
    def save(self, *args, **kwargs):
        # Gera um código de 6 dígitos numéricos ao criar
        if not self.codigo:
            self.codigo = f"{random.randint(0, 999999):06d}"
        super().save(*args, **kwargs)
 
    def esta_expirado(self) -> bool:
        return timezone.now() > self.criado_em + timedelta(minutes=15)
 
    def __str__(self):
        return f"Código {self.codigo} → {self.usuario}"