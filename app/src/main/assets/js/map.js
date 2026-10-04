let map, markers = [], mapOverlay;

// Fully offline Blind Map. The SVG contains borders only: no country or city names.
const DARK_MAP_ASSET = 'world_blind_dark.svg';
const LIGHT_MAP_ASSET = 'world_blind_light.svg';

// Label layout is intentionally handled in screen pixels rather than geographic
// distance. This keeps labels readable on small Android screens at every zoom.
let markerLayoutFrame = null;

function scheduleMarkerLabelLayout() {
    if (markerLayoutFrame !== null) return;
    markerLayoutFrame = requestAnimationFrame(() => {
        markerLayoutFrame = null;
        applyMarkerLabelLayout();
    });
}

function rectsOverlap(a, b, gap = 6) {
    return !(
        a.right + gap < b.left ||
        a.left - gap > b.right ||
        a.bottom + gap < b.top ||
        a.top - gap > b.bottom
    );
}

function labelRect(label) {
    // getBoundingClientRect reflects the final CSS transform, which is exactly
    // what we need for collision testing on the actual device viewport.
    return label.getBoundingClientRect();
}

function setLabelPosition(label, position) {
    label.classList.remove(
        'label-pos-top',
        'label-pos-bottom',
        'label-pos-left',
        'label-pos-right',
        'label-pos-top-left',
        'label-pos-top-right',
        'label-pos-bottom-left',
        'label-pos-bottom-right',
        'label-pos-center'
    );
    label.classList.add(`label-pos-${position}`);
}

function applyMarkerLabelLayout() {
    if (!map || markers.length === 0) return;

    const zoom = map.getZoom();
    const labels = markers
        .map(marker => marker.getElement()?.querySelector('.mk-label'))
        .filter(Boolean);

    if (labels.length === 0) return;

    // At world/continental zoom, labels are intentionally hidden. Markers remain
    // visible, so the map still communicates the locations without clutter.
    const hideBelowZoom = 2.75;
    const compactZoom = 3.75;

    labels.forEach(label => {
        label.classList.remove('label-hidden');
        label.style.visibility = 'hidden';
    });

    if (zoom < hideBelowZoom) {
        labels.forEach(label => label.classList.add('label-hidden'));
        return;
    }

    // With only a few pixels between locations, showing both labels is worse than
    // showing the primary birth label. At the next zoom level both labels return.
    if (zoom < compactZoom && labels.length > 1) {
        const points = markers.map(marker => map.latLngToContainerPoint(marker.getLatLng()));
        const dx = points[0].x - points[1].x;
        const dy = points[0].y - points[1].y;
        const distance = Math.hypot(dx, dy);

        if (distance < 110) {
            labels[0].classList.remove('label-hidden');
            setLabelPosition(labels[0], 'top');
            labels[0].style.visibility = 'visible';
            labels.slice(1).forEach(label => label.classList.add('label-hidden'));
            return;
        }
    }

    const positions = [
        'top', 'bottom', 'left', 'right',
        'top-left', 'top-right', 'bottom-left', 'bottom-right'
    ];

    // Try every sensible placement for each label. The first non-overlapping
    // placement wins; if none is possible, keep a stable side placement rather
    // than allowing labels to sit directly on top of each other.
    const placed = [];

    labels.forEach((label, index) => {
        let placedPosition = null;

        for (const position of positions) {
            setLabelPosition(label, position);
            label.style.visibility = 'visible';
            const candidate = labelRect(label);

            const overlaps = placed.some(other => rectsOverlap(candidate, other, 7));
            if (!overlaps) {
                placedPosition = position;
                placed.push(candidate);
                break;
            }
        }

        if (!placedPosition) {
            // If the two labels cannot both fit, hide the secondary one. This is
            // preferable to unreadable stacked text and is reversible on zoom.
            if (index > 0) {
                label.classList.add('label-hidden');
                label.style.visibility = 'hidden';
            } else {
                setLabelPosition(label, 'top');
                label.style.visibility = 'visible';
                placed.push(labelRect(label));
            }
        }
    });
}

function initMap() {
    console.log("initMap starting...");
    if (typeof L === 'undefined') {
        console.warn("Leaflet not ready, retrying...");
        setTimeout(initMap, 300);
        return;
    }

    const container = document.getElementById('map');
    if (!container) return;

    if (map) {
        map.invalidateSize();
        scheduleMarkerLabelLayout();
        return;
    }

    try {
        console.log("Initializing Leaflet map...");
        map = L.map('map', {
            crs: L.CRS.EPSG4326,
            zoomControl: false,
            attributionControl: false,
            fadeAnimation: false,
            zoomAnimation: false,
            markerZoomAnimation: false,
            inertia: true,
            preferCanvas: true,
            dragging: true,
            touchZoom: true,
            doubleClickZoom: true,
            boxZoom: true,
            tap: true
        }).setView([20, 10], 2);

        map.on('zoomend moveend', scheduleMarkerLabelLayout);
        map.on('resize', scheduleMarkerLabelLayout);

        const mode = (window.Android && Android.getAppTheme) ? Android.getAppTheme() : 'dark';
        const asset = mode === 'light' ? LIGHT_MAP_ASSET : DARK_MAP_ASSET;
        const bounds = [[-90, -180], [90, 180]];
        mapOverlay = L.imageOverlay(asset, bounds, {
            opacity: 1,
            interactive: false
        }).addTo(map);
        const area = document.getElementById('map-area');
        if (area) area.style.background = mode === 'light' ? '#f2f2f2' : '#1f1f1f';

        // Force a series of re-renders to catch layout shifts on Android.
        [100, 500, 1200].forEach(delay => {
            setTimeout(() => {
                if (map) {
                    map.invalidateSize();
                    scheduleMarkerLabelLayout();
                }
            }, delay);
        });

    } catch (e) {
        console.error("Map Init Error:", e);
    }
}

function setMapTheme(mode) {
    if (!map || !mapOverlay) return;
    const asset = mode === 'light' ? LIGHT_MAP_ASSET : DARK_MAP_ASSET;
    mapOverlay.setUrl(asset);
    const area = document.getElementById('map-area');
    if (area) area.style.background = mode === 'light' ? '#f2f2f2' : '#1f1f1f';
    scheduleMarkerLabelLayout();
}

function updateMapMarkers(p, t) {
    if (!map) {
        initMap();
        if (!map) return;
    }

    if (!p.bc || !p.dc || !Array.isArray(p.bc) || !Array.isArray(p.dc)) return;

    const bcLabel = t.bc_label + " " + Utils.formatYear(p.by, t);
    const dcLabel = t.dc_label + " " + Utils.formatYear(p.dy, t);

    const birthIcon = L.divIcon({
        className: 'custom-marker',
        iconSize: [1, 1],
        iconAnchor: [0, 0],
        html: `<div class="pulse" style="--accent:var(--success)"></div><div class="mk-label label-pos-top" style="border-color:var(--success)">${bcLabel}</div>`
    });

    const deathIcon = L.divIcon({
        className: 'custom-marker',
        iconSize: [1, 1],
        iconAnchor: [0, 0],
        html: `<div class="pulse" style="--accent:var(--death)"></div><div class="mk-label label-pos-bottom" style="border-color:var(--death)">${dcLabel}</div>`
    });

    if (markers.length === 2) {
        markers[0].setLatLng(p.bc).setIcon(birthIcon);
        markers[1].setLatLng(p.dc).setIcon(deathIcon);
    } else {
        markers = [
            L.marker(p.bc, { icon: birthIcon }).addTo(map),
            L.marker(p.dc, { icon: deathIcon }).addTo(map)
        ];
    }

    const bounds = L.latLngBounds([p.bc, p.dc]);
    const isSameLocation = p.bc[0] === p.dc[0] && p.bc[1] === p.dc[1];

    if (isSameLocation) {
        map.setView(p.bc, 5, { animate: false });
    } else {
        map.fitBounds(bounds, {
            padding: [60, 60],
            maxZoom: 5,
            animate: false
        });
    }

    // fitBounds/setView updates the viewport asynchronously; schedule after it
    // so collision measurements use the final screen coordinates.
    setTimeout(scheduleMarkerLabelLayout, 0);
}
