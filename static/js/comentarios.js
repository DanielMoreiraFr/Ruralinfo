/* ============================================================
   COMENTARIOS.JS — Toggle do form de resposta inline
   ============================================================ */

// Aguarda o carregamento do HTML
document.addEventListener('DOMContentLoaded', function () {

    // Gerencia o clique no botão "Responder"
    document.querySelectorAll('.btn-responder').forEach(function (btn) {
        btn.addEventListener('click', function () {
            const comentarioId = this.dataset.comentarioId;
            const form = document.getElementById('form-resposta-' + comentarioId);
            if (!form) return;

            const visivel = form.classList.contains('visivel');

            // Fecha todos os outros formulários de resposta que estiverem abertos
            document.querySelectorAll('.form-resposta.visivel').forEach(function (f) {
                f.classList.remove('visivel');
            });

            // Abre o formulário atual (ou fecha se já estava aberto) e foca no campo de texto
            if (!visivel) {
                form.classList.add('visivel');
                form.querySelector('textarea').focus();
            }
        });
    });

    // Gerencia o clique no botão "Cancelar" do formulário de resposta
    document.querySelectorAll('.btn-cancelar-resposta').forEach(function (btn) {
        btn.addEventListener('click', function () {
            const form = this.closest('.form-resposta');
            if (form) {
                form.classList.remove('visivel'); // Esconde o formulário
                form.querySelector('textarea').value = ''; // Limpa o texto digitado
            }
        });
    });
});