let x = document.querySelector(".navbar-logo");
let links = document.querySelectorAll(".nav-link");
let toggler = document.querySelector("#toggler-btn");

x.classList.add("highlight-title");

links.forEach(link => {
    link.classList.add("custom-homepage-buttons");
});

toggler.classList.add("toggler-shadow");