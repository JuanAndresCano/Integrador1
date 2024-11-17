document.addEventListener('DOMContentLoaded', function() {
    const paymentMethods = document.querySelectorAll('.payment-method-item');
    const cardForm = document.getElementById('cardForm');
    const paypalForm = document.getElementById('paypalForm');

    paymentMethods.forEach(method => {
        method.addEventListener('click', function() {
            paymentMethods.forEach(m => m.classList.remove('active'));
            this.classList.add('active');

            if (this.dataset.method === 'card') {
                paypalForm.classList.remove('active');
                cardForm.classList.add('active');
            } else {
                cardForm.classList.remove('active');
                paypalForm.classList.add('active');
            }
        });
    });
});