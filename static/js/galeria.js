/* ============================================================
   GALERIA.JS — Linha de 5 thumbnails + lightbox
   ============================================================ */

// Aguarda o HTML carregar completamente
document.addEventListener('DOMContentLoaded', function () {
    const overlay  = document.getElementById('lightbox-overlay');
    const imgEl    = document.getElementById('lightbox-img');
    const contador = document.getElementById('lightbox-contador');
    const grid     = document.getElementById('galeria-grid');
    const dados    = document.getElementById('galeria-dados');

    // Cancela se os elementos essenciais da galeria não existirem
    if (!grid || !dados) return;

    const spans = dados.querySelectorAll('span[data-src]');
    if (spans.length === 0) return;

    const VISIVEIS = 5;

    // Mapeia os dados das fotos recebidos do HTML do Django
    const fotos = Array.from(spans).map(function (s) {
        return { src: s.dataset.src, alt: s.dataset.alt || '' };
    });

    const total = fotos.length;

    // Limpa o grid antes de renderizar as miniaturas
    grid.innerHTML = '';

    // Gera dinamicamente as miniaturas na tela (limite de 5 visíveis)
    fotos.forEach(function (foto, i) {
        if (i >= VISIVEIS) return;

        const wrapper = document.createElement('div');
        wrapper.className = 'galeria-thumb-wrapper';

        const img = document.createElement('img');
        img.src       = foto.src;
        img.alt       = foto.alt;
        img.className = 'galeria-thumb';

        // Se houver mais de 5 fotos, aplica efeito de blur e o contador oculto (+X) na última miniatura
        if (i === VISIVEIS - 1 && total > VISIVEIS) {
            wrapper.classList.add('galeria-thumb-mais');

            const blurOverlay = document.createElement('div');
            blurOverlay.className   = 'galeria-blur-overlay';
            blurOverlay.textContent = '+' + (total - VISIVEIS + 1);

            wrapper.appendChild(img);
            wrapper.appendChild(blurOverlay);
        } else {
            wrapper.appendChild(img);
        }

        // Abre o lightbox na imagem correspondente ao clicar na miniatura
        wrapper.addEventListener('click', function () {
            indiceAtual = i;
            abrir();
        });

        grid.appendChild(wrapper);
    });

    // ── Lógica do Lightbox (Visualizador em Tela Cheia) ──
    let indiceAtual = 0;

    if (!overlay) return;

    // Eventos de fechar e navegar clicando nos botões ou no fundo escuro
    document.getElementById('lightbox-fechar').addEventListener('click', fechar);

    overlay.addEventListener('click', function (e) {
        if (e.target === overlay) fechar();
    });

    document.getElementById('lightbox-anterior').addEventListener('click', anterior);
    document.getElementById('lightbox-proximo').addEventListener('click', proximo);

    // Atalhos do teclado (Seta esquerda, Seta direita e Esc)
    document.addEventListener('keydown', function (e) {
        if (!overlay.classList.contains('ativo')) return;
        if (e.key === 'ArrowLeft')  anterior();
        if (e.key === 'ArrowRight') proximo();
        if (e.key === 'Escape')     fechar();
    });

    // Abre a tela cheia e bloqueia a barra de rolagem da página
    function abrir() {
        exibir(indiceAtual);
        overlay.classList.add('ativo');
        document.body.style.overflow = 'hidden';
    }

    // Fecha a tela cheia e libera a rolagem da página novamente
    function fechar() {
        overlay.classList.remove('ativo');
        document.body.style.overflow = '';
    }

    // Avança para a imagem anterior (retorna ao fim se estiver na primeira)
    function anterior() {
        indiceAtual = (indiceAtual - 1 + total) % total;
        exibir(indiceAtual);
    }

    // Avança para a próxima imagem (retorna ao início se estiver na última)
    function proximo() {
        indiceAtual = (indiceAtual + 1) % total;
        exibir(indiceAtual);
    }

    // Atualiza a imagem e o contador numérico exibidos no lightbox
    function exibir(i) {
        imgEl.src = fotos[i].src;
        imgEl.alt = fotos[i].alt;
        if (contador) {
            contador.textContent = (i + 1) + ' / ' + total;
        }
    }
});