function toggleContacts() {
    const contactDetails = document.getElementById('contactDetails');
    const chevron = document.getElementById('chevron');

    if (contactDetails.classList.contains('show')) {
        contactDetails.classList.remove('show');
        chevron.style.transform = 'rotate(0deg)';
    } else {
        contactDetails.classList.add('show');
        chevron.style.transform = 'rotate(180deg)';
    }
}

function setActive(element) {
    document.querySelectorAll('.review_category p').forEach(p => p.classList.remove('active'));
    element.classList.add('active');
}
