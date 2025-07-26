// script.js — можно использовать для будущей интерактивности
document.addEventListener('DOMContentLoaded', function () {
    console.log('Бар "Эклектика" — сайт загружен');

    // Пример: анимация появления при скролле
    const fadeElements = document.querySelectorAll('.beer-card, .about-text, .about-image');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = 1;
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, { threshold: 0.1 });

    fadeElements.forEach(el => {
        el.style.opacity = 0;
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
});