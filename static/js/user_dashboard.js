document.addEventListener("DOMContentLoaded", function () {
    const alertsList = document.getElementById("alertsList");
    const rainfallText = document.getElementById("rainfallText");
    const areasGrid = document.getElementById("areasGrid");

    // Safely remove segment from street name
    function cleanStreetName(name) {
        if (!name || typeof name !== "string") return "Unknown";
        return name.split("_")[0];
    }

    fetch("/user/dashboard-data")
        .then((r) => r.json())
        .then((data) => {

            // 1. Alerts (past 7 days)
            alertsList.innerHTML = "";
            const alerts = (data.alerts || []).filter(a => {
                const alertDate = new Date(a.prediction_time);
                const sevenDaysAgo = new Date();
                sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 7);
                return alertDate >= sevenDaysAgo;
            });

            if (alerts.length === 0) {
                alertsList.innerHTML = `<p class="muted">No alerts in the past 7 days</p>`;
            } else {
                alerts.forEach((a) => {
                    const severityClass = a.severity ? `tag ${a.severity}` : "badge";
                    const displayName = cleanStreetName(a.street_name);
                    alertsList.innerHTML += `
                        <div class="alert-item">
                            <div class="alert-top">
                                <strong>${displayName}</strong>
                                <span class="${severityClass}">${(a.severity || "alert").toUpperCase()}</span>
                            </div>
                            <div>${a.alert_message || "Flood activity detected."}</div>
                            <div class="alert-meta">${a.prediction_time}</div>
                        </div>
                    `;
                });
            }

            // 2. Top 3 Areas (cards)
            const areas = data.areas || [];
            areasGrid.innerHTML = "";

            areas.forEach((a) => {
                let severity = a.severity_level.toLowerCase();

                let color =
                    severity === "normal" ? "#a8f3b4" :
                    severity === "alert" ? "#ffd166" :
                    "#ff8787";

                areasGrid.innerHTML += `
                    <div class="area-card">
                        <strong>${a.area_name}</strong>
                        <div class="muted">Severity: ${severity}</div>
                        <span class="area-severity" style="background:${color}">
                            ${severity.toUpperCase()}
                        </span>
                    </div>
                `;
            });

            // 3. Flood Map
            const map = initLeafletMap("floodMap");
            const layers = createLayerGroups(map, ["safe", "flooded", "shelters", "areas"]);

            // Safe routes
            (data.safe_routes || []).forEach((r) => {
                L.polyline(r.coords, {
                    color: "#47d1c4",
                    weight: 4
                }).addTo(layers.safe);
            });

            // Flooded routes
            (data.flooded_routes || []).forEach((r) => {
                const color = r.severity === "alert" ? "#ffd166" : "#ff6b6b";
                L.polyline(r.coords, {
                    color,
                    weight: 4
                }).addTo(layers.flooded);
            });

            // Shelters
            (data.shelters || []).forEach(sh => {
                L.marker([sh.lat, sh.lon]).bindPopup(sh.name).addTo(layers.shelters);
            });

            // Top 3 area circles
            areas.forEach((a) => {
                if (a.lat && a.lon) {
                    let severity = a.severity_level.toLowerCase();
                    let color =
                        severity === "normal" ? "#a8f3b4" :
                        severity === "alert" ? "#ffd166" :
                        "#ff8787";

                    L.circle([a.lat, a.lon], {
                        radius: 300,
                        color,
                        fillOpacity: 0.2,
                    }).addTo(layers.areas);
                }
            });

            // 4. Rainfall forecast
            rainfallText.textContent = "Moderate rain expected — 70% chance";

            // 5. Filters
            bindLayerFilters(map, layers, ".filter-btn", "#clearFilter");

        })
        .catch((err) => {
            console.error("Dashboard fetch error:", err);
            alertsList.innerHTML = `<p class="muted">Error loading data</p>`;
            areasGrid.innerHTML = `<p class="muted">Error loading data</p>`;
            rainfallText.textContent = "Error loading forecast";
        });
});





/*
document.addEventListener("DOMContentLoaded", function () {
    const alertsList = document.getElementById("alertsList");
    const rainfallText = document.getElementById("rainfallText");
    const areasGrid = document.getElementById("areasGrid");

    fetch("/user/dashboard-data")
        .then((r) => r.json())
        .then((data) => {

       
            // 1. Alerts (past 7 days)
            alertsList.innerHTML = "";
            const alerts = (data.alerts || []).filter(a => {
                const alertDate = new Date(a.prediction_time);
                const sevenDaysAgo = new Date();
                sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 7);
                return alertDate >= sevenDaysAgo;
            });

            if (alerts.length === 0) {
                alertsList.innerHTML = `<p class="muted">No alerts in the past 7 days</p>`;
            } else {
                alerts.forEach((a) => {
                    const severityClass = a.severity ? `tag ${a.severity}` : "badge";
                    alertsList.innerHTML += `
                        <div class="alert-item">
                            <div class="alert-top">
                                <strong>${a.street_name}</strong>
                                <span class="${severityClass}">${(a.severity || "alert").toUpperCase()}</span>
                            </div>
                            <div>${a.alert_message || "Flood activity detected."}</div>
                            <div class="alert-meta">${a.prediction_time}</div>
                        </div>
                    `;
                });
            }

            // 2️. Top 3 Areas (cards)
            const areas = data.areas || [];
            areasGrid.innerHTML = "";

            areas.forEach((a) => {
                let severity = a.severity_level.toLowerCase();

                let color =
                    severity === "normal" ? "#a8f3b4" :
                    severity === "alert" ? "#ffd166" :
                    "#ff8787";

                areasGrid.innerHTML += `
                    <div class="area-card">
                        <strong>${a.area_name}</strong>
                        <div class="muted">Severity: ${severity}</div>
                        <span class="area-severity" style="background:${color}">
                            ${severity.toUpperCase()}
                        </span>
                    </div>
                `;
            });

            // 3️. Flood Map
            const map = initLeafletMap("floodMap");
            const layers = createLayerGroups(map, ["safe", "flooded", "shelters", "areas"]);

            // Safe routes
            (data.safe_routes || []).forEach((r) => {
                L.polyline(r.coords, {
                    color: "#47d1c4",
                    weight: 4
                }).addTo(layers.safe);
            });

            // Flooded routes
            (data.flooded_routes || []).forEach((r) => {
                const color = r.severity === "alert" ? "#ffd166" : "#ff6b6b";
                L.polyline(r.coords, {
                    color,
                    weight: 4
                }).addTo(layers.flooded);
            });

            // Shelters
            (data.shelters || []).forEach(sh => {
                L.marker([sh.lat, sh.lon]).bindPopup(sh.shelter_name).addTo(layers.shelters);
            });

            // Top 3 area circles (string severity)
            areas.forEach((a) => {
                if (a.lat && a.lon) {
                    let severity = a.severity_level.toLowerCase();
                    let color =
                        severity === "normal" ? "#a8f3b4" :
                        severity === "alert" ? "#ffd166" :
                        "#ff8787";

                    L.circle([a.lat, a.lon], {
                        radius: 300,
                        color,
                        fillOpacity: 0.2,
                    }).addTo(layers.areas);
                }
            });

            // 4️. Rainfall forecast
            rainfallText.textContent = "Moderate rain expected — 70% chance";

            // 5️. Filters
            bindLayerFilters(map, layers, ".filter-btn", "#clearFilter");

        })
        .catch((err) => {
            console.error("Dashboard fetch error:", err);
            alertsList.innerHTML = `<p class="muted">Error loading data</p>`;
            areasGrid.innerHTML = `<p class="muted">Error loading data</p>`;
            rainfallText.textContent = "Error loading forecast";
        });
}); 
*/
