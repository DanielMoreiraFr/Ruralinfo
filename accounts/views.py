from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import LoginForm, CadastroComumForm, CadastroAdminForm


def login_view(request):
    """
    Autentica usando o username composto (email_TIPO) montado pelo LoginForm.
    """
    # se o usuario ta logado joga ele pra home
    if request.user.is_authenticated:
        return redirect('mural:index')

    # validação pelo LoginForm e retorna o usuário identificado
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            usuario = form.cleaned_data['_usuario']
            login(request, usuario)
            messages.success(request, f'Bem-vindo(a), {usuario.nome_completo}!')
            return redirect('mural:index')
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})

# view pra cadastro que lida com os dois tipos de conta, diferenciando com os prefixos
def cadastro_view(request):
    """
    Exibe dois formulários na mesma página: um para COMUM e um para ADMIN.
    O template controla qual aba está visível via JavaScript.
    Equivale ao fluxo de `inserir_usuario` do legado, com validações reais.
    """

    # aqui também envia o user pra home se já estiver logado
    if request.user.is_authenticated:
        return redirect('mural:index')

    form_comum = CadastroComumForm(prefix='comum')
    form_admin = CadastroAdminForm(prefix='admin')

    # o campo hidden 'tipo_formulario' no template indica qual formulário foi submetido
    if request.method == 'POST':
        tipo = request.POST.get('tipo_formulario')  # campo hidden no template

        # valida o formulário correto com base no tipo e salva se for válido
        if tipo == 'comum':
            form_comum = CadastroComumForm(request.POST, prefix='comum')
            if form_comum.is_valid():
                form_comum.save()
                messages.success(
                    request, 'Conta Comum criada! Faça login para continuar.'
                )
                return redirect('accounts:login')

        # o processo é o mesmo pro admin, só muda o form e a mensagem
        elif tipo == 'admin':
            form_admin = CadastroAdminForm(request.POST, prefix='admin')
            if form_admin.is_valid():
                form_admin.save()
                messages.success(
                    request, 'Conta Admin criada! Faça login para continuar.'
                )
                return redirect('accounts:login')

        # Se teve erro, mostra qual aba estava ativa para o template reabrir
        aba_ativa = tipo or 'comum'
    else:
        aba_ativa = 'comum'

    return render(request, 'accounts/cadastro.html', {
        'form_comum': form_comum,
        'form_admin': form_admin,
        'aba_ativa':  aba_ativa,
    })


# logout por POST pra evitar CSRF — só acessível pra usuários logados
@login_required
def logout_view(request):
    """Logout via POST — protegido contra CSRF."""
    if request.method == 'POST':
        logout(request)
        messages.info(request, 'Você saiu com segurança.')
    return redirect('mural:index')