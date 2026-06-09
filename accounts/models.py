import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class Usuario(AbstractUser):
    """
    Modelo de usuário personalizado que suporta dois tipos de conta: COMUM e ADMIN.
    A unicidade é garantida pela combinação de e-mail + tipo de conta, permitindo o mesmo e-mail em tipos diferentes.
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

    # Desativa os campos nativos de nome do AbstractUser para usar apenas o nome_completo
    first_name = None
    last_name = None

    # Campos obrigatórios ao criar superusuário via terminal
    REQUIRED_FIELDS = ['email', 'nome_completo']

    # Configurações de metadados do modelo no banco de dados e no Admin
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        # Cria uma restrição de unicidade composta no banco (impede e-mail duplicado no mesmo tipo)
        unique_together = [('email', 'tipo_conta')]

    # Sobrescreve o salvamento do modelo para interceptar e injetar lógica antes de ir pro banco
    def save(self, *args, **kwargs):
        # Padroniza o e-mail limpando espaços e forçando letras minúsculas
        self.email = self.email.strip().lower()
        
        # Gera o username composto automaticamente juntando e-mail e tipo de conta
        self.username = f"{self.email}_{self.tipo_conta}"

        # Define automaticamente o acesso ao Admin (is_staff) caso o usuário seja ADMIN
        self.is_staff = (self.tipo_conta == 'ADMIN')
        
        # Executa a rotina padrão de salvamento do Django
        super().save(*args, **kwargs)

    # Define a representação em texto do objeto (usado no Admin e em listagens)
    def __str__(self):
        return f"{self.nome_completo} ({self.get_tipo_conta_display()})"


class CodigoConvite(models.Model):
    """
    Controla e armazena os tokens de convite gerados para permitir o cadastro de novas contas ADMIN.
    """

    # Gera um UUID aleatório e impossível de ser editado
    codigo = models.UUIDField(
        verbose_name='Código',
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )

    # Relacionamento de Chave Estrangeira (N:1) mostrando qual usuário gerou este convite
    criado_por = models.ForeignKey(
        Usuario,
        verbose_name='Criado por',
        on_delete=models.SET_NULL,
        null=True,
        related_name='convites_gerados',
    )

    # Relacionamento Um para Um (1:1) vinculando o convite ao usuário específico que o utilizou
    usado_por = models.OneToOneField(
        Usuario,
        verbose_name='Usado por',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='convite_utilizado',
    )

    foi_usado = models.BooleanField(default=False)
    # Registra a data e hora de criação de forma automática
    criado_em = models.DateTimeField(auto_now_add=True)

    # Configurações de metadados do modelo
    class Meta:
        verbose_name = 'Código de Convite'
        verbose_name_plural = 'Códigos de Convite'
        # Define a ordenação padrão trazendo sempre os convites mais recentes primeiro
        ordering = ['-criado_em']

    # Define a representação em texto do código exibindo apenas os 8 primeiros dígitos do UUID
    def __str__(self):
        status = 'Usado' if self.foi_usado else 'Disponível'
        return f"Convite {str(self.codigo)[:8]}... [{status}]"