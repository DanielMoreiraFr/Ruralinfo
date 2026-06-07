/* ============================================================
   ESTRELAS.JS — Avaliação interativa de 0.5 a 5.0
   ============================================================
   Estratégia: cada estrela cheia (★) é dividida em duas metades
   clicáveis via CSS/JS. Metade esquerda = X.5, metade direita = X.0.
   O valor é escrito num input hidden que o form envia ao Django.
   ============================================================ */

document.addEventListener('DOMContentLoaded', function () {
    const wrapper    = document.getElementById('estrelas-input');
    const inputNota  = document.getElementById('id_nota_estrela');
    const notaTexto  = document.getElementById('nota-selecionada');

    if (!wrapper || !inputNota) return;

    const metades = wrapper.querySelectorAll('.estrela-metade');

    // Nota atual (se o usuário já avaliou, o Django passa via data-nota)
    let notaAtual = parseFloat(wrapper.dataset.notaAtual) || 0;

    // Preenche visualmente a nota já salva ao carregar
    if (notaAtual > 0) {
        marcarAte(notaAtual);
        atualizarTexto(notaAtual);
    }

    // Hover — acende as estrelas até o ponto do mouse
    metades.forEach(function (metade) {
        metade.addEventListener('mouseenter', function () {
            const valor = parseFloat(this.dataset.valor);
            destacarAte(valor);
        });

        metade.addEventListener('mouseleave', function () {
            // Volta para a nota salva
            if (notaAtual > 0) {
                marcarAte(notaAtual);
            } else {
                limparDestaques();
            }
        });

        // Clique — salva a nota
        metade.addEventListener('click', function () {
            notaAtual = parseFloat(this.dataset.valor);
            inputNota.value = notaAtual;
            marcarAte(notaAtual);
            atualizarTexto(notaAtual);
        });
    });

    // ── Helpers ──

    function destacarAte(valor) {
        metades.forEach(function (m) {
            m.classList.toggle('hover', parseFloat(m.dataset.valor) <= valor);
            m.classList.remove('preenchida');
        });
    }

    function marcarAte(valor) {
        metades.forEach(function (m) {
            const v = parseFloat(m.dataset.valor);
            m.classList.toggle('preenchida', v <= valor);
            m.classList.remove('hover');
        });
    }

    function limparDestaques() {
        metades.forEach(function (m) {
            m.classList.remove('hover', 'preenchida');
        });
    }

    function atualizarTexto(valor) {
        if (notaTexto) {
            notaTexto.textContent = valor.toFixed(1) + ' / 5.0';
        }
    }
});