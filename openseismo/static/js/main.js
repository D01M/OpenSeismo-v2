/**
 * OpenSeismo Lite - Main Application Entry Point
 * Initializes all modules and connects them together with 3D Globe
 */

class OpenSeismoApp {
  constructor() {
    this.initialized = false;
    this.modules = {};
  }

  async init() {
    try {
      console.log('Initializing OpenSeismo Lite with 3D Globe...');

      // Initialize 3D Globe first
      if (window.globe3d) {
        this.modules.globe = window.globe3d;
        console.log('3D Globe initialized');
      } else {
        console.error('3D Globe not available, initializing...');
        this.modules.globe = new Globe3D();
      }

      // Initialize monitoring modules
      await this.initializeModules();

      // Setup UI controls
      this.setupControls();

      this.initialized = true;
      console.log('OpenSeismo Lite ready with 3D Globe');
    } catch (err) {
      console.error('Initialization failed:', err);
    }
  }

  async initializeModules() {
    // Earthquake monitoring
    this.modules.earthquakes = new EarthquakeMonitor(this.modules.globe);
    await this.modules.earthquakes.init();

    // Tsunami monitoring
    this.modules.tsunami = new TsunamiMonitor(this.modules.globe);
    await this.modules.tsunami.init();

    // UI Controller
    this.modules.ui = new UIController(this.modules);
    await this.modules.ui.init();
  }

  setupControls() {
    // Magnitude filter
    const magSlider = document.getElementById('magnitude-slider');
    if (magSlider) {
      magSlider.addEventListener('input', (e) => {
        const value = e.target.value;
        document.getElementById('magnitude-value').textContent = `Min: ${value}`;
        if (this.modules.earthquakes) {
          this.modules.earthquakes.setMinMagnitude(value);
        }
      });
    }

    // Panel visibility
    document.getElementById('show-eq-panel')?.addEventListener('click', () => {
      document.getElementById('earthquake-panel').style.display = 'block';
    });

    document.getElementById('show-tsunami-panel')?.addEventListener('click', () => {
      document.getElementById('tsunami-panel').style.display = 'block';
    });

    // Refresh data
    document.getElementById('refresh-btn')?.addEventListener('click', async () => {
      if (this.modules.earthquakes) {
        await this.modules.earthquakes.update();
      }
      if (this.modules.tsunami) {
        await this.modules.tsunami.update();
      }
    });

    // Close buttons
    document.querySelectorAll('.close-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.target.closest('.panel').style.display = 'none';
      });
    });

    // Panel close buttons in control panel
    document.getElementById('btn-earthquakes')?.addEventListener('click', () => {
      document.getElementById('earthquake-panel').style.display = 
        document.getElementById('earthquake-panel').style.display === 'none' ? 'block' : 'none';
    });

    document.getElementById('btn-tsunami')?.addEventListener('click', () => {
      document.getElementById('tsunami-panel').style.display = 
        document.getElementById('tsunami-panel').style.display === 'none' ? 'block' : 'none';
    });
  }

  getModule(name) {
    return this.modules[name];
  }
}

// Global app instance
const app = new OpenSeismoApp();

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  app.init();
});
