// Aguarda o HTML carregar completamente
document.addEventListener('DOMContentLoaded', function () {

    // ── Menu mobile ──
    const menuToggle = document.getElementById('menuToggle');
    const navbarMenu = document.getElementById('navbarMenu');
    
    // Abre ou fecha o menu hambúrguer no mobile
    if (menuToggle && navbarMenu) {
        menuToggle.addEventListener('click', function (e) {
            e.stopPropagation(); // Impede o clique de propagar para o document
            navbarMenu.classList.toggle('active');
        });
    }

    // ── Dropdown do usuário ──
    const dropdownToggle = document.getElementById('userDropdownToggle');
    const dropdownMenu   = document.getElementById('userDropdownMenu');
    const dropdownArrow  = document.getElementById('dropdownArrow');

    // Gerencia a abertura do menu de perfil e rotaciona a seta indicadora
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

        // Fecha o dropdown do usuário e o menu mobile automaticamente ao clicar fora deles
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