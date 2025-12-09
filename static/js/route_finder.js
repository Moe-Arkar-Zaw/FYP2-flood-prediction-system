document.addEventListener("DOMContentLoaded", function() {
    const map = L.map("routeMap").setView([6.12, 100.37], 13);
    L.tileLayer('https://tiles.stadiamaps.com/tiles/alidade_smooth/{z}/{x}/{y}{r}.png', {
        maxZoom: 20
    }).addTo(map);

    const routeLayer = L.layerGroup().addTo(map);
    const findBtn = document.getElementById("findRouteBtn");
    const distanceText = document.getElementById("routeDistance");

    // Function to render a route
    function renderRoute(routeData) {
        routeLayer.clearLayers();
        const allCoords = [];

        (routeData.coordinates || []).forEach(seg => {
            const color = seg.severity === "normal" ? "#47d1c4"
                        : seg.severity === "alert" ? "#ffd166"
                        : "#ff6b6b";

            const line = L.polyline([[seg.start_lat, seg.start_lon], [seg.end_lat, seg.end_lon]], {
                color, weight: 6
            });
            line.addTo(routeLayer);

            allCoords.push([seg.start_lat, seg.start_lon], [seg.end_lat, seg.end_lon]);
        });

        if (allCoords.length > 0) map.fitBounds(allCoords);
        // Display distance with 2 decimal places
        distanceText.textContent = `Total Distance: ${routeData.total_distance.toFixed(2)} meters`;
        distanceText.classList.remove("hidden");
    }

    // Check sessionStorage for saved route
    const savedRoute = sessionStorage.getItem("lastRoute");
    if (savedRoute) {
        try {
            const routeData = JSON.parse(savedRoute);
            renderRoute(routeData);
        } catch (err) {
            console.warn("Failed to load saved route:", err);
        }
    }

    // Event listener for finding route
    findBtn.addEventListener("click", function() {
        const start = document.getElementById("startStreet").value.trim();
        const end = document.getElementById("endStreet").value.trim();
        if (!start || !end) return alert("Enter both start and end streets.");

        fetch("/user/api/find-safest-route", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ start, end })
        })
        .then(r => r.json())
        .then(data => {
            if (data.error) return alert(data.error);

            // Save to sessionStorage
            sessionStorage.setItem("lastRoute", JSON.stringify(data));

            // Render the route
            renderRoute(data);
        })
        .catch(() => alert("Unable to compute route."));
    });
});
