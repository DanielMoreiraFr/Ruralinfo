/* ============================================================
   GALERIA_FORM.JS — Adicionar slots de foto dinamicamente
   ============================================================
   O Django formset usa um campo hidden TOTAL_FORMS para saber
   quantos formulários processar no POST. Cada vez que adicionamos
   um slot novo, incrementamos esse número e clonamos o HTML
   do template de formulário vazio.
   ============================================================ */

// Aguarda o HTML carregar completamente
document.addEventListener('DOMContentLoaded', function () {
    const btnAdicionar = document.getElementById('btn-adicionar-foto');
    const container    = document.getElementById('galeria-formset');
    const totalForms   = document.getElementById('id_imagens-TOTAL_FORMS');

    // Cancela a execução se os elementos do gerenciador de formset não existirem
    if (!btnAdicionar || !container || !totalForms) return;

    // Escuta o clique para gerar um novo campo de imagem
    btnAdicionar.addEventListener('click', function () {
        const indice = parseInt(totalForms.value);

        // Busca o template HTML invisível configurado no Django
        const template = document.getElementById('template-foto-vazio');
        if (!template) return;

        // Clona o nó do template e remove as restrições de visibilidade
        const novoSlot = template.cloneNode(true);
        novoSlot.id = '';
        novoSlot.style.display = '';
        novoSlot.classList.remove('template-oculto');

        // Substitui a string curinga '__prefix__' pelo índice numérico atual da lista
        novoSlot.innerHTML = novoSlot.innerHTML
            .replace(/__prefix__/g, indice);

        // Preenche o campo de ordenação do formulário baseado no índice atual
        const campoOrdem = novoSlot.querySelector('input[name$="-ordem"]');
        if (campoOrdem) campoOrdem.value = indice;

        // Injeta o novo formulário de upload no container da galeria
        container.appendChild(novoSlot);

        // Incrementa o contador geral para o Django validar a quantidade certa no POST
        totalForms.value = indice + 1;
    });
});