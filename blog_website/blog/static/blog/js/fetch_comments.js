let currentPage = 2; // Start with page 2 because page 1 is preloaded in the template
let hasMoreComments = true; // Whether there are more comments to load
const commentsList = document.getElementById('comments-list');
const loadMoreButton = document.getElementById('load-more-btn');
const spinner = document.getElementById('loading-spinner');

// Function to load comments
async function loadComments() {
    if (!hasMoreComments) return; // Stop if no more comments

    spinner.style.display = 'block'; // Show loading spinner
    loadMoreButton.disabled = true; // Disable button while loading

    try {
        const response = await fetch(`/posts/${postSlug}/comments/?page=${currentPage}`);
        const data = await response.json();

        // Append comments to the list
        data.comments.forEach(comment => {
            const commentItem = document.createElement('li');
            commentItem.className = 'comment shadow-sm p-3 mb-3';
            commentItem.innerHTML = `
                <strong>${comment.username}</strong>
                <small>${comment.created_at}</small>
                <p>${comment.content}</p>
            `;
            commentsList.appendChild(commentItem);
        });

        // Update flags
        hasMoreComments = data.has_next;
        currentPage++;

        // Hide the "Load More" button if there are no more comments
        if (!hasMoreComments) {
            loadMoreButton.style.display = 'none';
        }
    } catch (error) {
        console.error('Error loading comments:', error);
    } finally {
        spinner.style.display = 'none'; // Hide loading spinner
        loadMoreButton.disabled = false; // Re-enable button
    }
}

// Event Listener for Load More button
if (loadMoreButton) {
    loadMoreButton.addEventListener('click', loadComments);
}
