/* Controle do sidebar — sem animação, apenas show/hide */
function abrirSidebar() {
    document.getElementById('sidebar').classList.add('aberto');
    document.getElementById('sidebar-overlay').classList.add('ativo');
}

function fecharSidebar() {
    document.getElementById('sidebar').classList.remove('aberto');
    document.getElementById('sidebar-overlay').classList.remove('ativo');
}

/* Fecha ao pressionar ESC */
document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') fecharSidebar();
});