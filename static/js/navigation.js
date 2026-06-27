const menuToggle = document.querySelector("[data-menu-toggle]");
const sidebar = document.querySelector("[data-sidebar]");
const backdrop = document.querySelector("[data-menu-backdrop]");
const navLinks = Array.from(document.querySelectorAll("[data-nav-link]"));

function setMenu(open) {
    document.body.classList.toggle("menu-open", open);
    if (menuToggle) {
        menuToggle.setAttribute("aria-expanded", String(open));
    }
}

if (menuToggle && sidebar && backdrop) {
    menuToggle.addEventListener("click", () => {
        setMenu(!document.body.classList.contains("menu-open"));
    });

    backdrop.addEventListener("click", () => setMenu(false));
    navLinks.forEach((link) => {
        link.addEventListener("click", () => setMenu(false));
    });

    window.addEventListener("keydown", (event) => {
        if (event.key === "Escape") {
            setMenu(false);
        }
    });
}
