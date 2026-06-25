/**
 * Seismic Map Module - Manages Leaflet map instance and map-related operations
 */

class SeismicMap {
  constructor() {
    this.map = null;
    this.layers = {
      earthquakes: null,
      tsunami: null,
      stations: null,
      tectonic: null
    };
    this.markers = {};
  }

  async init() {
    try {
      this.createMap();
      await this.loadLayers();
      console.log('SeismicMap initialized');
    } catch (err) {
      console.error('Map initialization failed:', err);
      throw err;
    }
  }

  createMap() {
    const mapElement = document.getElementById('map');
    if (!mapElement) {
      throw new Error('Map container not found');
    }

    this.map = L.map('map').setView([20, 140], 3);

    // Base layers
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors',
      maxZoom: 19
    }).addTo(this.map);

    // Layer control
    L.control.layers(
      { 'OpenStreetMap': L.tileLayer('') },
      {},
      { position: 'topleft' }
    ).addTo(this.map);
  }

  async loadLayers() {
    // Initialize layer groups
    this.layers.earthquakes = L.layerGroup().addTo(this.map);
    this.layers.tsunami = L.layerGroup().addTo(this.map);
    this.layers.stations = L.layerGroup();
    this.layers.tectonic = L.layerGroup();
  }

  addEarthquakeMarker(eq) {
    const key = `eq_${eq.id}`;
    if (this.markers[key]) return; // Already added

    const magnitude = eq.magnitude || 0;
    const radius = Math.max(5, Math.min(30, magnitude * 3));
    const color = this.getMagnitudeColor(magnitude);

    const circle = L.circleMarker([eq.latitude, eq.longitude], {
      radius,
      fillColor: color,
      color: '#000',
      weight: 1,
      opacity: 0.8,
      fillOpacity: 0.7
    }).addTo(this.layers.earthquakes);

    circle.bindPopup(`
      <strong>${eq.location || 'Unknown'}</strong><br>
      Magnitude: ${magnitude.toFixed(1)}<br>
      Depth: ${eq.depth_km || '?'} km<br>
      Time: ${new Date(eq.time_utc).toLocaleString()}
    `);

    this.markers[key] = circle;
  }

  addTsunamiMarker(warning) {
    const key = `tsunami_${warning.id}`;
    if (this.markers[key]) return;

    const marker = L.marker([warning.latitude, warning.longitude], {
      icon: L.icon({
        iconUrl: '/static/icons/tsunami.png',
        iconSize: [32, 32]
      })
    }).addTo(this.layers.tsunami);

    marker.bindPopup(`
      <strong>Tsunami Warning</strong><br>
      Level: ${warning.level}<br>
      Region: ${warning.region}
    `);

    this.markers[key] = marker;
  }

  getMagnitudeColor(magnitude) {
    if (magnitude >= 7) return '#cc0000';
    if (magnitude >= 6) return '#ff3300';
    if (magnitude >= 5) return '#ff9900';
    if (magnitude >= 4) return '#ffcc00';
    return '#00ccff';
  }

  clear() {
    this.layers.earthquakes.clearLayers();
    this.layers.tsunami.clearLayers();
    this.markers = {};
  }
}
