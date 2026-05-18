from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, CodigoConvite


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display    = ('email', 'nome_completo', 'tipo_conta', 'is_active')
    list_filter     = ('tipo_conta', 'is_active')
    search_fields   = ('email', 'nome_completo')
    ordering        = ('email',)
    readonly_fields = ('username', 'date_joined', 'last_login')

    fieldsets = (
        (None,               {'fields': ('username', 'password')}),
        ('Dados Pessoais',   {'fields': ('nome_completo', 'email', 'tipo_conta')}),
        ('Permissões',       {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Datas',            {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('nome_completo', 'email', 'tipo_conta', 'password1', 'password2'),
        }),
    )


@admin.register(CodigoConvite)
class CodigoConviteAdmin(admin.ModelAdmin):
    list_display    = ('codigo', 'criado_por', 'foi_usado', 'usado_por', 'criado_em')
    list_filter     = ('foi_usado',)
    readonly_fields = ('codigo', 'foi_usado', 'usado_por', 'criado_em')

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.criado_por = request.user
        super().save_model(request, obj, form, change)