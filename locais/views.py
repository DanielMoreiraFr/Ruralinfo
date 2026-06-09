from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import LocalRural, ImagemLocal, Avaliacao, Comentario
from .forms import AvaliacaoForm, ComentarioForm, LocalRuralForm, ImagemLocalFormSet


# =============================================================================
# DECORATOR — acesso restrito a ADMIN do sistema
# =============================================================================

def admin_required(view_func):
    """
    Decorator customizado para controle de níveis de acesso.
    Garante que apenas usuários com o atributo tipo_conta igual a 'ADMIN' 
    possam acessar rotas críticas de gerenciamento (CRUD).
    """
    @login_required
    def wrapper(request, *args, **kwargs):
        # Bloqueia usuários comuns, dispara uma mensagem de erro e redireciona
        if request.user.tipo_conta != 'ADMIN':
            messages.error(request, 'Acesso restrito a administradores.')
            return redirect('locais:lista')
        return view_func(request, *args, **kwargs)
    # Preserva o nome e metadados originais da view envelopada para evitar erros de roteamento
    wrapper.__name__ = view_func.__name__
    return wrapper


# =============================================================================
# VIEWS PÚBLICAS (autenticados)
# =============================================================================

@login_required
def lista_locais(request):
    """
    Lista todos os locais cadastrados na plataforma.
    Usa prefetch_related para carregar de forma otimizada as avaliações associadas,
    evitando o problema de consultas excessivas ao banco de dados (Query N+1).
    """
    locais = LocalRural.objects.prefetch_related('avaliacoes').all()
    return render(request, 'locais/lista.html', {'locais': locais})


@login_required
def detalhe_local(request, pk):
    """
    Exibe a página completa de um local com sua galeria de fotos integrada,
    histórico de comentários estruturados e o formulário de atribuição de notas.
    """
    local = get_object_or_404(
        LocalRural.objects.prefetch_related('imagens', 'avaliacoes'),
        pk=pk,
    )

    # Separa apenas os comentários principais e pré-carrega suas respectivas sub-respostas
    comentarios = local.comentarios.filter(pai=None).prefetch_related(
        'respostas', 'respostas__autor', 'autor'
    ).order_by('-criado_em')

    # Localiza se o usuário atual já deixou alguma nota para este local
    avaliacao_usuario = Avaliacao.objects.filter(
        local=local, usuario=request.user
    ).first()

    # Instancia os formulários injetando a nota existente (caso o usuário já tenha avaliado antes)
    form_comentario = ComentarioForm()
    form_avaliacao  = AvaliacaoForm(instance=avaliacao_usuario)

    # Une a imagem de capa principal e as imagens da galeria em uma lista iterável única para o template
    galeria = [local.imagem_principal] + [img.imagem for img in local.imagens.all()]

    return render(request, 'locais/detalhe.html', {
        'local':             local,
        'comentarios':       comentarios,
        'avaliacao_usuario': avaliacao_usuario,
        'form_comentario':   form_comentario,
        'form_avaliacao':    form_avaliacao,
        'galeria':           galeria,
    })


# =============================================================================
# CRUD DE LOCAIS — restrito a ADMIN
# =============================================================================

@admin_required
def criar_local(request):
    """Cria um novo local associando múltiplos uploads de imagens via FormSet."""
    if request.method == 'POST':
        form    = LocalRuralForm(request.POST, request.FILES)
        formset = ImagemLocalFormSet(request.POST, request.FILES)

        # Valida de forma síncrona o formulário do Local e o grupo de arquivos da galeria
        if form.is_valid() and formset.is_valid():
            local = form.save() # Registra o local primeiro para obter a chave primária (ID)
            
            # commit=False gera as instâncias de imagem em memória sem salvá-las imediatamente no banco
            imagens = formset.save(commit=False)
            for img in imagens:
                img.local = local # Vincula a chave estrangeira (FK) ao local recém-criado
                img.save()
            messages.success(request, f'"{local.nome}" criado com sucesso!')
            return redirect('locais:detalhe', pk=local.pk)
    else:
        form    = LocalRuralForm()
        formset = ImagemLocalFormSet()

    return render(request, 'locais/form_local.html', {
        'form':          form,
        'formset':       formset,
        'titulo_pagina': 'Novo Local',
        'btn_label':     'Criar Local',
    })


@admin_required
def editar_local(request, pk):
    """Edita dados estruturais e atualiza/remove mídias vinculadas ao FormSet da galeria."""
    local = get_object_or_404(LocalRural, pk=pk)

    if request.method == 'POST':
        # Associa a instância existente (instance=local) para realizar o UPDATE no banco
        form    = LocalRuralForm(request.POST, request.FILES, instance=local)
        formset = ImagemLocalFormSet(request.POST, request.FILES, instance=local)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save() # O formset do Django lida automaticamente com adições, edições e deleções marcadas
            messages.success(request, f'"{local.nome}" atualizado!')
            return redirect('locais:detalhe', pk=local.pk)
    else:
        form    = LocalRuralForm(instance=local)
        formset = ImagemLocalFormSet(instance=local)

    return render(request, 'locais/form_local.html', {
        'form':          form,
        'formset':       formset,
        'local':         local,
        'titulo_pagina': f'Editar: {local.nome}',
        'btn_label':     'Salvar Alterações',
    })


@admin_required
def deletar_local(request, pk):
    """Remove definitivamente o local físico. O banco apaga em cascata os itens associados."""
    local = get_object_or_404(LocalRural, pk=pk)

    if request.method == 'POST':
        nome = local.nome
        local.delete()
        messages.success(request, f'"{nome}" removido com sucesso.')
        return redirect('locais:lista')

    return render(request, 'locais/confirmar_delete_local.html', {'local': local})


# =============================================================================
# AVALIAÇÃO E COMENTÁRIOS
# =============================================================================

@login_required
def avaliar_local(request, pk):
    """
    Registra ou altera uma nota. O método update_or_create impede a duplicidade de 
    avaliações criadas pelo mesmo estudante em um único local da instituição.
    """
    local = get_object_or_404(LocalRural, pk=pk)

    if request.method == 'POST':
        form = AvaliacaoForm(request.POST)
        if form.is_valid():
            # Cria se não existir; atualiza a coluna 'nota' se a combinação local+usuario já constar no banco
            Avaliacao.objects.update_or_create(
                local=local,
                usuario=request.user,
                defaults={'nota': form.cleaned_data['nota']},
            )
            messages.success(request, 'Avaliação salva!')
        else:
            messages.error(request, 'Selecione uma nota válida.')

    return redirect('locais:detalhe', pk=pk)


@login_required
def comentar_local(request, pk):
    """Insere um novo comentário de primeiro nível (comentário raiz)."""
    local = get_object_or_404(LocalRural, pk=pk)

    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            c = form.save(commit=False)
            c.local  = local
            c.autor  = request.user
            c.pai    = None # marcar como comentário raiz
            c.save()
            messages.success(request, 'Comentário publicado!')
        else:
            messages.error(request, 'Não foi possível publicar.')

    return redirect('locais:detalhe', pk=pk)


@login_required
def responder_comentario(request, pk, comentario_pk):
    """Insere uma resposta vinculada diretamente a um comentário pai existente."""
    local      = get_object_or_404(LocalRural, pk=pk)
    comentario = get_object_or_404(Comentario, pk=comentario_pk, local=local)

    # Trava de Segurança: Impede aninhamento infinito forçando o limite máximo de 1 sub-nível
    if comentario.pai is not None:
        messages.error(request, 'Não é possível responder a uma resposta.')
        return redirect('locais:detalhe', pk=pk)

    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            r = form.save(commit=False)
            r.local  = local
            r.autor  = request.user
            r.pai    = comentario # Vincula este novo comentário como resposta do comentário selecionado
            r.save()
            messages.success(request, 'Resposta publicada!')

    return redirect('locais:detalhe', pk=pk)


@login_required
def deletar_comentario(request, pk, comentario_pk):
    """Remove um comentário ou uma resposta específica do sistema."""
    local      = get_object_or_404(LocalRural, pk=pk)
    comentario = get_object_or_404(Comentario, pk=comentario_pk, local=local)

    # Regra de Permissão: Apenas o próprio autor do texto ou um ADMIN podem excluir o registro
    if request.user != comentario.autor and request.user.tipo_conta != 'ADMIN':
        messages.error(request, 'Sem permissão para deletar este comentário.')
        return redirect('locais:detalhe', pk=pk)

    if request.method == 'POST':
        comentario.delete()
        messages.success(request, 'Comentário removido.')

    return redirect('locais:detalhe', pk=pk)