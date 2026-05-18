from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Aviso
from .forms import AvisoForm

# decorator para restringir acesso a views de criação/edição/deleção apenas para ADMINs
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

# view pra visitante / entrada imediata do mural ( pre login)
def index(request):
    """
    Página inicial = mural de avisos em modo leitura.
    Acessível por qualquer pessoa (visitante, COMUM ou ADMIN).

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


# views de CRUD para adm
@admin_required
def criar(request):
    if request.method == 'POST':
        form = AvisoForm(request.POST, request.FILES)
        if form.is_valid():
            aviso        = form.save(commit=False)
            aviso.autor  = request.user  # linka o adm logado ao aviso
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


# views de CRUD para adm
@admin_required
def editar(request, pk):
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
    aviso = get_object_or_404(Aviso, pk=pk)

    if request.method == 'POST':
        aviso.delete()
        messages.success(request, 'Aviso removido permanentemente.')
        return redirect('mural:index')

    return render(request, 'mural/confirmar_delete.html', {'aviso': aviso})


@admin_required
def toggle_publicado(request, pk):
    aviso = get_object_or_404(Aviso, pk=pk)

    if request.method == 'POST':
        aviso.publicado = not aviso.publicado
        aviso.save()
        status = 'publicado' if aviso.publicado else 'ocultado'
        messages.success(request, f'Aviso {status} com sucesso.')

    return redirect('mural:index')