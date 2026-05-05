from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Aviso
from .forms import AvisoForm


# =============================================================================
# DECORATOR CUSTOMIZADO — ACESSO APENAS PARA ADMIN
# =============================================================================

def admin_required(view_func):
    """
    Decorator que combina @login_required com a verificação de tipo_conta == 'ADMIN'.

    POR QUE não usar @permission_required?
    O sistema de permissões do Django é baseado em grupos e permissões de model
    (add_aviso, change_aviso, etc.). Nossa regra é mais simples: tipo_conta == 'ADMIN'.
    Um decorator explícito é mais legível e direto para este caso.

    POR QUE não usar @user_passes_test(lambda u: u.tipo_conta == 'ADMIN')?
    Poderíamos, mas criar um decorator nomeado melhora a legibilidade:
    @admin_required é autoexplicativo na view.
    """
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.tipo_conta != 'ADMIN':
            messages.error(request, 'Acesso restrito a administradores.')
            return redirect('mural:lista')
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return wrapper


# =============================================================================
# VIEWS PÚBLICAS (usuários autenticados de qualquer tipo)
# =============================================================================

@login_required
def mural_lista(request):
    """
    Feed principal do Ruralinfo — lista todos os avisos com filtros e paginação.

    FILTROS DISPONÍVEIS (via GET params):
    - ?categoria=evento   → filtra por categoria
    - ?q=texto            → busca no título e conteúdo (case-insensitive)

    PAGINAÇÃO:
    Exibimos 9 cards por página (grade 3x3 no Bootstrap, responsiva).
    O Paginator do Django cuida da matemática de páginas automaticamente.
    """
    avisos = Aviso.objects.select_related('autor').all()

    # Filtro por categoria
    categoria = request.GET.get('categoria', '').strip()
    if categoria:
        avisos = avisos.filter(categoria=categoria)

    # Busca textual
    q = request.GET.get('q', '').strip()
    if q:
        # Q objects permitem OR entre filtros
        avisos = avisos.filter(
            Q(titulo__icontains=q) | Q(conteudo__icontains=q)
        )

    # Paginação
    paginator = Paginator(avisos, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'mural/mural_list.html', {
        'page_obj':        page_obj,
        'categorias':      Aviso.CATEGORIA_CHOICES,
        'categoria_ativa': categoria,
        'busca':           q,
    })


@login_required
def aviso_detalhe(request, pk):
    """Exibe um aviso individual com todos os detalhes."""
    aviso = get_object_or_404(Aviso, pk=pk)
    return render(request, 'mural/aviso_detalhe.html', {'aviso': aviso})


# =============================================================================
# VIEWS DE CRUD (exclusivo para ADMIN)
# =============================================================================

@admin_required
def aviso_criar(request):
    """
    Cria um novo aviso.
    O autor é definido automaticamente como o usuário logado (request.user).
    Nunca permitimos que o usuário escolha o autor — evita falsificação de autoria.
    """
    if request.method == 'POST':
        form = AvisoForm(request.POST, request.FILES)
        if form.is_valid():
            aviso = form.save(commit=False)
            aviso.autor = request.user  # Atribui o autor aqui, não no form
            aviso.save()
            messages.success(request, f'Aviso "{aviso.titulo}" publicado com sucesso!')
            return redirect('mural:lista')
    else:
        form = AvisoForm()

    return render(request, 'mural/aviso_form.html', {
        'form':  form,
        'titulo_pagina': 'Novo Aviso',
        'btn_label':     'Publicar',
    })


@admin_required
def aviso_editar(request, pk):
    """
    Edita um aviso existente.
    Um ADMIN pode editar QUALQUER aviso do sistema (conforme especificação).
    Se quiser restringir para o próprio aviso, adicione:
        aviso = get_object_or_404(Aviso, pk=pk, autor=request.user)
    """
    aviso = get_object_or_404(Aviso, pk=pk)

    if request.method == 'POST':
        # instance=aviso diz ao form que é uma edição, não criação
        form = AvisoForm(request.POST, request.FILES, instance=aviso)
        if form.is_valid():
            form.save()
            messages.success(request, f'Aviso "{aviso.titulo}" atualizado!')
            return redirect('mural:lista')
    else:
        form = AvisoForm(instance=aviso)

    return render(request, 'mural/aviso_form.html', {
        'form':          form,
        'aviso':         aviso,
        'titulo_pagina': f'Editar: {aviso.titulo}',
        'btn_label':     'Salvar Alterações',
    })


@admin_required
def aviso_deletar(request, pk):
    """
    Deleta um aviso — exige confirmação via POST (página de confirmação).

    FLUXO:
    GET  → exibe página de confirmação ("Tem certeza?")
    POST → executa a deleção e redireciona

    POR QUE não deletar no GET?
    Igual ao logout — um link GET pode ser disparado por bots, prefetch do
    browser ou ataques CSRF. A confirmação via POST com token CSRF é segura.
    """
    aviso = get_object_or_404(Aviso, pk=pk)

    if request.method == 'POST':
        titulo = aviso.titulo
        aviso.delete()
        messages.success(request, f'Aviso "{titulo}" removido do mural.')
        return redirect('mural:lista')

    return render(request, 'mural/aviso_confirmar_delete.html', {'aviso': aviso})