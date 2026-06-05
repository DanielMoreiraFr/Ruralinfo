/* ============================================================
   PERFIL — Modal de confirmação de exclusão de conta
   Extraído do perfil.html para manter o HTML limpo
   ============================================================ */
document.addEventListener('DOMContentLoaded', function () {
    const modal      = document.getElementById('deleteAccountModal');
    const btnAbrir   = document.getElementById('btnAbrirModalDelete');
    const btnFechar  = document.getElementById('btnFecharModalDelete');
    const inputSenha = document.getElementById('confirmarSenhaInput');

    if (!modal || !btnAbrir) return;

    // Abre o modal
    btnAbrir.addEventListener('click', function () {
        modal.classList.add('active');
        if (inputSenha) inputSenha.focus();
    });

    // Fecha ao clicar em Cancelar
    if (btnFechar) {
        btnFechar.addEventListener('click', function () {
            modal.classList.remove('active');
            if (inputSenha) inputSenha.value = '';
        });
    }

    // Fecha ao clicar no fundo escuro
    modal.addEventListener('click', function (e) {
        if (e.target === modal) {
            modal.classList.remove('active');
            if (inputSenha) inputSenha.value = '';
        }
    });

    // Fecha ao pressionar ESC
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && modal.classList.contains('active')) {
            modal.classList.remove('active');
            if (inputSenha) inputSenha.value = '';
        }
    });
});