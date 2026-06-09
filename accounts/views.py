from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.db import IntegrityError
from .forms import LoginForm, CadastroComumForm, CadastroAdminForm
from django.core.mail import send_mail
from django.conf import settings
from .models import CodigoVerificacao

def login_view(request):
    """
    Formulário de Login Personalizado.
    Autentica usando o username composto (email_TIPO) montado pelo LoginForm.
    """
    # Redireciona o usuário para a home se ele já estiver logado no sistema
    if request.user.is_authenticated:
        return redirect('mural:index')

    # Valida as credenciais recebidas via POST e efetua o login se tudo estiver correto
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


def cadastro_view(request):
    """
    Formulário de Cadastro Duplo.
    Exibe dois formulários na mesma página (COMUM e ADMIN) e gerencia o salvamento com base na aba ativa do template.
    """
    # Redireciona o usuário para a home se ele já estiver logado no sistema
    if request.user.is_authenticated:
        return redirect('mural:index')

    form_comum = CadastroComumForm(prefix='comum')
    form_admin = CadastroAdminForm(prefix='admin')

    # Identifica qual formulário foi enviado através do campo oculto do template
    if request.method == 'POST':
        tipo = request.POST.get('tipo_formulario')

        # Processa e salva o formulário se o envio veio da aba de Usuário Comum
        if tipo == 'comum':
            form_comum = CadastroComumForm(request.POST, prefix='comum')
            if form_comum.is_valid():
                usuario = form_comum.save(commit=False) #ainda não salva, precsa do código de verificação
                usuario.is_active = False # desativa a conta até a verificação do email
                usuario.save()
                
                request.session['usuario_verificacao_id'] = usuario.id
                verificacao_email_view(request, usuario)
                
                messages.success(
                    request, 'Conta Comum criada! Por favor, verifique seu e-mail para ativar a conta.'
                )
                return redirect('accounts:verificar_codigo')

        # Processa e salva o formulário dentro de uma transação se o envio veio da aba de Admin
        elif tipo == 'admin':
            form_admin = CadastroAdminForm(request.POST, prefix='admin')
            if form_admin.is_valid():
                try:
                    # Deixa o save() do form consumir o convite atomicamente
                    usuario = form_admin.save()
                    usuario.is_active = False
                    usuario.save()
 
                    request.session['usuario_verificacao_id'] = usuario.id
                    verificacao_email_view(request, usuario)
 
                    messages.success(
                        request, 'Conta Admin criada! Por favor, verifique seu e-mail para ativar a conta.'
                    )
                    return redirect('accounts:verigicar_codigo')
                except Exception:
                    messages.error(
                        request,
                        'Erro ao criar a conta. O código de convite não foi consumido, tente novamente.'
                    )
                    aba_ativa = 'admin'

        # Mantém a aba correta aberta no template caso o formulário retorne com erros de validação
        aba_ativa = tipo or 'comum'
    else:
        aba_ativa = 'comum'

    return render(request, 'accounts/cadastro.html', {
        'form_comum': form_comum,
        'form_admin': form_admin,
        'aba_ativa':  aba_ativa,
    })
    
def verificacao_email_view(request, usuario):
    codigo_obj = CodigoVerificacao.objects.create(usuario=usuario)
    
    send_mail(
        subject='Seu código de cerificação - Ruralinfo',
        message=f'Olá, {usuario.nome_completo or usuario.username}!\n\nUse o seguinte código para verificar seu e-mail: {codigo_obj.codigo}\n\nEste código é válido por 15 minutos.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[usuario.email],
        fail_silently=False,
    )
    
def verificar_codigo_view(request):
    """
    Exibe a tela para inserção do código de 6 dígitos e valida o número digitado.
    Se estiver correto, ativa o usuário e realiza o login automático.
    """
    # Recupera o ID do usuário que acabou de se cadastrar da sessão temporária
    usuario_id = request.session.get('usuario_verificacao_id')
    
    # Se não houver ID na sessão, significa que a pessoa não veio do cadastro
    if not usuario_id:
        messages.error(request, "Sessão expirada ou inválida. Por favor, faça o cadastro novamente.")
        return redirect('accounts:cadastro')
        
    if request.method == 'POST':
        codigo_digitado = request.POST.get('codigo', '').strip()
        
        try:
            # Busca se existe esse código atrelado a esse usuário específico
            codigo_obj = CodigoVerificacao.objects.get(codigo=codigo_digitado, usuario_id=usuario_id)
            
            # Verifica se os 15 minutos já passaram
            if codigo_obj.esta_expirado():
                messages.error(request, "Este código de ativação já expirou. Por favor, refaça o cadastro.")
                codigo_obj.delete()
                return redirect('accounts:cadastro')
            
            # Se encontrou o código e está no prazo: Ativa o usuário!
            usuario = codigo_obj.usuario
            usuario.is_active = True
            usuario.save()
            
            # Deleta o código do banco para que não possa ser usado de novo
            codigo_obj.delete()
            
            # Limpa o ID da sessão, pois ele não é mais necessário
            del request.session['usuario_verificacao_id']
        
            
            messages.success(request, f"E-mail verificado com sucesso! Bem-vindo(a), {usuario.nome_completo or usuario.username}!")
            return redirect('accounts:login')
            
        except CodigoVerificacao.DoesNotExist:
            # Se o get() não encontrar o código digitado no banco
            messages.error(request, "Código incorreto. Verifique o número enviado ao seu e-mail.")
            
    return render(request, 'accounts/verificar_codigo.html')
# logout por POST pra evitar CSRF — só acessível pra usuários logados
@login_required
def logout_view(request):
    """ Finaliza a sessão ativa do usuário atual no navegador. """
    # Só processa o encerramento se a requisição vier via método POST por segurança
    if request.method == 'POST':
        logout(request)
        messages.info(request, 'Você saiu com segurança.')
    return redirect('mural:index')


# Bloqueia o acesso direto de usuários anônimos à rota de perfil
@login_required
def perfil_view(request):
    """ Exibe o perfil do usuário e processa a alteração do nickname. """
    
    if request.method == 'POST':
        novo_username = request.POST.get('username', '').strip()
        
        # Validações de formato do nome de usuário
        if not novo_username:
            messages.error(request, "O nome de usuário não pode ficar em branco.")
        elif ' ' in novo_username:
            messages.error(request, "O nome de usuário não pode conter espaços.")
        elif len(novo_username) < 3:
            messages.error(request, "O nick deve conter pelo menos 3 caracteres.")
        else:
            try:
                # Atualiza o username do usuário logado
                user = request.user
                user.username = novo_username
                user.save()
                
                # Atualiza a sessão para manter o usuário logado após a mudança de credenciais
                update_session_auth_hash(request, user)
                
                messages.success(request, "Nome de usuário atualizado com sucesso!")
                return redirect('accounts:perfil')
                
            except IntegrityError:
                # Trata duplicidade caso o username já exista no banco (Unique Constraint)
                messages.error(request, "Este nome de usuário já está sendo utilizado por outro membro.")
                
    return render(request, 'accounts/perfil.html', {
        'usuario': request.user
    })


# Bloqueia o acesso direto de usuários anônimos à rota de exclusão de conta
@login_required
def deletar_conta_view(request):
    """ Remove permanentemente o registro do usuário atual do banco de dados após confirmar a senha. """
    # Só executa a exclusão definitiva se a requisição vier via método POST por segurança
    if request.method == 'POST':
        senha_informada = request.POST.get('password', '')
        usuario_atual = request.user
        
        # Valida se a senha enviada bate com o hash criptografado armazenado no banco de dados
        if usuario_atual.check_password(senha_informada):
            # Deleta o registro do usuário
            usuario_atual.delete()
            
            # Limpa os dados de sessão do navegador do cliente
            logout(request)
            
            messages.success(request, "Sua conta foi removida com sucesso. Esperamos ver você de volta em breve!")
            return redirect('mural:index')
        else:
            messages.error(request, "Falha na exclusão: A senha informada está incorreta.")
            return redirect('accounts:perfil')
            
    return redirect('accounts:perfil')