(function () {
    const defaultCenter = [6.12, 100.37];
    const defaultZoom = 13;

    window.initLeafletMap = function (elementId, options = {}) {
        const center = options.center || defaultCenter;
        const zoom = options.zoom || defaultZoom;
        const map = L.map("floodMap").setView([6.12, 100.37], 13);
        L.tileLayer('https://tiles.stadiamaps.com/tiles/alidade_smooth/{z}/{x}/{y}{r}.png', {
            maxZoom: 20
        }).addTo(map);

        return map;
    };

    window.createLayerGroups = function (map, names = []) {
        const groups = {};
        names.forEach((n) => {
            groups[n] = L.layerGroup().addTo(map);
        });
        return groups;
    };

    window.bindLayerFilters = function (map, layers, filterSelector, clearSelector) {
        const buttons = document.querySelectorAll(filterSelector);
        const clearButton = document.querySelector(clearSelector);

        buttons.forEach((btn) => {
            btn.addEventListener("click", function () {
                const filter = this.dataset.filter;

                Object.values(layers).forEach((layer) => map.removeLayer(layer));
                if (layers[filter]) {
                    map.addLayer(layers[filter]);
                }

                buttons.forEach((b) => b.classList.remove("active"));
                this.classList.add("active");
            });
        });

        if (clearButton) {
            clearButton.addEventListener("click", function () {
                Object.values(layers).forEach((layer) => map.addLayer(layer));
                buttons.forEach((b) => b.classList.remove("active"));
            });
        }
    };
})();
