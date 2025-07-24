let x = document.querySelector(".navbar-logo");
let links = document.querySelectorAll(".nav-link");
let toggler = document.querySelector("#toggler-btn");
let service_card_img = document.querySelectorAll(".service_card_img");

x.classList.add("highlight-title");

links.forEach(link => {
    link.classList.add("custom-homepage-buttons");
});

toggler.classList.add("toggler-shadow");

service_card_img.forEach(imgs => {
    imgs.classList.add("service-card-image")
});

var map = L.map('map').setView([12.820834, 80.039410], 13);


  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '© OpenStreetMap contributors'
  }).addTo(map);

  var marker = L.marker([12.820834, 80.039410]).addTo(map);
  marker.bindPopup("<b>Welcome!</b><br>This is your location.").openPopup();