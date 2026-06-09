/* ============================================================
   GALERIA.JS — Linha de 5 thumbnails + lightbox
   ============================================================ */

document.addEventListener('DOMContentLoaded', function () {
    const overlay  = document.getElementById('lightbox-overlay');
    const imgEl    = document.getElementById('lightbox-img');
    const contador = document.getElementById('lightbox-contador');
    const grid     = document.getElementById('galeria-grid');
    const dados    = document.getElementById('galeria-dados');

    if (!grid || !dados) return;

    const spans = dados.querySelectorAll('span[data-src]');
    if (spans.length === 0) return;

    const VISIVEIS = 5;

    // Coleta todas as fotos em ordem
    const fotos = Array.from(spans).map(function (s) {
        return { src: s.dataset.src, alt: s.dataset.alt || '' };
    });

    const total = fotos.length;

    // ── Monta a linha de thumbnails ──
    grid.innerHTML = '';

    fotos.forEach(function (foto, i) {
        if (i >= VISIVEIS) return;

        const wrapper = document.createElement('div');
        wrapper.className = 'galeria-thumb-wrapper';

        const img = document.createElement('img');
        img.src       = foto.src;
        img.alt       = foto.alt;
        img.className = 'galeria-thumb';

        // 5ª foto com blur e contador quando há mais de 5
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

        wrapper.addEventListener('click', function () {
            indiceAtual = i;
            abrir();
        });

        grid.appendChild(wrapper);
    });

    // ── Lightbox ──
    let indiceAtual = 0;

    if (!overlay) return;

    document.getElementById('lightbox-fechar').addEventListener('click', fechar);

    overlay.addEventListener('click', function (e) {
        if (e.target === overlay) fechar();
    });

    document.getElementById('lightbox-anterior').addEventListener('click', anterior);
    document.getElementById('lightbox-proximo').addEventListener('click', proximo);

    document.addEventListener('keydown', function (e) {
        if (!overlay.classList.contains('ativo')) return;
        if (e.key === 'ArrowLeft')  anterior();
        if (e.key === 'ArrowRight') proximo();
        if (e.key === 'Escape')     fechar();
    });

    function abrir() {
        exibir(indiceAtual);
        overlay.classList.add('ativo');
        document.body.style.overflow = 'hidden';
    }

    function fechar() {
        overlay.classList.remove('ativo');
        document.body.style.overflow = '';
    }

    function anterior() {
        indiceAtual = (indiceAtual - 1 + total) % total;
        exibir(indiceAtual);
    }

    function proximo() {
        indiceAtual = (indiceAtual + 1) % total;
        exibir(indiceAtual);
    }

    function exibir(i) {
        imgEl.src = fotos[i].src;
        imgEl.alt = fotos[i].alt;
        if (contador) {
            contador.textContent = (i + 1) + ' / ' + total;
        }
    }
});
