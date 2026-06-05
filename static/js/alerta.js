document.addEventListener('DOMContentLoaded', function () {
    // 1. Descarte automatizado dos alertas Django
    document.querySelectorAll('.django-messages .alert').forEach(function (alert) {
        setTimeout(function () {
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-8px)';
            setTimeout(() => alert.remove(), 300);
        }, 5000);
    });
});