/* ============================================================
   COMENTARIOS.JS — Toggle do form de resposta inline
   ============================================================ */

document.addEventListener('DOMContentLoaded', function () {

    // Botão "Responder" — abre/fecha o form de resposta
    document.querySelectorAll('.btn-responder').forEach(function (btn) {
        btn.addEventListener('click', function () {
            const comentarioId = this.dataset.comentarioId;
            const form = document.getElementById('form-resposta-' + comentarioId);
            if (!form) return;

            const visivel = form.classList.contains('visivel');

            // Fecha todos os outros forms abertos
            document.querySelectorAll('.form-resposta.visivel').forEach(function (f) {
                f.classList.remove('visivel');
            });

            // Abre este (ou fecha se já estava aberto)
            if (!visivel) {
                form.classList.add('visivel');
                form.querySelector('textarea').focus();
            }
        });
    });

    // Botão "Cancelar" dentro do form de resposta
    document.querySelectorAll('.btn-cancelar-resposta').forEach(function (btn) {
        btn.addEventListener('click', function () {
            const form = this.closest('.form-resposta');
            if (form) {
                form.classList.remove('visivel');
                form.querySelector('textarea').value = '';
            }
        });
    });
});