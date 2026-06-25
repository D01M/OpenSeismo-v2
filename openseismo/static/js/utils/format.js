/**
 * Format Utilities - Text formatting and display helpers
 */

const FormatUtil = {
  /**
   * Format magnitude with one decimal place
   */
  magnitude(mag) {
    return (mag || 0).toFixed(1);
  },

  /**
   * Format depth with "km" suffix
   */
  depth(depthKm) {
    return depthKm ? `${depthKm.toFixed(0)} km` : 'Unknown';
  },

  /**
   * Format coordinates as degrees, minutes, seconds or decimal
   */
  coordinates(lat, lon, format = 'decimal') {
    if (format === 'dms') {
      return `${this.toDMS(lat)}, ${this.toDMS(lon)}`;
    }
    return `${lat.toFixed(4)}, ${lon.toFixed(4)}`;
  },

  /**
   * Convert decimal degrees to degrees, minutes, seconds
   */
  toDMS(decimal) {
    const d = Math.floor(Math.abs(decimal));
    const m = Math.floor((Math.abs(decimal) - d) * 60);
    const s = (((Math.abs(decimal) - d) * 60 - m) * 60).toFixed(1);
    const dir = decimal >= 0 ? 'N/E' : 'S/W';
    return `${d}°${m}'${s}"${dir}`;
  },

  /**
   * Format alert level as badge text
   */
  alertLevel(level) {
    const labels = {
      'low': 'Low',
      'moderate': 'Moderate',
      'high': 'High',
      'critical': 'Critical'
    };
    return labels[level] || 'Unknown';
  },

  /**
   * Format location name, truncating long strings
   */
  location(name, maxLength = 30) {
    if (!name) return 'Unknown';
    return name.length > maxLength ? name.substring(0, maxLength) + '...' : name;
  },

  /**
   * Format time as relative (e.g., "2 hours ago")
   */
  relativeTime(isoString) {
    if (!isoString) return 'Unknown time';
    
    const eventTime = new Date(isoString);
    const now = new Date();
    const diffMs = now - eventTime;
    const diffSecs = Math.floor(diffMs / 1000);
    
    if (diffSecs < 60) return 'Just now';
    if (diffSecs < 3600) return `${Math.floor(diffSecs / 60)} min ago`;
    if (diffSecs < 86400) return `${Math.floor(diffSecs / 3600)} hrs ago`;
    if (diffSecs < 604800) return `${Math.floor(diffSecs / 86400)} days ago`;
    
    return eventTime.toLocaleDateString();
  }
};
