from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, CodigoConvite

# Customização do painel administrativo para o modelo de Usuário Personalizado
@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    # Colunas da tabela de listagem do Admin
    list_display    = ('email', 'nome_completo', 'tipo_conta', 'is_active')
    # Filtros de busca
    list_filter     = ('tipo_conta', 'is_active')
    # Barra de pesquisa (busca por correspondência nos campos)
    search_fields   = ('email', 'nome_completo')
    # Ordenação dos registros
    ordering        = ('email',)
    # Campos nao editaveis
    readonly_fields = ('username', 'date_joined', 'last_login')
    # Organização visual dos campos em blocos
    fieldsets = (
        (None,               {'fields': ('username', 'password')}),
        ('Dados Pessoais',   {'fields': ('nome_completo', 'email', 'tipo_conta')}),
        ('Permissões',       {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Datas',            {'fields': ('last_login', 'date_joined')}),
    )
    # Campos exibidos no formulário de criação de um novo usuário
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('nome_completo', 'email', 'tipo_conta', 'password1', 'password2'),
        }),
    )


# Customização do painel de adm para o modelo de Códigos de Convite
@admin.register(CodigoConvite)
class CodigoConviteAdmin(admin.ModelAdmin):
    list_display    = ('codigo', 'criado_por', 'foi_usado', 'usado_por', 'criado_em')
    list_filter     = ('foi_usado',)
    readonly_fields = ('codigo', 'foi_usado', 'usado_por', 'criado_em')
    def save_model(self, request, obj, form, change):
        # Se o objeto não tem uma PK, é pq está sendo criado agora, nao editado!
        if not obj.pk:
            obj.criado_por = request.user          
        super().save_model(request, obj, form, change)