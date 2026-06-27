const globalSearchInputs = Array.from(document.querySelectorAll("[data-global-search]"));
const searchableItems = Array.from(document.querySelectorAll("[data-search-item]"));

function filterSearchableItems(event) {
    const term = event.target.value.trim().toLowerCase();

    globalSearchInputs.forEach((input) => {
        if (input !== event.target) {
            input.value = event.target.value;
        }
    });

    searchableItems.forEach((item) => {
        const text = item.textContent.toLowerCase();
        item.classList.toggle("hidden-important", term.length > 0 && !text.includes(term));
    });
}

globalSearchInputs.forEach((input) => {
    input.addEventListener("input", filterSearchableItems);
});
