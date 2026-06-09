from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.urls import reverse

from .models import Aviso, Sugestao
from .forms import AvisoForm, SugestaoForm


# Decorador customizado para restringir o acesso a views específicas
def admin_required(view_func):
    """
    Garante acesso apenas para contas ADMIN.
    Valida o tipo de conta e barra usuários comuns ou anônimos, retornando para a home.
    """
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.tipo_conta != 'ADMIN':
            messages.error(request, 'Acesso restrito a administradores.')
            return redirect('mural:index')
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return wrapper


def index(request):
    """
    Exibe a página inicial do mural de avisos em modo leitura.
    Filtra os registros por categoria via parâmetros de URL (GET) e gerencia a visibilidade de avisos ocultos.
    """
    categoria_ativa = request.GET.get('categoria', '')

    # Otimiza a consulta com select_related e filtra se o usuário não for administrador
    if request.user.is_authenticated and request.user.tipo_conta == 'ADMIN':
        avisos = Aviso.objects.select_related('autor').all()
    else:
        avisos = Aviso.objects.select_related('autor').filter(publicado=True)

    # Aplica o filtro de categoria na query se ele existir na URL
    if categoria_ativa:
        avisos = avisos.filter(categoria=categoria_ativa)

    return render(request, 'mural/index.html', {
        'avisos':          avisos,
        'categorias':      Aviso.CATEGORIA_CHOICES,
        'categoria_ativa': categoria_ativa,
    })


@admin_required
def criar(request):
    """
    Cria um novo aviso no mural.
    Permite o pré-preenchimento dos dados caso receba o identificador de uma sugestão aprovada pela URL.
    """
    sugestao_pk = request.GET.get('sugestao')
    initial     = {}
 
    # Tenta resgatar os dados da sugestão aprovada para injetar como valor inicial no formulário
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
            # Intercepta a instância para injetar o usuário logado como autor do post
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


@admin_required
def editar(request, pk):
    """ Carrega um aviso específico através da chave primária (ID) para edição de dados. """
    aviso = get_object_or_404(Aviso, pk=pk)

    if request.method == 'POST':
        # Passa a instância existente (instance=aviso) para o formulário aplicar as alterações no mesmo registro
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
    """ Remove permanentemente um aviso do banco de dados após confirmação via POST. """
    aviso = get_object_or_404(Aviso, pk=pk)

    if request.method == 'POST':
        aviso.delete()
        messages.success(request, 'Aviso removido permanentemente.')
        return redirect('mural:index')

    return render(request, 'mural/confirmar_delete.html', {'aviso': aviso})


@admin_required
def toggle_publicado(request, pk):
    """ Inverte o status de publicação (visibilidade) de um aviso de forma rápida. """
    aviso = get_object_or_404(Aviso, pk=pk)

    if request.method == 'POST':
        # Altera o booleano para o valor oposto ao atual e salva no banco
        aviso.publicado = not aviso.publicado
        aviso.save()
        status = 'publicado' if aviso.publicado else 'ocultado'
        messages.success(request, f'Aviso {status} com sucesso.')

    return redirect('mural:index')


def horarios(request):
    """ Renderiza a página estática informativa com os horários de ônibus da UFRPE. """
    return render(request, 'mural/horarios.html')


@login_required
def sugestao_nova(request):
    """ Processa e armazena uma nova sugestão enviada por qualquer usuário autenticado. """
    if request.method == 'POST':
        form = SugestaoForm(request.POST)
        if form.is_valid():
            # Intercepta a gravação para atribuir o autor logado e forçar o status inicial como pendente
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
    """ Lista todas as sugestões com status pendente aguardando avaliação. """
    sugestoes = Sugestao.objects.filter(
        status='pendente'
    ).select_related('autor')
 
    return render(request, 'mural/sugestoes_pendentes.html', {
        'sugestoes': sugestoes,
    })
 
 
@admin_required
def sugestoes_arquivadas(request):
    """ Lista as sugestões rejeitadas, ordenando-as pelas datas de arquivamento mais recentes. """
    sugestoes = Sugestao.objects.filter(
        status='negada'
    ).select_related('autor').order_by('-arquivado_em')
 
    return render(request, 'mural/sugestoes_arquivadas.html', {
        'sugestoes': sugestoes,
    })
 
 
@admin_required
def sugestao_aceitar(request, pk):
    """ Altera o status da sugestão para aceita e redireciona o Admin para a tela de criação com os dados acoplados. """
    sugestao = get_object_or_404(Sugestao, pk=pk, status='pendente')
 
    if request.method == 'POST':
        sugestao.status = 'aceita'
        sugestao.save()
        messages.success(request, 'Sugestão aceita. Complete e publique o aviso.')
        # Constrói a URL de redirecionamento injetando a chave primária da sugestão como query param
        return redirect(f"{reverse('mural:criar')}?sugestao={sugestao.pk}")
 
    return redirect('mural:sugestoes_pendentes')
 
 
@admin_required
def sugestao_negar(request, pk):
    """ Rejeita uma sugestão pendente, atualizando seu status e gravando o timestamp exato da ação. """
    sugestao = get_object_or_404(Sugestao, pk=pk, status='pendente')
 
    if request.method == 'POST':
        sugestao.status       = 'negada'
        sugestao.arquivado_em = timezone.now()
        sugestao.save()
        messages.info(request, 'Sugestão negada e arquivada.')
 
    return redirect('mural:sugestoes_pendentes')