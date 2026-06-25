/**
 * UI Controller - Manages UI panels, controls, and user interactions
 */

class UIController {
  constructor(modules) {
    this.modules = modules;
    this.panels = {};
  }

  async init() {
    this.setupPanels();
    this.attachEventListeners();
    console.log('UIController initialized');
  }

  setupPanels() {
    this.panels.earthquakePanel = document.getElementById('earthquake-panel');
    this.panels.tsunamiPanel = document.getElementById('tsunami-panel');
    this.panels.controlPanel = document.getElementById('control-panel');
  }

  attachEventListeners() {
    // Example event listeners
    document.addEventListener('keypress', (e) => {
      if (e.key === 'Escape') this.collapseAllPanels();
    });
  }

  updateEarthquakeCount(count) {
    const elem = document.getElementById('earthquake-count');
    if (elem) elem.textContent = count;
  }

  updateTsunamiWarnings(warnings) {
    const elem = document.getElementById('tsunami-warnings');
    if (elem) {
      elem.textContent = warnings.length > 0 ? `${warnings.length} active` : 'None';
    }
  }

  showNotification(message, type = 'info') {
    const notif = document.createElement('div');
    notif.className = `notification notification-${type}`;
    notif.textContent = message;
    document.body.appendChild(notif);

    setTimeout(() => notif.remove(), 5000);
  }

  collapseAllPanels() {
    Object.values(this.panels).forEach(panel => {
      if (panel) panel.classList.remove('open');
    });
  }
}

// Global UI reference
const UI = {
  showNotification(msg, type) {
    if (app?.modules?.ui) {
      app.modules.ui.showNotification(msg, type);
    }
  },
  updateEarthquakeCount(count) {
    if (app?.modules?.ui) {
      app.modules.ui.updateEarthquakeCount(count);
    }
  },
  updateTsunamiWarnings(warnings) {
    if (app?.modules?.ui) {
      app.modules.ui.updateTsunamiWarnings(warnings);
    }
  }
};
