// JavaScript for Typing and Wiping Effect
const textElement = document.getElementById("typewriter-text");
const textToType = "Welcome to Om Yeole's Blogs"; // Text to type
const typingSpeed = 100; // Speed of typing (in ms)
const wipingSpeed = 50; // Speed of wiping (in ms)
const delayAfterTyping = 1500; // Delay after typing completes (in ms)

let charIndex = 0;
let isTyping = true; // Flag to determine whether typing or wiping

function typeWriterEffect() {
    if (isTyping) {
        if (charIndex < textToType.length) {
            // Typing the text character by character
            textElement.textContent += textToType.charAt(charIndex);
            charIndex++;
            setTimeout(typeWriterEffect, typingSpeed);
        } else {
            // Typing finished, delay before wiping starts
            isTyping = false;
            setTimeout(typeWriterEffect, delayAfterTyping);
        }
    } else {
        if (charIndex > 0) {
            // Wiping the text character by character
            textElement.textContent = textToType.substring(0, charIndex - 1);
            charIndex--;
            setTimeout(typeWriterEffect, wipingSpeed);
        } else {
            // Wiping finished, start typing again
            isTyping = true;
            setTimeout(typeWriterEffect, typingSpeed);
        }
    }
}

// Start the typing effect when the page loads
document.addEventListener("DOMContentLoaded", () => {
    typeWriterEffect();
});