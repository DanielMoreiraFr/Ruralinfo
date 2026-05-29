function toggleSenha(btn) {
    const container = btn.closest('.input-group');
    if (!container) return;
    
    const input = container.querySelector('input');
    const icon = btn.querySelector('i');
    
    if (input.type === 'password') {
        input.type = 'text';
        icon.className = 'bi bi-eye-slash';
    } else {
        input.type = 'password';
        icon.className = 'bi bi-eye';
    }
}