/* ============================================================
   GALERIA.JS — Lightbox de fotos do local
   ============================================================ */

document.addEventListener('DOMContentLoaded', function () {
    const overlay   = document.getElementById('lightbox-overlay');
    const imgEl     = document.getElementById('lightbox-img');
    const contador  = document.getElementById('lightbox-contador');
    const thumbs    = document.querySelectorAll('.galeria-thumb');

    if (!overlay || thumbs.length === 0) return;

    // Coleta todas as URLs das fotos em ordem
    const fotos = Array.from(thumbs).map(function (t) {
        return { src: t.src, alt: t.alt };
    });

    let indiceAtual = 0;

    // Abre o lightbox na foto clicada
    thumbs.forEach(function (thumb, i) {
        thumb.addEventListener('click', function () {
            indiceAtual = i;
            abrir();
        });
    });

    // Fechar
    document.getElementById('lightbox-fechar').addEventListener('click', fechar);
    overlay.addEventListener('click', function (e) {
        if (e.target === overlay) fechar();
    });

    // Navegação com botões
    document.getElementById('lightbox-anterior').addEventListener('click', anterior);
    document.getElementById('lightbox-proximo').addEventListener('click', proximo);

    // Navegação com teclado
    document.addEventListener('keydown', function (e) {
        if (!overlay.classList.contains('ativo')) return;
        if (e.key === 'ArrowLeft')  anterior();
        if (e.key === 'ArrowRight') proximo();
        if (e.key === 'Escape')     fechar();
    });

    // ── Helpers ──

    function abrir() {
        exibir(indiceAtual);
        overlay.classList.add('ativo');
        document.body.style.overflow = 'hidden'; // impede scroll da página
    }

    function fechar() {
        overlay.classList.remove('ativo');
        document.body.style.overflow = '';
    }

    function anterior() {
        indiceAtual = (indiceAtual - 1 + fotos.length) % fotos.length;
        exibir(indiceAtual);
    }

    function proximo() {
        indiceAtual = (indiceAtual + 1) % fotos.length;
        exibir(indiceAtual);
    }

    function exibir(i) {
        imgEl.src = fotos[i].src;
        imgEl.alt = fotos[i].alt;
        if (contador) {
            contador.textContent = (i + 1) + ' / ' + fotos.length;
        }
    }
});