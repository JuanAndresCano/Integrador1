// Añadir al archivo deliverablesJs.js
document.addEventListener('DOMContentLoaded', function() {
    // Mejorar la accesibilidad del checkbox
    const checkboxes = document.querySelectorAll('.custom-checkbox');
    
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('keypress', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                const input = this.querySelector('input[type="checkbox"]');
                input.checked = !input.checked;
            }
        });
        
        // Hacer el div focuseable
        checkbox.setAttribute('tabindex', '0');
    });
});