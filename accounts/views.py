from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from .forms import LoginForm, CadastroComumForm, CadastroAdminForm
from django.core.mail import send_mail
from django.conf import settings
from .models import CodigoVerificacao

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
                usuario = form_comum.save(commit=False) #ainda não salva, precsa do código de verificação
                usuario.is_active = False # desativa a conta até a verificação do email
                usuario.save()
                
                request.session['usuario_verificacao_id'] = usuario.id
                verificacao_email_view(request, usuario)
                
                messages.success(
                    request, 'Conta Comum criada! Por favor, verifique seu e-mail para ativar a conta.'
                )
                return redirect('accounts:verificar_codigo')

        # o processo é o mesmo pro admin, só muda o form e a mensagem
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

        # Se teve erro, mostra qual aba estava ativa para o template reabrir
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
            
            # REALIZA O LOGIN AUTOMÁTICO DO USUÁRIO 🎉
            login(request, usuario)
            
            messages.success(request, f"E-mail verificado com sucesso! Bem-vindo(a), {usuario.nome_completo or usuario.username}!")
            return redirect('mural:index')
            
        except CodigoVerificacao.DoesNotExist:
            # Se o get() não encontrar o código digitado no banco
            messages.error(request, "Código incorreto. Verifique o número enviado ao seu e-mail.")
            
    return render(request, 'accounts/verificar_codigo.html')
# logout por POST pra evitar CSRF — só acessível pra usuários logados
@login_required
def logout_view(request):
    """Logout via POST — protegido contra CSRF."""
    if request.method == 'POST':
        logout(request)
        messages.info(request, 'Você saiu com segurança.')
    return redirect('mural:index')

@login_required
def perfil_view(request):
    """
    Exibe os dados cadastrais e permite a alteração do Nome de Usuário (Nick).
    """
    if request.method == 'POST':
        novo_username = request.POST.get('username', '').strip()
        
        # Validações básicas para manter a ordem do chat
        if not novo_username:
            messages.error(request, "O nome de usuário não pode ficar em branco.")
        elif ' ' in novo_username:
            messages.error(request, "O nome de usuário não pode conter espaços.")
        elif len(novo_username) < 3:
            messages.error(request, "O nick deve conter pelo menos 3 caracteres.")
        else:
            try:
                # Tenta atualizar o identificador do usuário logado
                request.user.username = novo_username
                request.user.save()
                messages.success(request, "Nome de usuário atualizado com sucesso!")
                return redirect('accounts:perfil')
            except IntegrityError:
                # Caso o banco acuse que o username já existe por conta do UNIQUE do modelo
                messages.error(request, "Este nome de usuário já está sendo utilizado por outro membro.")
                
    return render(request, 'accounts/perfil.html', {
        'usuario': request.user
    })

@login_required
def deletar_conta_view(request):
    """
    Recebe o pedido de exclusão de conta via POST, valida a senha 
    e deleta permanentemente o usuário.
    """
    if request.method == 'POST':
        senha_informada = request.POST.get('password', '')
        usuario_atual = request.user
        
        # Verifica se a senha informada corresponde ao hash do banco
        if usuario_atual.check_password(senha_informada):
            # Deleta o registro do banco de dados
            usuario_atual.delete()
            
            # Realiza o logout limpo da sessão do usuário
            logout(request)
            
            messages.success(request, "Sua conta foi removida com sucesso. Esperamos ver você de volta em breve!")
            return redirect('mural:index')
        else:
            messages.error(request, "Falha na exclusão: A senha informada está incorreta.")
            return redirect('accounts:perfil')
            
    return redirect('accounts:perfil')