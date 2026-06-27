const form = document.querySelector("[data-symptom-form]");
const searchInputs = Array.from(document.querySelectorAll("[data-symptom-search]"));
const symptomCards = Array.from(document.querySelectorAll("[data-symptom-card]"));
const categoryButtons = Array.from(document.querySelectorAll("[data-category-button]"));
const selectedList = document.querySelector("[data-selected-list]");
const selectedCount = document.querySelector("[data-selected-count]");
let activeCategory = "general";

function updateSelectedView() {
    const selectedInputs = symptomCards
        .map((card) => card.querySelector("input"))
        .filter((input) => input.checked);

    symptomCards.forEach((card) => {
        const input = card.querySelector("input");
        const icon = card.querySelector(".material-symbols-outlined");
        const selected = input.checked;

        card.classList.toggle("border-primary", selected);
        card.classList.toggle("bg-secondary-container", selected);
        card.classList.toggle("shadow-md", selected);

        if (icon) {
            icon.dataset.icon = selected ? "check_circle" : "add_circle";
            icon.classList.toggle("text-primary", selected);
            icon.classList.toggle("text-outline-variant", !selected);
        }
    });

    selectedCount.textContent = selectedInputs.length;
    selectedList.innerHTML = "";

    if (selectedInputs.length === 0) {
        const emptyState = document.createElement("div");
        emptyState.className = "flex-1 flex flex-col items-center justify-center text-center py-xl";
        emptyState.innerHTML = `
            <span class="material-symbols-outlined text-outline-variant text-[48px] mb-md" data-icon="clinical_notes" aria-hidden="true"></span>
            <p class="font-body-md text-on-surface-variant">No symptoms selected yet. Start adding symptoms from the list.</p>
        `;
        selectedList.appendChild(emptyState);
        return;
    }

    selectedInputs.forEach((input) => {
        const chip = document.createElement("div");
        chip.className = "flex items-center justify-between p-sm bg-surface-bright border border-outline rounded-lg";
        chip.innerHTML = `
            <span class="font-body-md text-on-surface">${input.dataset.label}</span>
            <button type="button" class="material-symbols-outlined text-on-surface-variant hover:text-error transition-colors" data-icon="close" aria-label="close"></button>
        `;
        chip.querySelector("button").addEventListener("click", () => {
            input.checked = false;
            updateSelectedView();
        });
        selectedList.appendChild(chip);
    });
}

function setCategoryButtonState() {
    categoryButtons.forEach((button) => {
        const selected = button.dataset.categoryFilter === activeCategory;

        button.classList.toggle("border-primary", selected);
        button.classList.toggle("bg-secondary-container", selected);
        button.classList.toggle("text-primary", selected);
        button.classList.toggle("border-outline-variant", !selected);
        button.classList.toggle("text-on-surface-variant", !selected);
    });
}

function getSearchTerm() {
    const searchInput = searchInputs.find((input) => input.value.trim().length > 0);
    return searchInput ? searchInput.value.trim().toLowerCase() : "";
}

function filterSymptoms() {
    const term = getSearchTerm();

    symptomCards.forEach((card) => {
        const label = card.dataset.label;
        const categories = card.dataset.categories || "";
        const matchesSearch = term.length === 0 || label.includes(term);
        const matchesCategory = activeCategory === "general" || categories.split(" ").includes(activeCategory);

        card.classList.toggle("hidden-important", !matchesSearch || !matchesCategory);
    });
}

if (form) {
    symptomCards.forEach((card) => {
        card.querySelector("input").addEventListener("change", updateSelectedView);
    });

    searchInputs.forEach((input) => {
        input.addEventListener("input", (event) => {
            searchInputs.forEach((searchInput) => {
                if (searchInput !== event.target) {
                    searchInput.value = event.target.value;
                }
            });

            filterSymptoms();
        });
    });

    categoryButtons.forEach((button) => {
        button.addEventListener("click", () => {
            activeCategory = button.dataset.categoryFilter;
            setCategoryButtonState();
            filterSymptoms();
        });
    });

    updateSelectedView();
    setCategoryButtonState();
    filterSymptoms();
}
