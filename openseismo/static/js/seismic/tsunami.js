/**
 * Tsunami Monitor - Real-time tsunami warning monitoring (3D Globe Version)
 */

class TsunamiMonitor {
  constructor(globe) {
    this.globe = globe || window.globe3d;
    this.warnings = [];
    this.updateInterval = 300000; // 5 minutes
    this.updateTimer = null;
  }

  async init() {
    await this.update();
    this.startPolling();
    console.log('TsunamiMonitor initialized with 3D Globe');
  }

  async update() {
    try {
      const data = await API.getTsunamiWarnings();
      this.warnings = data.warnings || [];
      this.render();
    } catch (err) {
      console.error('Failed to fetch tsunami warnings:', err);
    }
  }

  render() {
    const listEl = document.getElementById('tsunami-list');
    if (!listEl) return;

    if (this.warnings.length === 0) {
      listEl.innerHTML = '<div class="empty-state">No active tsunami warnings</div>';
      const countEl = document.getElementById('tsunami-count');
      if (countEl) countEl.textContent = 'None';
      return;
    }

    const countEl = document.getElementById('tsunami-count');
    if (countEl) countEl.textContent = this.warnings.length;

    listEl.innerHTML = this.warnings.map((warning, idx) => {
      const regions = (warning.affected_areas || []).join(', ');
      const status = warning.status || 'Active';
      return `<div class="tsunami-item">
        <strong>${warning.advisory || 'Tsunami Warning'}</strong>
        <div class="meta">Status: ${status}</div>
        <div class="meta">Regions: ${regions || 'Unknown'}</div>
        <div class="meta">Magnitude: ${(warning.magnitude || 0).toFixed(1)}</div>
      </div>`;
    }).join('');
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

  getMajorWarnings() {
    return this.warnings.filter(w => w.level === 'major_warning');
  }
}
