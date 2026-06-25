"""
OpenSeismo Configuration
Central configuration for constants, API endpoints, cache settings, and app metadata
"""

import os
import sys
from pathlib import Path

# App metadata
APP_NAME = "OpenSeismo Lite"
APP_VERSION = "2.0.0"
DESCRIPTION = "Real-time earthquake monitoring with EEW alerts and tsunami warnings"

# Get app root directory
if getattr(sys, 'frozen', False):
    # Running as PyInstaller exe
    APP_ROOT = Path(sys._MEIPASS) / "openseismo"
else:
    # Running as script
    APP_ROOT = Path(__file__).parent

STATIC_DIR = APP_ROOT / "static"
TEMPLATES_DIR = APP_ROOT / "templates"
DATA_DIR = APP_ROOT / "data"

# Flask configuration
FLASK_HOST = "127.0.0.1"
FLASK_PORT = 5000
FLASK_DEBUG = False
JSON_SORT_KEYS = False

# External API endpoints
API_ENDPOINTS = {
    "USGS": "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson",
    "CSEM": "http://www.seismo.ethz.ch/json",
    "JMA": "https://www.jma.go.jp/bosai/quake/quake_0_0.json",
    "EMSC": "https://www.seismicportal.eu/fdsnws/event/1/query"
}

# Cache settings
CACHE_MAX_EARTHQUAKES = 1000
CACHE_EXPIRE_SECONDS = 3600
STATION_CACHE_FILE = DATA_DIR / "station_cache.json"

# Earthquake thresholds
MAGNITUDE_THRESHOLD_LOW = 4.0
MAGNITUDE_THRESHOLD_MODERATE = 5.0
MAGNITUDE_THRESHOLD_HIGH = 6.0
MAGNITUDE_THRESHOLD_CRITICAL = 7.0

# Sound alert configuration
SOUND_ALERTS = {
    "low": {
        "frequency": 440,        # A4 note
        "duration_ms": 100,
        "volume": 0.3,
        "magnitude_threshold": 4.0,
    },
    "moderate": {
        "frequency": 660,        # E5 note
        "duration_ms": 200,
        "volume": 0.6,
        "magnitude_threshold": 5.0,
    },
    "high": {
        "frequency": 880,        # A5 note
        "duration_ms": 300,
        "volume": 0.8,
        "magnitude_threshold": 6.0,
    },
    "critical": {
        "frequency": 1046,       # C6 note
        "duration_ms": 400,
        "volume": 1.0,
        "magnitude_threshold": 7.0,
    }
}

# Tsunami alert configuration
TSUNAMI_ALERTS = {
    "advisory": {
        "type": "siren",
        "pattern": "sweep",
        "frequency_start": 600,
        "frequency_end": 1200,
        "duration_ms": 2000,
        "volume": 0.8,
        "cycles": 2,
    },
    "warning": {
        "type": "siren",
        "pattern": "sweep",
        "frequency_start": 600,
        "frequency_end": 1200,
        "duration_ms": 3000,
        "volume": 1.0,
        "cycles": 3,
    },
    "major_warning": {
        "type": "siren",
        "pattern": "sweep",
        "frequency_start": 600,
        "frequency_end": 1200,
        "duration_ms": 4000,
        "volume": 1.0,
        "cycles": 4,
    }
}

# Map configuration
MAP_CENTER_LAT = 20.0
MAP_CENTER_LON = 140.0
MAP_DEFAULT_ZOOM = 3
MAP_MIN_ZOOM = 2
MAP_MAX_ZOOM = 18

# Seismic stations
SEISMIC_STATIONS = {
    "jp_stations": 18,
    "global_stations": 70,
    "coverage": "Global with emphasis on Pacific Rim"
}

# UI/UX configuration
THEME_COLORS = {
    "primary": "#0066cc",
    "secondary": "#ff6600",
    "success": "#00cc66",
    "warning": "#ffcc00",
    "danger": "#cc0000"
}

# Lazy loading thresholds (load on demand)
LAZY_LOAD_FEATURES = [
    "waveform_viewer",
    "station_detail_viewer",
    "audio_playback"
]

# Feature flags
FEATURES = {
    "earthquake_feed": True,
    "tsunami_warnings": True,
    "eew_alerts": True,
    "live_updates": True,
    "sound_alerts": True,
    "intensity_scales": True,
}
