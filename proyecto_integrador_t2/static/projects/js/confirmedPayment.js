document.addEventListener('mousemove', function(e) {
    const container = document.querySelector('.invoice-container');
    const rect = container.getBoundingClientRect();
    const centerX = rect.left + rect.width / 2;
    const centerY = rect.top + rect.height / 2;
    
    const deltaX = (e.clientX - centerX) / 25;
    const deltaY = (e.clientY - centerY) / 25;

    container.style.transform = `
        rotateY(${-deltaX}deg) 
        rotateX(${deltaY}deg) 
        translateZ(0)
    `;

    const shadowX = -deltaX * 2;
    const shadowY = -deltaY * 2;
    container.style.boxShadow = `
        ${shadowX}px ${shadowY}px 40px rgba(0, 0, 0, 0.1),
        0 0 100px rgba(0, 0, 0, 0.05),
        inset 0 0 0 1px rgba(255, 255, 255, 0.8)
    `;
});

document.addEventListener('mouseleave', function() {
    const container = document.querySelector('.invoice-container');
    container.style.transform = 'rotateY(0) rotateX(0) translateZ(0)';
    container.style.boxShadow = `
        0 20px 40px rgba(0, 0, 0, 0.1),
        0 0 100px rgba(0, 0, 0, 0.05),
        inset 0 0 0 1px rgba(255, 255, 255, 0.8)
    `;
});

document.querySelectorAll('.detail-item').forEach((item, index) => {
    item.style.animationDelay = `${0.6 + (index * 0.1)}s`;
});

function formatCurrency(elementId) {
    const element = document.getElementById(elementId);
    const value = parseFloat(element.textContent.replace('$', '').replace(',', '.'));
    element.textContent = `$${value.toLocaleString('es-ES', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
}
