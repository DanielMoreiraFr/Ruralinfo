import re
import uuid
from django import forms
from django.contrib.auth import authenticate

from .models import Usuario, CodigoConvite


# =============================================================================
# HELPERS DE VALIDAÇÃO
# =============================================================================

def validar_email_ufrpe(email: str) -> str:
    """Normaliza e valida que o email é do domínio @ufrpe.br."""
    email = email.strip().lower()
    if not email.endswith('@ufrpe.br'):
        raise forms.ValidationError(
            'Apenas e-mails institucionais @ufrpe.br são aceitos.'
        )
    return email


def validar_forca_senha(senha: str) -> None:
    """
    Implementação manual das regras de força de senha.

    POR QUE MANUAL e não usar AUTH_PASSWORD_VALIDATORS do settings?
    Os validadores nativos do Django são ótimos para o admin, mas aqui
    precisamos de mensagens de erro granulares em português para exibir
    individualmente no formulário — um por linha — o que o sistema nativo
    não faz de forma elegante nos forms customizados.
    """
    erros = []
    if len(senha) < 10:
        erros.append('A senha precisa ter pelo menos 10 caracteres.')
    if not re.search(r'[A-Z]', senha):
        erros.append('A senha precisa ter pelo menos uma letra maiúscula (A-Z).')
    if not re.search(r'\d', senha):
        erros.append('A senha precisa ter pelo menos um número (0-9).')
    if not re.search(r'[!@#$%^&*()\-_=+\[\]{}|;:\'",.<>?/`~\\]', senha):
        erros.append('A senha precisa ter pelo menos um caractere especial (!@#$...).')
    if erros:
        raise forms.ValidationError(erros)


# =============================================================================
# FORMULÁRIO DE CADASTRO
# =============================================================================

class CadastroForm(forms.ModelForm):
    """
    Formulário único que serve para cadastrar tanto COMUM quanto ADMIN.

    ARQUITETURA:
    - O campo `codigo_convite` fica oculto/desabilitado para usuários COMUM
      e é exibido/obrigatório para ADMIN (controlado via JavaScript no template).
    - A validação no clean() garante a regra no servidor, independente do JS.
    """

    senha = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mínimo 10 caracteres',
            'id': 'id_senha',
        }),
        help_text='10+ caracteres, com maiúscula, número e símbolo.',
    )

    confirmar_senha = forms.CharField(
        label='Confirmar Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Repita a senha',
        }),
    )

    codigo_convite = forms.CharField(
        label='Código de Convite (somente para Admin)',
        required=False,  # Required é aplicado condicionalmente no clean()
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Cole aqui o UUID do convite',
            'id': 'id_codigo_convite',
        }),
    )

    class Meta:
        model = Usuario
        fields = ['nome_completo', 'email', 'tipo_conta']
        widgets = {
            'nome_completo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Seu nome completo',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'seunome@ufrpe.br',
            }),
            'tipo_conta': forms.RadioSelect(attrs={
                'class': 'form-check-input',
                'id': 'id_tipo_conta',
            }),
        }

    # --- Validações individuais de campo ---

    def clean_email(self):
        return validar_email_ufrpe(self.cleaned_data.get('email', ''))

    def clean_senha(self):
        senha = self.cleaned_data.get('senha', '')
        validar_forca_senha(senha)
        return senha

    # --- Validações cruzadas ---

    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get('senha')
        confirmar_senha = cleaned_data.get('confirmar_senha')
        tipo_conta = cleaned_data.get('tipo_conta')
        email = cleaned_data.get('email')
        codigo_str = cleaned_data.get('codigo_convite', '').strip()

        # 1. Confirmação de senha
        if senha and confirmar_senha and senha != confirmar_senha:
            self.add_error('confirmar_senha', 'As senhas não coincidem.')

        # 2. Verificação de unique_together antes de tentar salvar
        #    (evita IntegrityError do banco chegando ao usuário como erro 500)
        if email and tipo_conta:
            if Usuario.objects.filter(email=email, tipo_conta=tipo_conta).exists():
                raise forms.ValidationError(
                    f'Já existe uma conta {tipo_conta} com este e-mail.'
                )

        # 3. Lógica do código de convite para ADMIN
        if tipo_conta == 'ADMIN':
            if not codigo_str:
                self.add_error(
                    'codigo_convite',
                    'O código de convite é obrigatório para criar uma conta Admin.'
                )
            else:
                try:
                    codigo_uuid = uuid.UUID(codigo_str)
                except ValueError:
                    self.add_error('codigo_convite', 'Formato de UUID inválido.')
                    return cleaned_data

                try:
                    convite = CodigoConvite.objects.get(
                        codigo=codigo_uuid, foi_usado=False
                    )
                    # Cache do objeto para usar no save() sem nova query
                    cleaned_data['_convite_obj'] = convite
                except CodigoConvite.DoesNotExist:
                    self.add_error(
                        'codigo_convite',
                        'Código inválido, expirado ou já utilizado.'
                    )

        return cleaned_data

    def save(self, commit=True):
        """
        set_password() aplica o hashing PBKDF2-SHA256 com salt do Django.
        NUNCA salvar senha em plain text — esse método garante isso.
        """
        usuario = super().save(commit=False)
        usuario.set_password(self.cleaned_data['senha'])

        if commit:
            usuario.save()

            # Marca convite como usado e registra quem usou
            convite = self.cleaned_data.get('_convite_obj')
            if convite:
                convite.foi_usado = True
                convite.usado_por = usuario
                convite.save()

        return usuario


# =============================================================================
# FORMULÁRIO DE LOGIN
# =============================================================================

class LoginForm(forms.Form):
    """
    Formulário de login com suporte à dualidade de contas.

    FLUXO DE AUTENTICAÇÃO:
    1. Usuário informa email + tipo_conta + senha.
    2. O form monta o username composto internamente.
    3. Chama authenticate() — o backend padrão do Django usa username + password.
    4. Se válido, o objeto Usuario autenticado fica em cleaned_data['_usuario'].
    5. A view apenas chama login(request, usuario) — simples e segura.

    POR QUE fazer o authenticate() no form e não na view?
    Mantém a lógica de negócio (validação de credenciais) no form, deixando
    a view responsável apenas por controle de fluxo HTTP (redirect, render).
    Segue o princípio Fat Models/Forms, Thin Views do Django.
    """

    TIPO_CHOICES = [
        ('COMUM', 'Conta Comum'),
        ('ADMIN', 'Conta Administrador'),
    ]

    email = forms.EmailField(
        label='E-mail Institucional',
        widget=forms.EmailInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'seunome@ufrpe.br',
            'autofocus': True,
        }),
    )

    tipo_conta = forms.ChoiceField(
        label='Entrar como',
        choices=TIPO_CHOICES,
        initial='COMUM',
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
    )

    senha = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Sua senha',
        }),
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email', '').strip().lower()
        tipo_conta = cleaned_data.get('tipo_conta')
        senha = cleaned_data.get('senha')

        if email and tipo_conta and senha:
            username_composto = f"{email}_{tipo_conta}"

            # authenticate() retorna None se as credenciais forem inválidas.
            # Nunca revelamos se o email ou a senha estão errados — segurança
            # contra enumeração de usuários.
            usuario = authenticate(username=username_composto, password=senha)

            if usuario is None:
                raise forms.ValidationError(
                    'E-mail, tipo de conta ou senha incorretos.'
                )
            if not usuario.is_active:
                raise forms.ValidationError('Esta conta está inativa.')

            cleaned_data['_usuario'] = usuario

        return cleaned_data