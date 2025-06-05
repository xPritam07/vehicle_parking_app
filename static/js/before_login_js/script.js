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