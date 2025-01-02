// Dark Mode Toggle
const modeToggle = document.getElementById('modeToggle');
const body = document.body;

modeToggle.addEventListener('click', () => {
  if (body.classList.contains('dark-mode')) {
    // Switch to Light Mode
    body.classList.remove('dark-mode');
    body.classList.add('light-mode');
    modeToggle.classList.remove('fa-moon'); // Change to sun icon
    modeToggle.classList.add('fa-sun');
  } else {
    // Switch to Dark Mode
    body.classList.remove('light-mode');
    body.classList.add('dark-mode');
    modeToggle.classList.remove('fa-sun'); // Change to moon icon
    modeToggle.classList.add('fa-moon');
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

window.addEventListener('scroll', () => {
    const backToTopButton = document.getElementById('backToTop');
    if (document.body.scrollTop > 200 || document.documentElement.scrollTop > 200) {
      backToTopButton.style.display = "block";
    } else {
      backToTopButton.style.display = "none";
    }
  });
  
document.getElementById('backToTop').addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });

window.addEventListener('load', () => {
    document.getElementById('loadingSpinner').style.display = 'none';
  });