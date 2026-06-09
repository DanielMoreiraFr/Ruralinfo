// Alterna a visibilidade do campo de senha (olho aberto / fechado)
function toggleSenhaCadastro(btn) {
    const container = btn.closest('.input-group');
    if (!container) return;
    
    const input = container.querySelector('input');
    const icon = btn.querySelector('i');
    
    // Troca o tipo do input entre password e text e atualiza o ícone do Bootstrap
    if (input.type === 'password') {
        input.type = 'text';
        icon.className = 'bi bi-eye-slash';
    } else {
        input.type = 'password';
        icon.className = 'bi bi-eye';
    }
}

// Gerencia o medidor de força da senha em tempo de execução
function iniciarForcaSenha(inputId, sufixo) {
    const input = document.getElementById(inputId);
    if (!input) return;
    
    const forcaContainer = document.getElementById('forca_' + sufixo);
    const barra = document.getElementById('barra_' + sufixo);
    const txt = document.getElementById('txt_' + sufixo);
    
    // Escuta a digitação no campo de senha
    input.addEventListener('input', function () {
        const val = this.value;
        if (!val) {
            forcaContainer.style.display = 'none'; // Esconde a barra se estiver vazio
            return;
        }
        
        forcaContainer.style.display = 'block';
        let pontos = 0;
        
        // Critérios de validação: tamanho, maiúsculas, números e caracteres especiais
        if (val.length >= 10) pontos++;
        if (/[A-Z]/.test(val)) pontos++;
        if (/\d/.test(val)) pontos++;
        if (/[!@#$%^&*()\-_=+\[\]{}|;:'",.<>?`~\\]/.test(val)) pontos++;
        
        // Configuração de cores e porcentagens da barra de progresso (Bootstrap)
        const escalas = [
            { txt: 'Muito fraca', cor: 'bg-danger', pct: 25 },
            { txt: 'Fraca', cor: 'bg-warning', pct: 50 },
            { txt: 'Boa', cor: 'bg-info', pct: 75 },
            { txt: 'Forte', cor: 'bg-success', pct: 100 }
        ];
        
        // Aplica a estilização correspondente à pontuação alcançada
        const config = escalas[Math.max(0, pontos - 1)];
        barra.style.width = config.pct + '%';
        barra.className = 'progress-bar ' + config.cor;
        txt.textContent = config.txt;
    });
}

// Aguarda o carregamento do HTML para configurar as abas da tela de cadastro
document.addEventListener('DOMContentLoaded', function () {
    // Alternância de Abas Manual
    const botoes = document.querySelectorAll('#tabsCadastro .nav-link');
    const panes = document.querySelectorAll('.tab-content .tab-pane');

    // Controla a troca de abas (ex: Estudante / Servidor) removendo e injetando as classes active
    botoes.forEach(botao => {
        botao.addEventListener('click', function () {
            const target = this.getAttribute('data-target');
            
            botoes.forEach(b => b.classList.remove('active'));
            panes.forEach(p => p.classList.remove('show', 'active'));
            
            this.classList.add('active');
            const targetPane = document.getElementById(target);
            if (targetPane) {
                targetPane.classList.add('show', 'active');
            }
        });
    });
});