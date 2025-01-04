document.getElementById("subscribeButton").addEventListener("click", function (e) {
    e.preventDefault(); // Prevent default behavior of the button

    const url = this.dataset.url; // Get the URL from the data-url attribute
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content'); // Fetch CSRF token

    // Send POST request to the subscribe endpoint
    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken, // Include CSRF token in the header
        },
    })
        .then((response) => {
            if (!response.ok) {
                throw new Error("Request failed");
            }
            return response.json();
        })
        .then((data) => {
                // Inject the Bootstrap alert into the subscriptionAlert div
                document.getElementById('subscriptionAlert').innerHTML = `
                <div class="alert alert-success alert-dismissible fade show" role="alert">
                    You have successfully subscribed to the weekly newsletter!
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>
            `;
             // Reload the page to reflect changes
            // location.reload();
        })
        .catch((error) => {
            console.error("There was an error:", error);
            // Handle error message with Bootstrap alert
            document.getElementById('subscriptionAlert').innerHTML = `
            <div class="alert alert-danger alert-dismissible fade show" role="alert">
            There was an error. Please try again.
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
            `;
        });
});
