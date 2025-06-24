const menuIcon = document.getElementById('menu-icon');
const dropdown = document.getElementById('custom-menu');

menuIcon.addEventListener('click', () => {
    dropdown.classList.toggle('show');
});
