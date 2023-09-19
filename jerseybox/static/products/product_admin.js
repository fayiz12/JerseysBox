document.addEventListener("DOMContentLoaded", function () {
    const categoryField = document.getElementById("id_category");
    const clubIdField = document.getElementById("id_club_id");
    const countryIdField = document.getElementById("id_country_id");

    // Function to toggle field visibility
    function toggleFieldVisibility() {
        const selectedCategory = categoryField.value;
        if (selectedCategory === "club") {
            clubIdField.parentElement.parentElement.style.display = "";
            countryIdField.parentElement.parentElement.style.display = "none";
        } else if (selectedCategory === "country") {
            clubIdField.parentElement.parentElement.style.display = "none";
            countryIdField.parentElement.parentElement.style.display = "";
        } else {
            clubIdField.parentElement.parentElement.style.display = "none";
            countryIdField.parentElement.parentElement.style.display = "none";
        }
    }

    // Initial visibility setup
    toggleFieldVisibility();

    // Add an event listener to update visibility on category field change
    categoryField.addEventListener("change", toggleFieldVisibility);
});

