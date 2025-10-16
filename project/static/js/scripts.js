// ===========================
// Документ готовий
// ===========================

document.addEventListener('DOMContentLoaded', function() {
    
    // Анімація навичок при завантаженні сторінки
    animateSkills();
    
    // Валідація форми
    setupFormValidation();
    
    // Smooth scroll для навігації
    setupSmoothScroll();
    
    // Автоматичне закриття alerts
    autoCloseAlerts();
    
});

// ===========================
// Анімація прогрес-барів навичок
// ===========================

function animateSkills() {
    const skillBars = document.querySelectorAll('.skill-progress');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const bar = entry.target;
                const width = bar.style.width;
                bar.style.width = '0';
                
                setTimeout(() => {
                    bar.style.width = width;
                }, 100);
                
                observer.unobserve(bar);
            }
        });
    }, { threshold: 0.5 });
    
    skillBars.forEach(bar => observer.observe(bar));
}

// ===========================
// Валідація форми контактів
// ===========================

function setupFormValidation() {
    const form = document.getElementById('contactForm');
    
    if (form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            
            form.classList.add('was-validated');
        });
        
        // Валідація email в реальному часі
        const emailInput = document.getElementById('email');
        if (emailInput) {
            emailInput.addEventListener('blur', function() {
                validateEmail(this);
            });
        }
    }
}

function validateEmail(input) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    
    if (input.value && !emailRegex.test(input.value)) {
        input.setCustomValidity('Будь ласка, введіть коректну email адресу');
    } else {
        input.setCustomValidity('');
    }
}

// ===========================
// Smooth scroll для посилань
// ===========================

function setupSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href !== '#' && href !== '') {
                const target = document.querySelector(href);
                if (target) {
                    e.preventDefault();
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });
}

// ===========================
// Автоматичне закриття alerts
// ===========================

function autoCloseAlerts() {
    const alerts = document.querySelectorAll('.alert');
    
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000); // Закриття через 5 секунд
    });
}

// ===========================
// Показ/приховування кнопки "Наверх"
// ===========================

window.addEventListener('scroll', function() {
    const scrollTop = document.getElementById('scrollTop');
    
    if (scrollTop) {
        if (window.pageYOffset > 300) {
            scrollTop.style.display = 'block';
        } else {
            scrollTop.style.display = 'none';
        }
    }
});

// ===========================
// Лічильник символів для textarea
// ===========================

const messageTextarea = document.getElementById('message');
if (messageTextarea) {
    const maxLength = 500;
    
    // Створюємо елемент лічильника
    const counter = document.createElement('small');
    counter.className = 'text-muted';
    counter.textContent = `0 / ${maxLength} символів`;
    messageTextarea.parentNode.appendChild(counter);
    
    messageTextarea.addEventListener('input', function() {
        const length = this.value.length;
        counter.textContent = `${length} / ${maxLength} символів`;
        
        if (length > maxLength) {
            counter.classList.add('text-danger');
            counter.classList.remove('text-muted');
        } else {
            counter.classList.add('text-muted');
            counter.classList.remove('text-danger');
        }
    });
}

// ===========================
// Анімація появи карток
// ===========================

const cards = document.querySelectorAll('.card');
const cardObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry, index) => {
        if (entry.isIntersecting) {
            setTimeout(() => {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }, index * 100);
            cardObserver.unobserve(entry.target);
        }
    });
}, { threshold: 0.1 });

cards.forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(20px)';
    card.style.transition = 'all 0.6s ease';
    cardObserver.observe(card);
});

// ===========================
// Tooltip ініціалізація для Bootstrap
// ===========================

const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
