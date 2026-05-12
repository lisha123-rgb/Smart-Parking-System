// Login/Signup Toggle
function showSignIn() {
    document.getElementById('signin-form').style.display = 'block';
    document.getElementById('signup-form').style.display = 'none';
    document.querySelectorAll('.toggle-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.toggle-btn')[0].classList.add('active');
}

function showSignUp() {
    document.getElementById('signin-form').style.display = 'none';
    document.getElementById('signup-form').style.display = 'block';
    document.querySelectorAll('.toggle-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.toggle-btn')[1].classList.add('active');
}

// Wallet Amount Validation
function validateAmount() {
    const amountInput = document.getElementById('amount');
    const amount = parseFloat(amountInput.value);
    const errorDiv = document.getElementById('amountError');
    
    if (amount < 50) {
        errorDiv.textContent = 'Minimum amount is ₹50';
        amountInput.focus();
        return false;
    }
    
    if (amount > 10000) {
        errorDiv.textContent = 'Maximum amount is ₹10,000';
        amountInput.focus();
        return false;
    }
    
    errorDiv.textContent = '';
    return true;
}

function setAmount(amount) {
    document.getElementById('amount').value = amount;
    document.getElementById('amountError').textContent = '';
}

// Booking Slot Selection
function selectSlot(slot) {
    document.getElementById('selectedSlot').textContent = slot;
    document.getElementById('slotInput').value = slot;
}

// Form Validation Enhancements
document.addEventListener('DOMContentLoaded', function() {
    // Mobile number validation
    const mobileInputs = document.querySelectorAll('input[type="tel"]');
    mobileInputs.forEach(input => {
        input.addEventListener('input', function(e) {
            e.target.value = e.target.value.replace(/[^0-9]/g, '').slice(0, 10);
        });
    });
    
    // Number plate validation (only for booking form)
    const numberplateInputs = document.querySelectorAll('input[name="numberplate"]');
    numberplateInputs.forEach(input => {
        input.addEventListener('input', function(e) {
            e.target.value = e.target.value.toUpperCase().replace(/[^A-Z0-9]/g, '');
        });
    });
    
    // Auto-format amount input
    const amountInput = document.getElementById('amount');
    if (amountInput) {
        amountInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/[^0-9]/g, '');
            if (value) {
                value = parseInt(value);
                if (value > 10000) value = 10000;
                e.target.value = value;
            }
        });
    }
});

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Auto-hide alerts after 5 seconds
setTimeout(() => {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        const bsAlert = new bootstrap.Alert(alert);
        bsAlert.close();
    });
}, 5000);