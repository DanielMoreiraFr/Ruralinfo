/* ============================================================
   PERFIL — Modal de confirmação de exclusão de conta
   Extraído do perfil.html para manter o HTML limpo
   ============================================================ */

// Aguarda o HTML carregar completamente
document.addEventListener('DOMContentLoaded', function () {
    const modal      = document.getElementById('deleteAccountModal');
    const btnAbrir   = document.getElementById('btnAbrirModalDelete');
    const btnFechar  = document.getElementById('btnFecharModalDelete');
    const inputSenha = document.getElementById('confirmarSenhaInput');

    // Cancela a execução se os elementos do modal não existirem
    if (!modal || !btnAbrir) return;

    // Abre o modal e foca no campo de senha
    btnAbrir.addEventListener('click', function () {
        modal.classList.add('active');
        if (inputSenha) inputSenha.focus();
    });

    // Fecha o modal ao clicar em "Cancelar" e limpa o campo de senha
    if (btnFechar) {
        btnFechar.addEventListener('click', function () {
            modal.classList.remove('active');
            if (inputSenha) inputSenha.value = '';
        });
    }

    // Fecha o modal ao clicar no fundo escuro de fora e limpa a senha
    modal.addEventListener('click', function (e) {
        if (e.target === modal) {
            modal.classList.remove('active');
            if (inputSenha) inputSenha.value = '';
        }
    });

    // Fecha o modal ao pressionar a tecla ESC e limpa a senha
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && modal.classList.contains('active')) {
            modal.classList.remove('active');
            if (inputSenha) inputSenha.value = '';
        }
    });
});