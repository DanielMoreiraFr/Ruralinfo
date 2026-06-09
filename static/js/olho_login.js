// Alterna a visibilidade da senha (olho aberto / fechado) no login
function toggleSenha(btn) {
    // Encontra o grupo do input que contém o botão clicado
    const container = btn.closest('.input-group');
    if (!container) return;
    
    const input = container.querySelector('input');
    const icon = btn.querySelector('i');
    
    // Altera o tipo do input e o ícone do Bootstrap correspondente
    if (input.type === 'password') {
        input.type = 'text';
        icon.className = 'bi bi-eye-slash';
    } else {
        input.type = 'password';
        icon.className = 'bi bi-eye';
    }
}