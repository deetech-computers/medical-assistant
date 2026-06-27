const analyticsDataNode = document.getElementById("admin-chart-data");

function readAnalyticsData() {
    if (!analyticsDataNode) {
        return null;
    }

    try {
        return JSON.parse(analyticsDataNode.textContent || "{}");
    } catch (error) {
        return null;
    }
}

function chartColor(name) {
    const styles = getComputedStyle(document.documentElement);
    return styles.getPropertyValue(name).trim();
}

function labels(items) {
    return items.map((item) => item.label);
}

function values(items) {
    return items.map((item) => item.value);
}

function renderChart(id, type, items, options = {}) {
    const canvas = document.getElementById(id);

    if (!canvas || !window.Chart || !items || items.length === 0) {
        return;
    }

    const primary = chartColor("--primary");
    const primaryContainer = chartColor("--primary-container");
    const secondaryContainer = chartColor("--secondary-container");
    const outline = chartColor("--outline-variant");
    const textColor = chartColor("--on-surface-variant");

    const background = type === "doughnut"
        ? [primary, primaryContainer, secondaryContainer, outline, "#5b6ee1", "#81a4cd", "#99d1c8", "#d0d7f7"]
        : options.background || primaryContainer;

    new Chart(canvas, {
        type,
        data: {
            labels: labels(items),
            datasets: [
                {
                    label: options.label || "Records",
                    data: values(items),
                    borderColor: options.borderColor || primary,
                    backgroundColor: background,
                    borderWidth: 2,
                    tension: 0.35,
                    fill: type === "line",
                },
            ],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: type === "doughnut",
                    labels: {
                        color: textColor,
                        boxWidth: 12,
                    },
                },
            },
            scales: type === "doughnut" ? {} : {
                x: {
                    ticks: { color: textColor, maxRotation: 0 },
                    grid: { color: "transparent" },
                },
                y: {
                    beginAtZero: true,
                    ticks: { color: textColor, precision: 0 },
                    grid: { color: outline },
                },
            },
        },
    });
}

function renderAnalyticsCharts() {
    const analyticsData = readAnalyticsData();

    if (!analyticsData) {
        return;
    }

    renderChart("dailyPredictionChart", "line", analyticsData.daily, {
        label: "Daily predictions",
        background: "rgba(26, 35, 126, 0.12)",
    });
    renderChart("diseaseChart", "doughnut", analyticsData.diseases, {
        label: "Disease records",
    });
    renderChart("weeklyChart", "bar", analyticsData.weekly, {
        label: "Weekly records",
    });
    renderChart("monthlyChart", "bar", analyticsData.monthly, {
        label: "Monthly records",
        background: chartColor("--secondary-container"),
    });
}

window.addEventListener("load", renderAnalyticsCharts);
