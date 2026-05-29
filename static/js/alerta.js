document.addEventListener('DOMContentLoaded', function () {
    // 1. Descarte automatizado dos alertas Django
    document.querySelectorAll('.django-messages .alert').forEach(function (alert) {
        setTimeout(function () {
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-8px)';
            setTimeout(() => alert.remove(), 300);
        }, 5000);
    });

    // 2. Acoplamento de Menu Sanduíche Responsivo
    const menuToggle = document.getElementById('menuToggle');
    const navbarMenu = document.getElementById('navbarMenu');
    if (menuToggle && navbarMenu) {
        menuToggle.addEventListener('click', function (e) {
            e.stopPropagation();
            navbarMenu.classList.toggle('active');
        });
    }

    // 3. Gerenciamento Próprio de Dropdown de Conta
    const dropdownToggle = document.getElementById('userDropdownToggle');
    const dropdownMenu = document.getElementById('userDropdownMenu');
    if (dropdownToggle && dropdownMenu) {
        dropdownToggle.addEventListener('click', function (e) {
            e.stopPropagation();
            dropdownMenu.classList.toggle('active');
        });
    }

    // Clique externo fecha elementos suspensos abertos
    document.addEventListener('click', function () {
        if (dropdownMenu) dropdownMenu.classList.remove('active');
        if (navbarMenu) navbarMenu.classList.remove('active');
    });
});