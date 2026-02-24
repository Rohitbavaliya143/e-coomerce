(function () {
    'use strict';

    // 1. Payment Method Interaction
    const paymentOptions = document.querySelectorAll('.payment-option');
    const radioInputs = document.querySelectorAll('.payment-option input[type="radio"]');

    function updatePaymentUI() {
        paymentOptions.forEach(option => {
            const radio = option.querySelector('input[type="radio"]');
            if (radio.checked) {
                option.classList.add('active');
            } else {
                option.classList.remove('active');
            }
        });
    }

    // Initialize on load
    updatePaymentUI();

    // Listen for changes
    radioInputs.forEach(input => {
        input.addEventListener('change', updatePaymentUI);
    });

    // 2. Bootstrap Validation
    const forms = document.querySelectorAll('.needs-validation');

    Array.prototype.slice.call(forms)
        .forEach(function (form) {
            form.addEventListener('submit', function (event) {
                if (!form.checkValidity()) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');
            }, false);
        });
})();