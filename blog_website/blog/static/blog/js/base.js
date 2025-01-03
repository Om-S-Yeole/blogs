// Hide the loading spinner once the page is fully loaded
window.addEventListener('load', function() {
  var spinner = document.getElementById('loadingSpinner');
    spinner.style.display = 'none'; // Hide the spinner after the page loads
});

// Dark Mode Toggle with Theme Persistence
const modeToggle = document.getElementById('modeToggle');
const body = document.body;

// Function to apply the saved theme or default to dark mode
function applySavedTheme() {
  const savedTheme = localStorage.getItem('theme');
  console.log('Saved Theme:', savedTheme); // Debugging: Check saved theme
  if (savedTheme === 'light-mode') {
    body.classList.add('light-mode');
    body.classList.remove('dark-mode');
    modeToggle.classList.remove('fa-moon'); // Change to sun icon
    modeToggle.classList.add('fa-sun');
  } else {
    localStorage.setItem('theme', 'dark-mode');
    body.classList.add('dark-mode'); // Default to dark mode
    body.classList.remove('light-mode');
    modeToggle.classList.remove('fa-sun'); // Change to moon icon
    modeToggle.classList.add('fa-moon');
  }
}

// Apply the saved theme on page load
applySavedTheme();

modeToggle.addEventListener('click', () => {
  if (body.classList.contains('dark-mode')) {
    // Switch to Light Mode
    body.classList.remove('dark-mode');
    body.classList.add('light-mode');
    modeToggle.classList.remove('fa-moon'); // Change to sun icon
    modeToggle.classList.add('fa-sun');
    localStorage.setItem('theme', 'light-mode'); // Save preference
  } else {
    // Switch to Dark Mode
    body.classList.remove('light-mode');
    body.classList.add('dark-mode');
    modeToggle.classList.remove('fa-sun'); // Change to moon icon
    modeToggle.classList.add('fa-moon');
    localStorage.setItem('theme', 'dark-mode'); // Save preference
  }
});

// Highlight Active Navbar Link
const navLinks = document.querySelectorAll('.nav-link');

navLinks.forEach((link) => {
  link.addEventListener('click', () => {
    navLinks.forEach((link) => link.classList.remove('active')); // Remove 'active' from all links
    link.classList.add('active'); // Add 'active' to the clicked link
  });
});

// Back to Top Button Visibility
window.addEventListener('scroll', () => {
  const backToTopButton = document.getElementById('backToTop');
  if (document.body.scrollTop > 200 || document.documentElement.scrollTop > 200) {
    backToTopButton.style.display = 'block';
  } else {
    backToTopButton.style.display = 'none';
  }
});

document.getElementById('backToTop').addEventListener('click', () => {
  window.scrollTo({ top: 0, behavior: 'smooth' });
});

// Hide Loading Spinner on Page Load
window.addEventListener('load', () => {
  document.getElementById('loadingSpinner').style.display = 'none';
});
