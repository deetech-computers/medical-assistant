const menuToggle = document.querySelector("[data-menu-toggle]");
const sidebar = document.querySelector("[data-sidebar]");
const backdrop = document.querySelector("[data-menu-backdrop]");
const navLinks = Array.from(document.querySelectorAll("[data-nav-link]"));
const themeToggle = document.querySelector("[data-theme-toggle]");
const themeLabel = document.querySelector("[data-theme-label]");
const printButtons = Array.from(document.querySelectorAll("[data-print-result]"));

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

function getTheme() {
    return document.documentElement.dataset.theme || "light";
}

function setTheme(theme) {
    document.documentElement.dataset.theme = theme;
    localStorage.setItem("medscope-theme", theme);

    if (themeToggle) {
        const dark = theme === "dark";
        themeToggle.querySelector(".material-symbols-outlined").dataset.icon = dark ? "light_mode" : "dark_mode";
        themeToggle.setAttribute("aria-label", dark ? "Switch to light mode" : "Switch to dark mode");
    }

    if (themeLabel) {
        themeLabel.textContent = theme === "dark" ? "Light mode" : "Dark mode";
    }
}

if (themeToggle) {
    setTheme(getTheme());
    themeToggle.addEventListener("click", () => {
        setTheme(getTheme() === "dark" ? "light" : "dark");
    });
}

document.addEventListener("submit", (event) => {
    const button = event.target.querySelector("button[type='submit']");

    if (!button || button.dataset.loading === "true") {
        return;
    }

    button.dataset.loading = "true";
    button.dataset.originalText = button.textContent.trim();
    button.textContent = "Processing";
});

printButtons.forEach((button) => {
    button.addEventListener("click", () => window.print());
});
