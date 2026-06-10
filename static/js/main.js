// Hamburger menu
const hamburger = document.getElementById('hamburger');
const navLinks = document.querySelector('.nav-links');

if (hamburger) {
    hamburger.addEventListener('click', () => {
        navLinks.classList.toggle('open');
    });
}

// Auto-update cart badge via API
function updateCartBadge() {
    fetch('/api/cart_count')
        .then(res => res.json())
        .then(data => {
            const badge = document.getElementById('cart-badge');
            if (badge) badge.textContent = data.count;
        })
        .catch(() => {});
}

// Notification toast
function showToast(msg, type = 'success') {
    const toast = document.createElement('div');
    toast.style.cssText = `
        position: fixed; bottom: 30px; right: 30px;
        background: ${type === 'success' ? '#22c55e' : '#ef4444'};
        color: white; padding: 15px 25px; border-radius: 10px;
        font-weight: 600; box-shadow: 0 5px 20px rgba(0,0,0,0.2);
        z-index: 9999; animation: slideIn 0.3s ease;
        font-family: 'Montserrat', sans-serif; font-size: 0.95rem;
    `;
    toast.textContent = msg;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 3000);
}

// Smooth scroll
document.querySelectorAll('a[href^="#"]').forEach(link => {
    link.addEventListener('click', e => {
        const target = document.querySelector(link.getAttribute('href'));
        if (target) {
            e.preventDefault();
            target.scrollIntoView({ behavior: 'smooth' });
        }
    });
});

// Set min date for booking
const dateInputs = document.querySelectorAll('input[type="date"]');
dateInputs.forEach(input => {
    const today = new Date().toISOString().split('T')[0];
    input.min = today;
    if (!input.value) input.value = today;
});
