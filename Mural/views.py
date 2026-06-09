from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.utils import timezone
from django.urls import reverse
from .models import Aviso, Sugestao
from .forms import AvisoForm, SugestaoForm

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
    """
    Cria um novo aviso.
    Se vier com ?sugestao=<pk> na URL, pré-preenche o formulário
    com o texto e categoria da sugestão aceita.
    """
    sugestao_pk = request.GET.get('sugestao')
    initial     = {}
 
    # Pré-preenche se vier de uma sugestão aceita
    if sugestao_pk:
        try:
            sugestao = Sugestao.objects.get(pk=sugestao_pk, status='aceita')
            initial  = {
                'conteudo':  sugestao.texto,
                'categoria': sugestao.categoria,
            }
        except Sugestao.DoesNotExist:
            pass
 
    if request.method == 'POST':
        form = AvisoForm(request.POST, request.FILES)
        if form.is_valid():
            aviso       = form.save(commit=False)
            aviso.autor = request.user
            aviso.save()
            messages.success(request, 'Aviso publicado com sucesso!')
            return redirect('mural:index')
    else:
        form = AvisoForm(initial=initial)
 
    return render(request, 'mural/aviso_form.html', {
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

def horarios(request):
    return render(request, 'mural/horarios.html')

@login_required
def sugestao_nova(request):
    """
    Qualquer usuário logado (COMUM ou ADMIN) pode enviar uma sugestão.
    """
    if request.method == 'POST':
        form = SugestaoForm(request.POST)
        if form.is_valid():
            sugestao        = form.save(commit=False)
            sugestao.autor  = request.user
            sugestao.status = 'pendente'
            sugestao.save()
            messages.success(
                request,
                'Sugestão enviada! Um administrador irá analisá-la em breve.'
            )
            return redirect('mural:index')
    else:
        form = SugestaoForm()
 
    return render(request, 'mural/sugestao_form.html', {'form': form})
 
 
@admin_required
def sugestoes_pendentes(request):
    """
    Lista de sugestões pendentes — visível apenas para ADMIN.
    """
    sugestoes = Sugestao.objects.filter(
        status='pendente'
    ).select_related('autor')
 
    return render(request, 'mural/sugestoes_pendentes.html', {
        'sugestoes': sugestoes,
    })
 
 
@admin_required
def sugestoes_arquivadas(request):
    """
    Lista de sugestões negadas — visível apenas para ADMIN.
    Ordenadas pela data de arquivamento para facilitar futura limpeza por tempo.
    """
    sugestoes = Sugestao.objects.filter(
        status='negada'
    ).select_related('autor').order_by('-arquivado_em')
 
    return render(request, 'mural/sugestoes_arquivadas.html', {
        'sugestoes': sugestoes,
    })
 
 
@admin_required
def sugestao_aceitar(request, pk):
    """
    Aceita uma sugestão e redireciona para criar post pré-preenchido.
    Passa o pk da sugestão via query param para a view de criar aviso.
    """
    sugestao = get_object_or_404(Sugestao, pk=pk, status='pendente')
 
    if request.method == 'POST':
        sugestao.status = 'aceita'
        sugestao.save()
        messages.success(request, 'Sugestão aceita. Complete e publique o aviso.')
        return redirect(f"{reverse('mural:criar')}?sugestao={sugestao.pk}")
 
    return redirect('mural:sugestoes_pendentes')
 
 
@admin_required
def sugestao_negar(request, pk):
    """
    Nega uma sugestão e a arquiva com a data atual.
    """
    sugestao = get_object_or_404(Sugestao, pk=pk, status='pendente')
 
    if request.method == 'POST':
        sugestao.status       = 'negada'
        sugestao.arquivado_em = timezone.now()
        sugestao.save()
        messages.info(request, 'Sugestão negada e arquivada.')
 
    return redirect('mural:sugestoes_pendentes')
 