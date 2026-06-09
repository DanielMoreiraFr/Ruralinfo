/* ============================================================
   GALERIA_FORM.JS — Adicionar slots de foto dinamicamente
   ============================================================
   O Django formset usa um campo hidden TOTAL_FORMS para saber
   quantos formulários processar no POST. Cada vez que adicionamos
   um slot novo, incrementamos esse número e clonamos o HTML
   do template de formulário vazio.
   ============================================================ */

document.addEventListener('DOMContentLoaded', function () {
    const btnAdicionar = document.getElementById('btn-adicionar-foto');
    const container    = document.getElementById('galeria-formset');
    const totalForms   = document.getElementById('id_imagens-TOTAL_FORMS');

    if (!btnAdicionar || !container || !totalForms) return;

    btnAdicionar.addEventListener('click', function () {
        const indice = parseInt(totalForms.value);

        // Clona o template de formulário vazio
        const template = document.getElementById('template-foto-vazio');
        if (!template) return;

        const novoSlot = template.cloneNode(true);
        novoSlot.id = '';
        novoSlot.style.display = '';
        novoSlot.classList.remove('template-oculto');

        // Substitui o prefixo __prefix__ pelo índice correto
        novoSlot.innerHTML = novoSlot.innerHTML
            .replace(/__prefix__/g, indice);

        // Define a ordem automaticamente
        const campoOrdem = novoSlot.querySelector('input[name$="-ordem"]');
        if (campoOrdem) campoOrdem.value = indice;

        container.appendChild(novoSlot);

        // Atualiza o TOTAL_FORMS para o Django processar o novo slot
        totalForms.value = indice + 1;
    });
});