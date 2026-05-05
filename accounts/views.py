from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import CadastroForm, LoginForm


def login_view(request):
    """
    View de login com suporte à dualidade COMUM/ADMIN.

    FLUXO:
    GET  → exibe o formulário em branco.
    POST → valida credenciais (via LoginForm.clean) → autentica → redireciona.

    REDIRECT PÓS-LOGIN:
    - ADMIN → /admin/ (painel administrativo do Django)
    - COMUM → /mural/ (feed de avisos)

    POR QUE não usar LoginView do django.contrib.auth?
    A view genérica do Django não suporta o campo extra `tipo_conta`.
    Precisamos de controle total sobre o processo de montagem do username composto.
    """
    if request.user.is_authenticated:
        return _redirect_por_tipo(request.user)

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            usuario = form.cleaned_data['_usuario']
            login(request, usuario)
            messages.success(request, f'Bem-vindo(a), {usuario.nome_completo}! 👋')
            return _redirect_por_tipo(usuario)
        # Se inválido, o form já tem os erros — renderiza novamente
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def cadastro_view(request):
    """
    View de cadastro unificada para COMUM e ADMIN.

    Após cadastro bem-sucedido, redireciona para o login sem autenticar
    automaticamente — força o usuário a confirmar suas credenciais.
    Isso é uma boa prática de segurança e UX.
    """
    if request.user.is_authenticated:
        return _redirect_por_tipo(request.user)

    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            messages.success(
                request,
                f'Conta {usuario.get_tipo_conta_display()} criada com sucesso! '
                f'Faça login para continuar.'
            )
            return redirect('accounts:login')
        else:
            messages.error(request, 'Corrija os erros abaixo antes de continuar.')
    else:
        form = CadastroForm()

    return render(request, 'accounts/cadastro.html', {'form': form})


@login_required
def logout_view(request):
    """
    Logout via POST — boa prática de segurança.

    POR QUE POST e não GET?
    Um logout via GET pode ser disparado por um <img src="/logout/"> em um
    site malicioso (ataque CSRF). O Django já protege POSTs com o token CSRF,
    então usar POST torna o logout seguro por padrão.
    """
    if request.method == 'POST':
        logout(request)
        messages.info(request, 'Você saiu com segurança. Até logo!')
        return redirect('accounts:login')
    return redirect('mural:lista')


# =============================================================================
# HELPER INTERNO
# =============================================================================

def _redirect_por_tipo(usuario):
    """
    Centraliza a lógica de redirecionamento pós-login.
    Retorna um HttpResponseRedirect baseado no tipo de conta.
    """
    if usuario.tipo_conta == 'ADMIN':
        return redirect('/admin/')
    return redirect('mural:lista')