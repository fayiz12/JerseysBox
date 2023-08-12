const imageElement = document.getElementById('changing-image');
const imageUrls = [
    "{% static 'Manchester-United-landingPage.jpg' %}",
    "{% static 'ManchesterCitylanding_page.jpg' %}",
    "{% static 'Manchester-United-landingPage.jpg' %}"
];
let currentIndex = 0;

function changeImage() {
    imageElement.src = imageUrls[currentIndex];
    currentIndex = (currentIndex + 1) % imageUrls.length;
}

// Change image every 3 seconds
setInterval(changeImage, 3000);
