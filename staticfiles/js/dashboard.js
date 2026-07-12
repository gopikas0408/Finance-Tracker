// ==========================================
// DASHBOARD CHARTS
// ==========================================

document.addEventListener("DOMContentLoaded", function () {

    // ==========================================
    // CHECK CHART.JS
    // ==========================================

    if (typeof Chart === "undefined") {

        console.error("Chart.js is not loaded.");

        return;

    }

    // ==========================================
// INCOME VS EXPENSE CHART
// ==========================================

const incomeCanvas = document.getElementById("incomeExpenseChart");

if (
    incomeCanvas &&
    typeof incomeLabels !== "undefined" &&
    typeof incomeValues !== "undefined" &&
    typeof expenseValues !== "undefined"
) {

    new Chart(incomeCanvas, {

        type: "line",

        data: {

            labels: incomeLabels,

            datasets: [

                {

                    label: "Income",

                    data: incomeValues,

                    borderColor: "#22C55E",

                    backgroundColor: "rgba(34,197,94,0.15)",

                    fill: true,

                    tension: 0.4,

                    pointRadius: 5,

                    pointHoverRadius: 7,

                    pointBackgroundColor: "#22C55E",

                },

                {

                    label: "Expense",

                    data: expenseValues,

                    borderColor: "#EF4444",

                    backgroundColor: "rgba(239,68,68,0.15)",

                    fill: true,

                    tension: 0.4,

                    pointRadius: 5,

                    pointHoverRadius: 7,

                    pointBackgroundColor: "#EF4444",

                }

            ]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            interaction: {

                mode: "index",

                intersect: false,

            },

            plugins: {

                legend: {

                    position: "top",

                    labels: {

                        usePointStyle: true,

                        pointStyle: "circle",

                    }

                }

            },

            scales: {

                x: {

                    grid: {

                        display: false,

                    }

                },

                y: {

                    beginAtZero: true,

                    ticks: {

                        callback: function(value){

                            return "₹ " + value;

                        }

                    }

                }

            }

        }

    });

}

    // ==========================================
    // EXPENSE CATEGORY CHART
    // ==========================================

    const expenseCanvas = document.getElementById("expenseChart");

    if (
        expenseCanvas &&
        typeof expenseCategoryLabels !== "undefined" &&
        typeof expenseCategoryValues !== "undefined"
    ) {

        new Chart(expenseCanvas, {

            type: "doughnut",

            data: {

                labels: expenseCategoryLabels,

                datasets: [

                    {

                        data: expenseCategoryValues,

                        backgroundColor: [

                            "#22C55E",

                            "#3B82F6",

                            "#F59E0B",

                            "#EF4444",

                            "#8B5CF6",

                            "#14B8A6",

                            "#EC4899",

                            "#64748B",

                            "#06B6D4",

                            "#F97316",

                        ],

                        borderWidth: 0,

                        hoverOffset: 8,

                    }

                ]

            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                cutout: "65%",

                plugins: {

                    legend: {

                        position: "bottom",

                        labels: {

                            usePointStyle: true,

                            pointStyle: "circle",

                            padding: 20,

                        }

                    }

                }

            }

        });

    }

    // ==========================================
    // GLOBAL SEARCH
    // ==========================================

    const searchInput = document.getElementById("globalSearch");

    const searchResults = document.getElementById("searchResults");

    if (searchInput) {

        searchInput.addEventListener("keyup", function () {

            const keyword = this.value.trim();

            if (keyword.length < 2) {

                searchResults.innerHTML = "";

                searchResults.style.display = "none";

                return;

            }

            fetch(`/dashboard/search/?q=${encodeURIComponent(keyword)}`)

                .then(response => response.json())

                .then(data => {

                    let html = "";

                    if (data.length === 0) {

                        html = `
                            <div class="search-item">
                                No Results Found
                            </div>
                        `;

                    } else {

                        data.forEach(item => {

                            html += `

                            <a href="${item.url}" class="search-item">

                                <h6>${item.title}</h6>

                                <p>${item.subtitle}</p>

                            </a>

                            `;

                        });

                    }

                    searchResults.innerHTML = html;

                    searchResults.style.display = "block";

                })

                .catch(error => {

                    console.error(error);

                });

        });

    }

});

// ==========================================
// DASHBOARD FILTER
// ==========================================

const chartFilter = document.getElementById("chartFilter");

if(chartFilter){

    chartFilter.addEventListener("change",function(){

        window.location.href =
        "?filter=" + this.value;

    });

}