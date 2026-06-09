// Aguarda o HTML carregar completamente
document.addEventListener('DOMContentLoaded', function () {
    
    // Seleciona todas as mensagens de alerta do Django
    document.querySelectorAll('.django-messages .alert').forEach(function (alert) {
        
        // Aguarda 5 segundos antes de sumir com o alerta
        setTimeout(function () {
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-8px)';
            
            // Aguarda 300ms da animação e remove o elemento do HTML
            setTimeout(() => alert.remove(), 300);
        }, 5000);
    });
});