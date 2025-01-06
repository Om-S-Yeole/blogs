document.getElementById('like-btn').addEventListener('click', async function () {
    console.log("Like button clicked"); // Debugging log

    const likeButton = document.getElementById('like-btn');
    const likeText = document.getElementById('like-text');
    const likeCount = document.getElementById('like-count');

    try {
        const response = await fetch(`/posts/${postSlug}/like/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
            },
        });

        if (response.redirected) {
            console.log("Redirect detected. Redirecting to login page...");
            // Redirect to login page
            window.location.href = response.url.substring(0, response.url.lastIndexOf("like/"));
            return;
        }

        if (response.ok) {
            const data = await response.json();
            console.log("Data received:", data); // Debugging log

            likeText.innerText = data.liked ? 'Unlike' : 'Like';
            likeCount.innerText = data.likes_count;
        } else {
            console.error("Failed to like the post:", response.statusText);
        }
    } catch (error) {
        console.error("Error liking the post:", error);
    }
});
