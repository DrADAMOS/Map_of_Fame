let map, markers = [];

function initMap() {
    if (map) return;
    if (typeof L === 'undefined') {
        console.error("Leaflet (L) is not defined. Map cannot be initialized.");
        return;
    }
    try {
        map = L.map('map', {
            zoomControl: false,
            attributionControl: false,
            fadeAnimation: true,
            zoomAnimation: true,
            markerZoomAnimation: true
        }).setView([20, 10], 2);

        L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_nolabels/{z}/{x}/{y}{r}.png').addTo(map);
        console.log("Map initialized successfully.");
    } catch (e) {
        console.error("Error initializing map:", e);
    }
}

function updateMapMarkers(p, t) {
    markers.forEach(m => map.removeLayer(m));

    const bcLabel = t.bc_label + " " + Math.abs(p.by);
    const dcLabel = t.dc_label + " " + Math.abs(p.dy);

    const birthIcon = L.divIcon({
        className: 'custom-marker',
        html: `<div class="pulse" style="--accent:var(--success)"></div><div class="mk-label" style="border-color:var(--success)">${bcLabel}</div>`
    });

    const deathIcon = L.divIcon({
        className: 'custom-marker',
        html: `<div class="pulse" style="--accent:var(--death)"></div><div class="mk-label" style="border-color:var(--death)">${dcLabel}</div>`
    });

    markers = [
        L.marker(p.bc, { icon: birthIcon }).addTo(map),
        L.marker(p.dc, { icon: deathIcon }).addTo(map)
    ];

    const bounds = L.latLngBounds([p.bc, p.dc]);

    // Check if birth and death locations are the same to avoid Leaflet errors with flyToBounds
    const isSameLocation = p.bc[0] === p.dc[0] && p.bc[1] === p.dc[1];

    // Cinematic Flight: Zoom out slightly first, then fly to destination
    const currentZoom = map.getZoom();
    if (currentZoom > 4) {
        map.setZoom(currentZoom - 1, { animate: true });
        setTimeout(() => {
            if (isSameLocation) {
                map.flyTo(p.bc, 5, { duration: 1.5 });
            } else {
                performFlight(bounds);
            }
        }, 300);
    } else {
        if (isSameLocation) {
            map.flyTo(p.bc, 5, { duration: 1.5 });
        } else {
            performFlight(bounds);
        }
    }
}

function performFlight(bounds) {
    map.flyToBounds(bounds, {
        padding: [80, 80],
        maxZoom: 5,
        duration: 2.0, // Slower, more majestic flight
        easeLinearity: 0.15
    });
}
