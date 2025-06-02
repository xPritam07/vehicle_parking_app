const sign_in_btn = document.querySelector("#sign-in-btn");
const sign_up_btn = document.querySelector("#sign-up-btn");
const container = document.querySelector(".container");
let x = document.querySelector(".navbar-logo");
let links = document.querySelectorAll(".nav-link");
let toggler = document.querySelector("#toggler-btn");

sign_up_btn.addEventListener("click", () => {
  container.classList.add("sign-up-mode");
});

sign_in_btn.addEventListener("click", () => {
  container.classList.remove("sign-up-mode");
});

x.classList.add("highlight-title");

links.forEach(link => {
    link.classList.add("custom-homepage-buttons");
});

toggler.classList.add("toggler-shadow");
