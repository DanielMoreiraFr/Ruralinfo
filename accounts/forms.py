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
# VALIDADORES REUTILIZÁVEIS
# =============================================================================

def validar_email_ufrpe(email: str) -> str:
    """Equivale ao check implícito do legado — só aceita @ufrpe.br."""
    email = email.strip().lower()
    if not email.endswith('@ufrpe.br'):
        raise forms.ValidationError('Apenas e-mails @ufrpe.br são aceitos.')
    return email


def validar_forca_senha(senha: str) -> None:
    """
    Regras de senha definidas no prompt — substituem o armazenamento
    em plain text que o legado (`senha TEXT`) fazia no SQLite.
    """
    erros = []
    if len(senha) < 10:
        erros.append('Mínimo de 10 caracteres.')
    if not re.search(r'[A-Z]', senha):
        erros.append('Pelo menos uma letra maiúscula.')
    if not re.search(r'\d', senha):
        erros.append('Pelo menos um número.')
    if not re.search(r'[!@#$%^&*()\-_=+\[\]{}|;:\'",.<>?/`~\\]', senha):
        erros.append('Pelo menos um caractere especial (!@#$...).')
    if erros:
        raise forms.ValidationError(erros)


# =============================================================================
# FORMULÁRIO DE LOGIN
# =============================================================================

class LoginForm(forms.Form):
    """
    Equivale à função `validação_login(email, senha, tipo_conta)` do legado.
    O seletor de tipo_conta é obrigatório para montar o username composto.
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

    def clean(self):
        cleaned = super().clean()
        email     = cleaned.get('email', '').strip().lower()
        tipo      = cleaned.get('tipo_conta')
        senha     = cleaned.get('senha')

        if email and tipo and senha:
            username = f"{email}_{tipo}"
            usuario  = authenticate(username=username, password=senha)

            if usuario is None:
                raise forms.ValidationError(
                    'E-mail, tipo de conta ou senha incorretos.'
                )
            if not usuario.is_active:
                raise forms.ValidationError('Conta inativa.')

            cleaned['_usuario'] = usuario

        return cleaned


# =============================================================================
# FORMULÁRIO DE CADASTRO — COMUM
# =============================================================================

class CadastroComumForm(forms.ModelForm):
    """
    Equivale a `inserir_usuario(nome, email, senha, tipo_c)` do legado,
    mas com validações de segurança que o legado não possuía.
    """

    senha = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={'placeholder': 'Mínimo 10 caracteres'}),
    )
    confirmar_senha = forms.CharField(
        label='Confirmar Senha',
        widget=forms.PasswordInput(attrs={'placeholder': 'Repita a senha'}),
    )

    class Meta:
        model  = Usuario
        fields = ['nome_completo', 'email']
        widgets = {
            'nome_completo': forms.TextInput(attrs={'placeholder': 'Seu nome completo'}),
            'email':         forms.EmailInput(attrs={'placeholder': 'seunome@ufrpe.br'}),
        }

    def clean_email(self):
        return validar_email_ufrpe(self.cleaned_data.get('email', ''))

    def clean_senha(self):
        senha = self.cleaned_data.get('senha', '')
        validar_forca_senha(senha)
        return senha

    def clean(self):
        cleaned = super().clean()
        senha   = cleaned.get('senha')
        confirm = cleaned.get('confirmar_senha')
        email   = cleaned.get('email')

        if senha and confirm and senha != confirm:
            self.add_error('confirmar_senha', 'As senhas não coincidem.')

        # Equivale ao `usuario_existe(email, tipoC)` do legado
        if email and Usuario.objects.filter(email=email, tipo_conta='COMUM').exists():
            raise forms.ValidationError(
                'Já existe uma conta COMUM com este e-mail.'
            )
        return cleaned

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.tipo_conta = 'COMUM'
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

    class Meta:
        model  = Usuario
        fields = ['nome_completo', 'email']
        widgets = {
            'nome_completo': forms.TextInput(attrs={'placeholder': 'Seu nome completo'}),
            'email':         forms.EmailInput(attrs={'placeholder': 'seunome@ufrpe.br'}),
        }

    def clean_email(self):
        return validar_email_ufrpe(self.cleaned_data.get('email', ''))

    def clean_senha(self):
        senha = self.cleaned_data.get('senha', '')
        validar_forca_senha(senha)
        return senha

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

        # Valida o código de convite
        if codigo_str:
            try:
                codigo_uuid = uuid.UUID(codigo_str)
            except ValueError:
                self.add_error('codigo_convite', 'Formato de UUID inválido.')
                return cleaned

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

    def save(self, commit=True):
        try:
            with transaction.atomic():
                usuario = super().save(commit=False)
                usuario.tipo_conta = 'ADMIN'
                usuario.set_password(self.cleaned_data['senha'])
                if commit:
                    usuario.save()
                    convite = self.cleaned_data.get('_convite')
                    if convite:
                        convite.foi_usado = True
                        convite.usado_por = usuario
                        convite.save()
            return usuario
        except Exception:
            raise