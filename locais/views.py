from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import LocalRural, ImagemLocal, Avaliacao, Comentario
from .forms import AvaliacaoForm, ComentarioForm, LocalRuralForm, ImagemLocalFormSet


# =============================================================================
# DECORATOR — acesso restrito a ADMIN do sistema
# =============================================================================

def admin_required(view_func):
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.tipo_conta != 'ADMIN':
            messages.error(request, 'Acesso restrito a administradores.')
            return redirect('locais:lista')
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return wrapper


# =============================================================================
# VIEWS PÚBLICAS (autenticados)
# =============================================================================

@login_required
def lista_locais(request):
    locais = LocalRural.objects.prefetch_related('avaliacoes').all()
    return render(request, 'locais/lista.html', {'locais': locais})


@login_required
def detalhe_local(request, pk):
    local = get_object_or_404(
        LocalRural.objects.prefetch_related('imagens', 'avaliacoes'),
        pk=pk,
    )

    comentarios = local.comentarios.filter(pai=None).prefetch_related(
        'respostas', 'respostas__autor', 'autor'
    ).order_by('-criado_em')

    avaliacao_usuario = Avaliacao.objects.filter(
        local=local, usuario=request.user
    ).first()

    form_comentario = ComentarioForm()
    form_avaliacao  = AvaliacaoForm(instance=avaliacao_usuario)

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
    """Cria um novo local com imagens da galeria."""
    if request.method == 'POST':
        form    = LocalRuralForm(request.POST, request.FILES)
        formset = ImagemLocalFormSet(request.POST, request.FILES)

        if form.is_valid() and formset.is_valid():
            local = form.save()
            # Vincula cada imagem do formset ao local recém-criado
            imagens = formset.save(commit=False)
            for img in imagens:
                img.local = local
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
    """Edita dados e galeria de um local existente."""
    local = get_object_or_404(LocalRural, pk=pk)

    if request.method == 'POST':
        form    = LocalRuralForm(request.POST, request.FILES, instance=local)
        formset = ImagemLocalFormSet(request.POST, request.FILES, instance=local)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
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
    """Deleta um local e todas as suas imagens, avaliações e comentários."""
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
    local = get_object_or_404(LocalRural, pk=pk)

    if request.method == 'POST':
        form = AvaliacaoForm(request.POST)
        if form.is_valid():
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
    local = get_object_or_404(LocalRural, pk=pk)

    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            c = form.save(commit=False)
            c.local  = local
            c.autor  = request.user
            c.pai    = None
            c.save()
            messages.success(request, 'Comentário publicado!')
        else:
            messages.error(request, 'Não foi possível publicar.')

    return redirect('locais:detalhe', pk=pk)


@login_required
def responder_comentario(request, pk, comentario_pk):
    local      = get_object_or_404(LocalRural, pk=pk)
    comentario = get_object_or_404(Comentario, pk=comentario_pk, local=local)

    if comentario.pai is not None:
        messages.error(request, 'Não é possível responder a uma resposta.')
        return redirect('locais:detalhe', pk=pk)

    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            r = form.save(commit=False)
            r.local  = local
            r.autor  = request.user
            r.pai    = comentario
            r.save()
            messages.success(request, 'Resposta publicada!')

    return redirect('locais:detalhe', pk=pk)


@login_required
def deletar_comentario(request, pk, comentario_pk):
    local      = get_object_or_404(LocalRural, pk=pk)
    comentario = get_object_or_404(Comentario, pk=comentario_pk, local=local)

    if request.user != comentario.autor and request.user.tipo_conta != 'ADMIN':
        messages.error(request, 'Sem permissão para deletar este comentário.')
        return redirect('locais:detalhe', pk=pk)

    if request.method == 'POST':
        comentario.delete()
        messages.success(request, 'Comentário removido.')

    return redirect('locais:detalhe', pk=pk)