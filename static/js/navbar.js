document.addEventListener('DOMContentLoaded', function () {

    // ── Menu mobile ──
    const menuToggle = document.getElementById('menuToggle');
    const navbarMenu = document.getElementById('navbarMenu');
    if (menuToggle && navbarMenu) {
        menuToggle.addEventListener('click', function (e) {
            e.stopPropagation();
            navbarMenu.classList.toggle('active');
        });
    }

    // ── Dropdown do usuário ──
    const dropdownToggle = document.getElementById('userDropdownToggle');
    const dropdownMenu   = document.getElementById('userDropdownMenu');
    const dropdownArrow  = document.getElementById('dropdownArrow');

    if (dropdownToggle && dropdownMenu) {
        dropdownToggle.addEventListener('click', function (e) {
            e.stopPropagation();
            e.preventDefault();
            const aberto = dropdownMenu.classList.contains('active');
            dropdownMenu.classList.toggle('active');
            if (dropdownArrow) {
                dropdownArrow.style.transform = aberto ? 'rotate(0deg)' : 'rotate(180deg)';
            }
        });

        // Fecha ao clicar fora — usa setTimeout para deixar o clique no botão processar primeiro
        document.addEventListener('click', function (e) {
            if (!dropdownToggle.contains(e.target) && !dropdownMenu.contains(e.target)) {
                dropdownMenu.classList.remove('active');
                if (dropdownArrow) dropdownArrow.style.transform = 'rotate(0deg)';
            }
            if (navbarMenu && !menuToggle.contains(e.target)) {
                navbarMenu.classList.remove('active');
            }
        });
    }
});