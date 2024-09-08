// main.js
const sidebar = document.querySelector('.sidebar');
const menuToggle = document.querySelector('#menu-toggle');

menuToggle.addEventListener('click', () => {
    sidebar.classList.toggle('active');
});
