const resultPanel = document.querySelector("[data-confidence]");
const fills = Array.from(document.querySelectorAll("[data-confidence-fill]"));
const note = document.querySelector("[data-confidence-note]");

if (resultPanel && fills.length > 0) {
    const confidence = Number(resultPanel.dataset.confidence || 0);

    fills.forEach((fill) => {
        fill.style.width = `${confidence}%`;
    });

    if (note) {
        if (confidence >= 80) {
            note.textContent = "The selected symptoms have a strong match in the project dataset.";
        } else if (confidence >= 55) {
            note.textContent = "The selected symptoms have a moderate match in the project dataset.";
        } else {
            note.textContent = "The selected symptoms have a limited match in the project dataset.";
        }
    }
}
