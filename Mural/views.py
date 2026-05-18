from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Aviso
from .forms import AvisoForm


# =============================================================================
# DECORATOR ADMIN — substitui a verificação manual de `tipoConta` do legado
# =============================================================================

def admin_required(view_func):
    """
    Garante acesso apenas para contas ADMIN.
    Visitas de COMUM ou anônimos são redirecionadas com mensagem de erro.
    """
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.tipo_conta != 'ADMIN':
            messages.error(request, 'Acesso restrito a administradores.')
            return redirect('mural:index')
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return wrapper


# =============================================================================
# VIEW PÚBLICA — equivale ao botão "Visitante" da TelaInicial do legado
# =============================================================================

def index(request):
    """
    Página inicial = mural de avisos em modo leitura.
    Acessível por qualquer pessoa (visitante, COMUM ou ADMIN).
    Equivale à `MuralInformativo(tipo_usuario='visitante')` do legado.

    Filtro de categoria via GET: /mural/?categoria=evento
    Apenas avisos publicados são exibidos para não-admins.
    """
    categoria_ativa = request.GET.get('categoria', '')

    # Admins veem tudo (publicados e ocultos); outros só veem publicados
    if request.user.is_authenticated and request.user.tipo_conta == 'ADMIN':
        avisos = Aviso.objects.select_related('autor').all()
    else:
        avisos = Aviso.objects.select_related('autor').filter(publicado=True)

    if categoria_ativa:
        avisos = avisos.filter(categoria=categoria_ativa)

    return render(request, 'mural/index.html', {
        'avisos':          avisos,
        'categorias':      Aviso.CATEGORIA_CHOICES,
        'categoria_ativa': categoria_ativa,
    })


# =============================================================================
# CRUD — equivalem às funções do banco_infos.py do legado
# =============================================================================

@admin_required
def criar(request):
    """Equivale à função `postagem(msg, img_url, alt)` do legado."""
    if request.method == 'POST':
        form = AvisoForm(request.POST, request.FILES)
        if form.is_valid():
            aviso        = form.save(commit=False)
            aviso.autor  = request.user  # auditoria via id do usuário logado
            aviso.save()
            messages.success(request, 'Aviso publicado com sucesso!')
            return redirect('mural:index')
    else:
        form = AvisoForm()

    return render(request, 'mural/form.html', {
        'form':          form,
        'titulo_pagina': 'Novo Aviso',
        'btn_label':     'Publicar',
    })


@admin_required
def editar(request, pk):
    """Equivale à função `atualizar_postagem` do legado — mas para qualquer coluna."""
    aviso = get_object_or_404(Aviso, pk=pk)

    if request.method == 'POST':
        form = AvisoForm(request.POST, request.FILES, instance=aviso)
        if form.is_valid():
            form.save()
            messages.success(request, 'Aviso atualizado!')
            return redirect('mural:index')
    else:
        form = AvisoForm(instance=aviso)

    return render(request, 'mural/form.html', {
        'form':          form,
        'aviso':         aviso,
        'titulo_pagina': 'Editar Aviso',
        'btn_label':     'Salvar',
    })


@admin_required
def deletar(request, pk):
    """
    Equivale a `apagar_postagem(id_postagem)` do legado.
    Exige confirmação via POST — protegido contra exclusão acidental.
    """
    aviso = get_object_or_404(Aviso, pk=pk)

    if request.method == 'POST':
        aviso.delete()
        messages.success(request, 'Aviso removido permanentemente.')
        return redirect('mural:index')

    return render(request, 'mural/confirmar_delete.html', {'aviso': aviso})


@admin_required
def toggle_publicado(request, pk):
    """
    Equivale a `atualizar_postagem(id, 'estado', 0/1)` do legado.
    Oculta ou reativa um aviso sem deletá-lo — lógica de estado solicitada.
    """
    aviso = get_object_or_404(Aviso, pk=pk)

    if request.method == 'POST':
        aviso.publicado = not aviso.publicado
        aviso.save()
        status = 'publicado' if aviso.publicado else 'ocultado'
        messages.success(request, f'Aviso {status} com sucesso.')

    return redirect('mural:index')