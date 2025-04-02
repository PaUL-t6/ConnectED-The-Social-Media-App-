// JavaScript to handle skill selection
const skillButtons = document.querySelectorAll('.skill-btn');

skillButtons.forEach(button => {
    button.addEventListener('click', () => {
        const checkbox = button.querySelector('input[type="checkbox"]');
        checkbox.checked = !checkbox.checked; // Toggle the checkbox state
        button.classList.toggle('selected'); // Toggle the 'selected' class
    });
});