document.addEventListener('DOMContentLoaded', () => {
    const wrapper = document.getElementById('estrelas-input');
    const inputNota = document.getElementById('id_nota_estrela');
    const notaTexto = document.getElementById('nota-selecionada');

    if (!wrapper || !inputNota) return;

    const metades = wrapper.querySelectorAll('.estrela-metade');
    const icones = wrapper.querySelectorAll('.estrela-icone');
    
    let notaAtual = parseFloat(wrapper.dataset.notaAtual.replace(',', '.')) || 0;

    if (notaAtual > 0) {
        atualizarVisual(notaAtual);
        if (notaTexto) notaTexto.textContent = `${notaAtual.toFixed(1)} / 5.0`;
    }

    metades.forEach(metade => {
        metade.addEventListener('mouseenter', function() {
            atualizarVisual(parseFloat(this.dataset.valor));
        });

        metade.addEventListener('mouseleave', () => atualizarVisual(notaAtual));

        metade.addEventListener('click', function() {
            notaAtual = parseFloat(this.dataset.valor);
            inputNota.value = notaAtual;
            atualizarVisual(notaAtual);
            if (notaTexto) notaTexto.textContent = `${notaAtual.toFixed(1)} / 5.0`;
        });
    });

    function atualizarVisual(valor) {
        icones.forEach((icone, i) => {
            const num = i + 1;
            icone.className = 'estrela-icone bi ' + 
                (num <= Math.floor(valor) ? 'bi-star-fill' : 
                 num === Math.ceil(valor) && valor % 1 !== 0 ? 'bi-star-half' : 'bi-star');
        });
    }
});