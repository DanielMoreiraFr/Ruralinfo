/* ============================================================
   ESTRELAS.JS — Avaliação interativa de 0.5 a 5.0
   ============================================================
   Estratégia: cada estrela cheia (★) é dividida em duas metades
   clicáveis via CSS/JS. Metade esquerda = X.5, metade direita = X.0.
   O valor é escrito num input hidden que o form envia ao Django.
   ============================================================ */

// Aguarda o HTML carregar
document.addEventListener('DOMContentLoaded', function () {
    const wrapper    = document.getElementById('estrelas-input');
    const inputNota  = document.getElementById('id_nota_estrela');
    const notaTexto  = document.getElementById('nota-selecionada');

    // Cancela a execução se os elementos essenciais não existirem na página
    if (!wrapper || !inputNota) return;

    const metades = wrapper.querySelectorAll('.estrela-metade');

    // Recupera a nota anterior enviada pelo Django (ou define 0 se for a primeira vez)
    let notaAtual = parseFloat(wrapper.dataset.notaAtual) || 0;

    // Se o usuário já tiver avaliado antes, exibe visualmente as estrelas preenchidas
    if (notaAtual > 0) {
        marcarAte(notaAtual);
        atualizarTexto(notaAtual);
    }

    // Configura os eventos para cada metade de estrela
    metades.forEach(function (metade) {
        
        // Efeito Hover: acende temporariamente as estrelas até onde o mouse passar
        metade.addEventListener('mouseenter', function () {
            const valor = parseFloat(this.dataset.valor);
            destacarAte(valor);
        });

        // Retorno do mouse: apaga os hovers e restaura a nota que já estava salva
        metade.addEventListener('mouseleave', function () {
            if (notaAtual > 0) {
                marcarAte(notaAtual);
            } else {
                limparDestaques();
            }
        });

        // Clique: define e salva permanentemente a nova nota no input oculto do formulário
        metade.addEventListener('click', function () {
            notaAtual = parseFloat(this.dataset.valor);
            inputNota.value = notaAtual;
            marcarAte(notaAtual);
            atualizarTexto(notaAtual);
        });
    });

    // ── Funções Auxiliares (Helpers) ──

    // Aplica a classe visual de hover até a metade apontada pelo mouse
    function destacarAte(valor) {
        metades.forEach(function (m) {
            m.classList.toggle('hover', parseFloat(m.dataset.valor) <= valor);
            m.classList.remove('preenchida');
        });
    }

    // Fixa a classe de estrela preenchida com base na nota definitiva escolhida
    function marcarAte(valor) {
        metades.forEach(function (m) {
            const v = parseFloat(m.dataset.valor);
            m.classList.toggle('preenchida', v <= valor);
            m.classList.remove('hover');
        });
    }

    // Remove todas as classes de preenchimento e hover das estrelas
    function limparDestaques() {
        metades.forEach(function (m) {
            m.classList.remove('hover', 'preenchida');
        });
    }

    // Atualiza o contador de texto ao lado das estrelas (Ex: 4.5 / 5.0)
    function atualizarTexto(valor) {
        if (notaTexto) {
            notaTexto.textContent = valor.toFixed(1) + ' / 5.0';
        }
    }
});