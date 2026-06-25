/**
 * Earthquake Monitor - Real-time earthquake monitoring and alerts (3D Globe Version)
 */

class EarthquakeMonitor {
  constructor(globe) {
    this.globe = globe || window.globe3d;
    this.earthquakes = [];
    this.updateInterval = 60000; // 1 minute
    this.updateTimer = null;
    this.minMagnitude = 4.0;
  }

  async init() {
    await this.update();
    this.startPolling();
    console.log('EarthquakeMonitor initialized with 3D Globe');
  }

  async update() {
    try {
      const data = await API.getEarthquakesCurrent();
      this.earthquakes = data.data || [];
      this.render();
    } catch (err) {
      console.error('Failed to fetch earthquakes:', err);
    }
  }

  render() {
    if (!this.globe) {
      console.warn('Globe not initialized');
      return;
    }

    // Clear previous markers
    this.globe.clear();
    
    // Add markers for each earthquake
    for (const eq of this.earthquakes) {
      if ((eq.magnitude || 0) >= this.minMagnitude) {
        this.globe.addEarthquakeMarker(eq.latitude, eq.longitude, eq.magnitude);
      }
    }

    // Update UI
    this.updateStats();
    this.updateList();
  }

  updateStats() {
    const count = this.earthquakes.length;
    const highMag = this.earthquakes.filter(e => e.magnitude >= 6).length;
    
    const countEl = document.getElementById('eq-count');
    const alertEl = document.getElementById('eq-alert');
    
    if (countEl) countEl.textContent = count;
    if (alertEl) {
      if (highMag > 0) {
        alertEl.textContent = 'HIGH ACTIVITY';
        alertEl.style.color = '#ff6464';
      } else {
        alertEl.textContent = 'Normal';
        alertEl.style.color = '#00ff99';
      }
    }
  }

  updateList() {
    const listEl = document.getElementById('earthquake-list');
    if (!listEl) return;

    const filtered = this.earthquakes.filter(eq => (eq.magnitude || 0) >= this.minMagnitude);
    
    if (filtered.length === 0) {
      listEl.innerHTML = '<div class="empty-state">No earthquakes above threshold</div>';
      return;
    }

    const sorted = filtered.sort((a, b) => b.magnitude - a.magnitude);
    listEl.innerHTML = sorted.map((eq, idx) => {
      const mag = (eq.magnitude || 0).toFixed(1);
      const location = eq.location || `${eq.latitude.toFixed(2)}°N, ${eq.longitude.toFixed(2)}°E`;
      let levelClass = 'low';
      if (eq.magnitude >= 7) levelClass = 'critical';
      else if (eq.magnitude >= 6) levelClass = 'high';
      else if (eq.magnitude >= 5) levelClass = 'moderate';
      
      return `<div class="earthquake-item ${levelClass}">
        <span class="magnitude">M${mag}</span> 
        <strong>${location}</strong>
        <div class="meta">Depth: ${(eq.depth_km || 0).toFixed(1)} km</div>
      </div>`;
    }).join('');

    // Update last updated time
    const lastEl = document.getElementById('last-updated');
    if (lastEl) lastEl.textContent = new Date().toLocaleTimeString();
  }

  startPolling() {
    this.updateTimer = setInterval(() => this.update(), this.updateInterval);
  }

  stopPolling() {
    if (this.updateTimer) {
      clearInterval(this.updateTimer);
      this.updateTimer = null;
    }
  }

  setMinMagnitude(value) {
    this.minMagnitude = parseFloat(value);
    this.render();
  }

  getSignificantEarthquakes() {
    return this.earthquakes.filter(eq => eq.magnitude >= 4.0);
  }

  getAlerts() {
    return this.earthquakes.filter(eq => eq.magnitude >= 5.0);
  }
}
