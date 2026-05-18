/* Toggle de visibilidade da senha no cadastro.*/
function toggleSenhaCadastro(btn) {
    var input = btn.closest('.input-group').querySelector('input');
    var icon  = btn.querySelector('i');

    if (input.type === 'password') {
        input.type     = 'text';
        icon.className = 'bi bi-eye-slash';
    } else {
        input.type     = 'password';
        icon.className = 'bi bi-eye';
    }
}

/* Indicador de força de senha
   Chamado pelo _campos_senha.html passando os IDs gerados

       iniciarForcaSenha('id_comum-senha', 'comum'); */
function iniciarForcaSenha(inputId, sufixo) {
    var input = document.getElementById(inputId);
    if (!input) return;

    var forca = document.getElementById('forca_'  + sufixo);
    var barra = document.getElementById('barra_'  + sufixo);
    var txt   = document.getElementById('txt_'    + sufixo);

    input.addEventListener('input', function () {
        var s = this.value;
        if (!s) { forca.style.display = 'none'; return; }
        forca.style.display = 'block';

        var pts = 0;
        if (s.length >= 10)                                        pts++;
        if (/[A-Z]/.test(s))                                      pts++;
        if (/\d/.test(s))                                         pts++;
        if (/[!@#$%^&*()\-_=+\[\]{}|;:'",.<>?`~\\]/.test(s))    pts++;

        var cfg = [
            { label: 'Muito fraca', cor: 'bg-danger',  pct: 25  },
            { label: 'Fraca',       cor: 'bg-warning', pct: 50  },
            { label: 'Boa',         cor: 'bg-info',    pct: 75  },
            { label: 'Forte',       cor: 'bg-success', pct: 100 },
        ];
        var c = cfg[Math.max(0, pts - 1)];

        barra.style.width   = c.pct + '%';
        barra.className     = 'progress-bar ' + c.cor;
        txt.textContent     = c.label;
    });
}