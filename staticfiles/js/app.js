document.addEventListener('DOMContentLoaded', function () {
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function (alert) {
        const closeButton = alert.querySelector('.btn-close');
        if (closeButton) {
            closeButton.addEventListener('click', function () {
                alert.remove();
            });
        }
    });

    const navbarToggle = document.querySelector('.navbar-toggler');
    const navCollapse = document.querySelector('.navbar-collapse');
    if (navbarToggle && navCollapse) {
        navbarToggle.addEventListener('click', function () {
            navCollapse.classList.toggle('show');
        });
    }

    const cards = document.querySelectorAll('.event-card');
    cards.forEach(function (card, index) {
        card.style.animationDelay = (index * 80) + 'ms';
        card.classList.add('reveal-card');
    });

    const searchInput = document.querySelector('#event-search');
    if (searchInput) {
        const filterCards = function () {
            const query = searchInput.value.toLowerCase().trim();
            cards.forEach(function (card) {
                const text = card.textContent.toLowerCase();
                const visible = !query || text.includes(query);
                card.style.display = visible ? '' : 'none';
            });
        };

        searchInput.addEventListener('input', filterCards);
    }
});
