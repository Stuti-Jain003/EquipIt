document.addEventListener('DOMContentLoaded', function () {
    // Get the search button and input element
    const searchButton = document.getElementById('searchButton');
    const searchInput = document.getElementById('searchInput');

    // Add a click event listener to the search button
    searchButton.addEventListener('click', function () {
        // Get the search term from the input field
        const searchTerm = searchInput.value.trim();

        // Redirect to the search results page with the search term as a query parameter
        window.location.href = `/search?term=${encodeURIComponent(searchTerm)}`;
    });
});
