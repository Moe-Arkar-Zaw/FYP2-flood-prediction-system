document.addEventListener("DOMContentLoaded", async function () {

    const topStreetsList = document.getElementById("topStreetsList");
    const detailedStatus = document.getElementById("detailedStatus");
    const trendChartCanvas = document.getElementById("trendChart");

    let chart = null;
    let streetsData = [];

    // Color palette for chart
    const palette = [
        "#ff4d6d", "#0096c7", "#ffb703", "#8ac926",
        "#6a4c93", "#ef476f", "#219ebc", "#fb8500"
    ];

    function cleanStreetName(name) {
        return name.replace(/_\d+$/, "");
    }

    // 1️⃣ Fetch top flooded streets
    try {
        const resp = await fetch("/api/top-flooded-streets");
        const data = await resp.json();
        streetsData = data.streets || [];

        // Clean names
        streetsData.forEach((s) => {
            s.display_name = cleanStreetName(s.street_name);
        });

        loadTopStreetCards();

        // Fetch each street’s trend data
        await Promise.all(
            streetsData.map(async (s, index) => {
                const trendResp = await fetch(`/api/flood-trend/${s.street_id}`);
                const trendData = await trendResp.json();

                s.current_level = trendData.current_level;
                s.trend = trendData.trend;
                s.chart = trendData.chart || [];
                s.color = palette[index % palette.length];
            })
        );

        loadDetailedStatus();
        loadTrendGraph();

    } catch (err) {
        console.error("Error", err);
        topStreetsList.innerHTML = `<p class='muted'>Error loading.</p>`;
    }

    // ------------------------------
    // UI BUILDERS
    // ------------------------------

    function loadTopStreetCards() {
        topStreetsList.innerHTML = "";

        streetsData.forEach((s, i) => {
            topStreetsList.innerHTML += `
                <div class="street-card fade-in" style="border-left:5px solid ${palette[i]}">
                    <div class="card-title">${s.display_name}</div>
                    <div class="card-value">${s.peak_water_level.toFixed(2)} m</div>
                    <span class="trend-tag ${s.trend}">
                        ${s.trend === "increasing" ? "⬆ Rising" :
                          s.trend === "decreasing" ? "⬇ Dropping" : "➡ Stable"}
                    </span>
                </div>
            `;
        });
    }

    function loadDetailedStatus() {
        detailedStatus.innerHTML = "";
        streetsData.forEach(s => {
            detailedStatus.innerHTML += `
                <div class="status-box fade-in">
                    <div class="status-title">
                        ${s.display_name}
                    </div>
                    <div class="status-level">
                        <strong>${s.current_level.toFixed(2)} m</strong>
                    </div>
                    <div class="status-trend">
                        ${s.trend === "increasing" ? "📈 Increasing" :
                          s.trend === "decreasing" ? "📉 Decreasing" : "➖ Stable"}
                    </div>
                </div>
            `;
        });
    }

    function loadTrendGraph() {
        const ctx = trendChartCanvas.getContext("2d");

        const labels = streetsData[0]?.chart.map(p => {
            const d = new Date(p.time);
            const date = d.toLocaleDateString([], { day: "2-digit", month: "short" });
            const time = d.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
            return `${date} ${time}`;  // Example: "05 Dec, 14:30"
        }) || [];


        const datasets = streetsData.map((s, idx) => ({
            label: s.display_name,
            data: s.chart.map(p => p.value),
            borderColor: s.color,
            borderWidth: 4,
            tension: 0.2,
            fill: false
        }));

        chart = new Chart(ctx, {
            type: "line",
            data: { labels, datasets },
            options: {
                responsive: true,
                plugins: { legend: { position: "bottom" } },
                elements: {
                    point: { radius: 3 },
                    line: { borderCapStyle: "round" }
                }
            }
        });

        // Generate interactive pill buttons for filters
        const graphFilters = document.getElementById("graphFilters");
        graphFilters.innerHTML = "";

        streetsData.forEach((s, idx) => {
            const btn = document.createElement("button");
            btn.className = "filter-pill active";    // active by default
            btn.dataset.index = idx;
            btn.innerText = s.display_name;

            btn.addEventListener("click", function () {
                const i = parseInt(this.dataset.index);

                // Toggle appearance
                this.classList.toggle("active");

                // Toggle dataset visibility
                chart.data.datasets[i].hidden = !this.classList.contains("active");
                chart.update();
            });

            graphFilters.appendChild(btn);
        });

    }
});
