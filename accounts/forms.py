import re
import uuid
import secrets
import string
from datetime import datetime, timedelta
from django import forms
from django.contrib.auth import authenticate
from django.db import transaction

from .models import Usuario, CodigoConvite


# =============================================================================
# UTILS DE VALIDAÇÃO
# =============================================================================

def validar_email_ufrpe(email: str) -> str:
    """Equivale ao check implícito do legado — só aceita @ufrpe.br."""
    email = email.strip().lower()
    # Barra e-mails de fora da UFRPE
    if not email.endswith('@ufrpe.br'):
        raise forms.ValidationError('Apenas e-mails @ufrpe.br são aceitos.')
    return email


def validar_forca_senha(senha: str) -> None:
    """
    Validação de força de senha 
    """
    erros = []
    # Valida mínimo de 10 caracteres
    if len(senha) < 10:
        erros.append('Mínimo de 10 caracteres.')
    # Valida pelo menos uma maiúscula
    if not re.search(r'[A-Z]', senha):
        erros.append('Pelo menos uma letra maiúscula.')
    # Valida pelo menos um número
    if not re.search(r'\d', senha):
        erros.append('Pelo menos um número.')
    # Valida pelo menos um caractere especial
    if not re.search(r'[!@#$%^&*()\-_=+\[\]{}|;:\'",.<>?/`~\\]', senha):
        erros.append('Pelo menos um caractere especial (!@#$...).')
    if erros:
        raise forms.ValidationError(erros)


# =============================================================================
# FORMULÁRIO DE LOGIN
# =============================================================================

class LoginForm(forms.Form):
    """
    Formulário de Login Personalizado que substitui o padrão do Django.
    Recebe o e-mail, tipo de conta e senha, e autentica usando o sistema de autenticação do Django, que por sua vez usa o backend personalizado para validar as credenciais.
    """

    TIPO_CHOICES = [
        ('COMUM',  'Conta Comum'),
        ('ADMIN',  'Conta Administrador'),
    ]

    email = forms.EmailField(
        label='E-mail',
        widget=forms.EmailInput(attrs={'placeholder': 'seunome@ufrpe.br'}),
    )

    tipo_conta = forms.ChoiceField(
        label='Entrar como',
        choices=TIPO_CHOICES,
        initial='COMUM',
        # RadioSelect → exibido como dois botões no template
        widget=forms.RadioSelect(),
    )

    senha = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={'placeholder': 'Sua senha'}),
    )

    # Executa a validação global do formulário (cruza dados de múltiplos campos)
    def clean(self):
        cleaned = super().clean()
        email     = cleaned.get('email', '').strip().lower()
        tipo      = cleaned.get('tipo_conta')
        senha     = cleaned.get('senha')

        if email and tipo and senha:
            # Monta o username composto
            username = f"{email}_{tipo}"
            # Autentica usando as credenciais do Django
            usuario  = authenticate(username=username, password=senha)

            if usuario is None:
                raise forms.ValidationError(
                    'E-mail, tipo de conta ou senha incorretos.'
                )
            if not usuario.is_active:
                raise forms.ValidationError('Conta inativa.')

            # Salva o usuário no context do formulário para a view usar depois
            cleaned['_usuario'] = usuario

        return cleaned


# =============================================================================
# FORMULÁRIO DE CADASTRO — COMUM
# =============================================================================

class CadastroComumForm(forms.ModelForm):
    """
    Formulário de Cadastro para Contas Comuns.
    Coleta nome completo, e-mail, senha e confirmação de senha.
    """

    senha = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={'placeholder': 'Mínimo 10 caracteres'}),
    )
    confirmar_senha = forms.CharField(
        label='Confirmar Senha',
        widget=forms.PasswordInput(attrs={'placeholder': 'Repita a senha'}),
    )

    # Configuração interna que diz ao Django qual Model e quais campos usar na tela
    class Meta:
        model  = Usuario
        fields = ['nome_completo', 'email']
        widgets = {
            'nome_completo': forms.TextInput(attrs={'placeholder': 'Seu nome completo'}),
            'email':         forms.EmailInput(attrs={'placeholder': 'seunome@ufrpe.br'}),
        }

    # Intercepta e valida especificamente o campo 'email' antes de salvar
    def clean_email(self):
        return validar_email_ufrpe(self.cleaned_data.get('email', ''))

    # Intercepta e valida especificamente o campo 'senha' antes de salvar
    def clean_senha(self):
        senha = self.cleaned_data.get('senha', '')
        validar_forca_senha(senha)
        return senha

    # Executa a validação global do formulário (cruza dados de múltiplos campos)
    def clean(self):
        cleaned = super().clean()
        senha   = cleaned.get('senha')
        confirm = cleaned.get('confirmar_senha')
        email   = cleaned.get('email')

        # Garante que a confirmação de senha é idêntica
        if senha and confirm and senha != confirm:
            self.add_error('confirmar_senha', 'As senhas não coincidem.')

        # Equivale ao `usuario_existe(email, tipoC)` do legado
        if email and Usuario.objects.filter(email=email, tipo_conta='COMUM').exists():
            raise forms.ValidationError(
                'Já existe uma conta COMUM com este e-mail.'
            )
        return cleaned

    # Sobrescreve o método de salvamento para interceptar e tratar os dados
    def save(self, commit=True):
        # Cria a instância na memória sem jogar no banco ainda (commit=False)
        usuario = super().save(commit=False)
        # Força o tipo da conta como COMUM
        usuario.tipo_conta = 'COMUM'
        # Criptografa a senha antes de salvar no banco
        usuario.set_password(self.cleaned_data['senha'])
        if commit:
            usuario.save()
        return usuario
    
    


# =============================================================================
# FORMULÁRIO DE CADASTRO — ADMIN
# =============================================================================

class CadastroAdminForm(forms.ModelForm):
    """
    Igual ao CadastroComumForm, mas exige código de convite válido.
    Nenhuma conta ADMIN pode ser criada sem convite de um admin existente.
    """

    senha = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={'placeholder': 'Mínimo 10 caracteres'}),
    )
    confirmar_senha = forms.CharField(
        label='Confirmar Senha',
        widget=forms.PasswordInput(attrs={'placeholder': 'Repita a senha'}),
    )
    codigo_convite = forms.CharField(
        label='Código de Convite',
        widget=forms.TextInput(attrs={'placeholder': 'Cole o UUID do convite'}),
    )

    # Configuração interna que diz ao Django qual Model e quais campos usar + seus placeholders pro html
    class Meta:
        model  = Usuario
        fields = ['nome_completo', 'email']
        widgets = {
            'nome_completo': forms.TextInput(attrs={'placeholder': 'Seu nome completo'}),
            'email':         forms.EmailInput(attrs={'placeholder': 'seunome@ufrpe.br'}),
        }

    # Intercepta e valida especificamente o campo 'email' antes de salvar
    def clean_email(self):
        return validar_email_ufrpe(self.cleaned_data.get('email', ''))

    # Intercepta e valida especificamente o campo 'senha' antes de salvar
    def clean_senha(self):
        senha = self.cleaned_data.get('senha', '')
        validar_forca_senha(senha)
        return senha

    # Executa a validação global do formulário (cruza dados de múltiplos campos)
    def clean(self):
        cleaned       = super().clean()
        senha         = cleaned.get('senha')
        confirm       = cleaned.get('confirmar_senha')
        email         = cleaned.get('email')
        codigo_str    = cleaned.get('codigo_convite', '').strip()

        if senha and confirm and senha != confirm:
            self.add_error('confirmar_senha', 'As senhas não coincidem.')

        if email and Usuario.objects.filter(email=email, tipo_conta='ADMIN').exists():
            raise forms.ValidationError(
                'Já existe uma conta ADMIN com este e-mail.'
            )

        if codigo_str:
            # Valida se a string é um formato UUID legítimo
            try:
                codigo_uuid = uuid.UUID(codigo_str)
            except ValueError:
                self.add_error('codigo_convite', 'Formato de UUID inválido.')
                return cleaned

            # Busca se o convite existe e está disponível no banco
            try:
                convite = CodigoConvite.objects.get(
                    codigo=codigo_uuid, foi_usado=False
                )
                cleaned['_convite'] = convite
            except CodigoConvite.DoesNotExist:
                self.add_error(
                    'codigo_convite',
                    'Código inválido ou já utilizado.'
                )
        else:
            self.add_error('codigo_convite', 'O código de convite é obrigatório.')

        return cleaned

    # Sobrescreve o método de salvamento para interceptar e tratar os dados
    def save(self, commit=True):
        try:
            # Transação Atômica: Se o usuário falhar, o convite não é usadodo e o contrário também
            with transaction.atomic():
                usuario = super().save(commit=False)
                # Força o tipo da conta como ADMIN
                usuario.tipo_conta = 'ADMIN'
                # Criptografa a senha antes de salvar no banco
                usuario.set_password(self.cleaned_data['senha'])
                if commit:
                    usuario.save()
                    # Recupera o objeto do convite que guardamos lá no método clean
                    convite = self.cleaned_data.get('_convite')
                    if convite:
                        # Queima o convite vinculando ao novo admin criado
                        convite.foi_usado = True
                        convite.usado_por = usuario
                        convite.save()
            return usuario
        except Exception:
            raise