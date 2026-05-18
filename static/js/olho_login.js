/* Toggle de visibilidade da senha na tela de login */
function toggleSenha(inputId, btn) {
    var input = document.getElementById(inputId);
    var icon  = btn.querySelector('i');

    if (input.type === 'password') {
        input.type     = 'text';
        icon.className = 'bi bi-eye-slash';
    } else {
        input.type     = 'password';
        icon.className = 'bi bi-eye';
    }
}