/**
 * API Module - All fetch/request logic centralized here
 * Provides methods for all backend API calls
 */

const API = {
  BASE_URL: '/api',
  TIMEOUT: 10000,

  /**
   * Generic fetch wrapper with error handling and timeout
   */
  async fetch(endpoint, options = {}) {
    const url = `${this.BASE_URL}${endpoint}`;
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), this.TIMEOUT);

    try {
      const response = await fetch(url, {
        ...options,
        signal: controller.signal
      });

      clearTimeout(timeout);

      if (!response.ok) {
        throw new Error(`API Error: ${response.status} ${response.statusText}`);
      }

      return await response.json();
    } catch (err) {
      clearTimeout(timeout);
      throw err;
    }
  },

  /**
   * App Information
   */
  async getAppInfo() {
    return this.fetch('/app-info');
  },

  /**
   * Earthquake Endpoints
   */
  async getEarthquakesCurrent() {
    return this.fetch('/earthquakes/current');
  },

  async getEarthquakesSince(minutes) {
    return this.fetch(`/earthquakes/since/${minutes}`);
  },

  async getEarthquakeAlerts() {
    return this.fetch('/earthquakes/alerts');
  },

  /**
   * Tsunami Endpoints
   */
  async getTsunamiWarnings() {
    return this.fetch('/tsunami/warnings');
  },

  async getTsunamiAlertConfig() {
    return this.fetch('/tsunami/alerts-config');
  },

  async getTsunamiRegionForecast(region) {
    return this.fetch(`/tsunami/forecast/${region}`);
  },

  /**
   * Intensity Endpoints
   */
  async getIntensityAgencyInfo() {
    return this.fetch('/intensity/agency-info');
  },

  async getIntensityScales() {
    return this.fetch('/intensity/scales');
  },

  /**
   * Location Endpoints
   */
  async searchLocation(query) {
    return this.fetch('/location/search', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query })
    });
  },

  async getLocationInfo(latitude, longitude) {
    return this.fetch('/location/info', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ latitude, longitude })
    });
  }
};
