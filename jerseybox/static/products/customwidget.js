document.addEventListener("DOMContentLoaded", function () {
    const searchWidgets = document.querySelectorAll(".search-widget");

    searchWidgets.forEach(function (widget) {
        const input = widget.querySelector(".search-widget-input");
        const button = widget.querySelector(".search-widget-button");

        button.addEventListener("click", function () {
            const searchTerm = input.value.trim();
            if (searchTerm) {
                // Perform your custom search logic here
                alert("Searching for: " + searchTerm);
            } else {
                alert("Please enter a search term.");
            }
        });
    });
});