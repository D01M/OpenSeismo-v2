# OpenSeismo Lite - Refactored Modular Architecture

## Overview

OpenSeismo Lite has been refactored into a modular, scalable structure optimized for:
- **Browser deployment** with lightweight asset loading
- **Windows executable packaging** via PyInstaller
- **Code maintainability** with clear separation of concerns
- **Easy feature expansion** without affecting other modules

## Directory Structure

```
openseismo/
├── app.py                    # Flask app factory and route registration
├── config.py                 # Centralized configuration and constants
├── static/
│   ├── css/
│   │   ├── base.css         # Core typography, colors, layout
│   │   ├── map.css          # Leaflet map styling
│   │   └── panels.css       # UI panels and sidebars
│   └── js/
│       ├── main.js          # App initialization and module orchestration
│       ├── api.js           # All fetch/request logic
│       ├── map/
│       │   ├── initMap.js   # Leaflet map setup
│       │   ├── layers.js    # Layer management (todo)
│       │   ├── markers.js   # Marker creation/management (todo)
│       │   └── popups.js    # Popup/tooltip handling (todo)
│       ├── seismic/
│       │   ├── events.js    # Earthquake monitoring
│       │   ├── tsunami.js   # Tsunami monitoring
│       │   ├── intensity.js # Intensity scales (todo)
│       │   ├── stations.js  # Seismic stations (todo)
│       │   └── waveform.js  # Waveform viewer (lazy-loaded)
│       ├── ui/
│       │   ├── controls.js  # Buttons, toggles, interactions
│       │   ├── panels.js    # Panel management (todo)
│       │   ├── filters.js   # Filter controls (todo)
│       │   └── notifications.js # Alert messages (todo)
│       └── utils/
│           ├── format.js    # Text formatting helpers
│           ├── time.js      # Time/date utilities (todo)
│           └── geo.js       # Geolocation helpers (todo)
├── templates/
│   └── index.html           # Main application template
├── routes/
│   ├── earthquakes.py       # Earthquake API endpoints
│   ├── tsunami.py           # Tsunami API endpoints
│   ├── intensity.py         # Intensity scales API
│   └── location.py          # Location search API
├── processors/
│   ├── earthquake.py        # Earthquake data processing
│   ├── tsunami.py           # Tsunami processing
│   └── intensity.py         # Intensity calculation (todo)
├── utils/
│   └── asset_path.py        # Asset loading (dev & PyInstaller modes)
└── data/
    ├── tectonic_zones.json  # Geological fault data
    └── station_cache.json   # Cached seismic station data
```

## Module Responsibilities

### Backend (Python)

**app.py**
- Flask application factory
- Route blueprint registration
- Error handlers
- Does NOT contain business logic

**config.py**
- App metadata (name, version)
- Flask settings
- API endpoints and URLs
- Alert/threshold configurations
- Magnitude thresholds
- Feature flags

**routes/**
- One file per API feature (earthquakes, tsunami, intensity, location)
- Only request handling and JSON response formatting
- Call processors for business logic

**processors/**
- Business logic (data transformation, calculations)
- Integration with external systems
- Caching logic
- Earthquake detection, tsunami analysis, intensity calculations

**utils/asset_path.py**
- Handles asset loading for both:
  - Development (runs as Python script)
  - Production (packaged as .exe via PyInstaller)
- Automatically detects and uses `sys._MEIPASS` when frozen

### Frontend (JavaScript)

**main.js**
- App initialization
- Module orchestration
- Does NOT contain feature logic

**api.js**
- All `fetch()` calls
- Request/response handling
- Error handling
- Timeout management
- Central request utility

**map/initMap.js**
- Leaflet map creation
- Layer groups setup
- Marker management
- Map interactions

**seismic/events.js**
- Earthquake monitoring logic
- Real-time updates via polling
- Alert level determination
- Marker rendering on map

**seismic/tsunami.js**
- Tsunami warning monitoring
- Regional forecasting
- Update polling

**ui/controls.js**
- Panel management
- Button event listeners
- Notification display
- UI state management

**utils/format.js**
- Text formatting (magnitude, depth, coordinates)
- DMS coordinate conversion
- Localization helpers
- No DOM manipulation or API calls

### Styling (CSS)

**base.css**
- CSS variables (colors, spacing)
- Typography
- Global buttons, inputs
- Notification styles
- Utility classes

**map.css**
- Leaflet map customization
- Marker styles
- Control customization
- Legend styling

**panels.css**
- Panel layouts (absolute positioned)
- List item styling
- Filter controls
- Loading/empty states
- Toggle buttons

## Development Workflow

### Running Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Start the dev server
python -m openseismo.app
```

Then open http://localhost:5000 in your browser.

### Adding a New Feature

1. **Create API endpoint** in `routes/` (e.g., `routes/stations.py`)
2. **Add processor logic** in `processors/` (e.g., `processors/stations.py`)
3. **Create JavaScript module** in `static/js/seismic/` or `static/js/ui/`
4. **Add API methods** to `static/js/api.js`
5. **Import and initialize** in `static/js/main.js`
6. **Add UI** to `templates/index.html`
7. **Add styling** to appropriate CSS file

### Asset Loading

The `asset_path.py` helper ensures:
- ✅ During development: loads from `openseismo/static/` and `openseismo/data/`
- ✅ After PyInstaller build: loads from bundled `_internal/openseismo/` directory
- ✅ Relative paths work on Windows without issues

Example usage in Python code:
```python
from openseismo.utils.asset_path import get_asset_path
data_file = get_asset_path('data', 'stations.json')
css_file = get_asset_path('static', 'css', 'base.css')
```

## Building for Windows

### Method 1: Using Python script
```bash
python build_windows.py
```

### Method 2: Using PyInstaller directly
```bash
pyinstaller --clean -y openseismo.spec
```

Output: `dist/OpenSeismo Lite.exe`

The executable includes:
- ✅ Python runtime and all dependencies
- ✅ Flask server
- ✅ Static files (CSS, JS)
- ✅ Templates
- ✅ Data files
- ✅ All third-party packages

## Key Design Patterns

### 1. No Global State
- Use class instances, not global variables
- Pass references to dependent modules
- Example: `earthquakeMonitor = new EarthquakeMonitor(map)`

### 2. Module Exports
- JavaScript modules: return class or object
- Python routes: use Flask blueprints
- Makes testing easier

### 3. Configuration Centralization
- All constants in `config.py`
- No hardcoded values scattered in code
- Easy to adjust thresholds, APIs, colors

### 4. Lazy Loading
- Heavy features (waveform viewer, etc.) loaded on demand
- List in `config.LAZY_LOAD_FEATURES`
- Reduces initial load time

### 5. Error Handling
- API errors caught and displayed
- Backend errors return JSON with error message
- Frontend shows user-friendly notifications

## Performance Considerations

### CSS
- Three focused files (~15KB combined gzipped)
- CSS variables for theming
- Flexbox for responsive layout

### JavaScript
- Modular structure enables tree-shaking
- No jQuery dependency (vanilla DOM APIs)
- Efficient DOM updates
- Consider minification for production

### Data
- Earthquakes cached locally
- Station data cached between updates
- Configurable cache expiration

### Browser Load
```
Initial:  ~300KB (HTML + CSS + JS + Leaflet)
Map tiles: ~1-2MB (from CDN, cached by browser)
API data: ~100-500KB (gzip compressed)
```

## Packaging with PyInstaller

The `openseismo.spec` file configures:
- Entry point: `run_desktop.py`
- Includes all Flask data files
- Bundles static/ and templates/
- No console window (clean desktop app)
- Icon support (provide `openseismo/assets/icon.ico`)

Key PyInstaller settings:
```python
datas = [
    ('openseismo/static', 'openseismo/static'),
    ('openseismo/templates', 'openseismo/templates'),
    ('openseismo/data', 'openseismo/data'),
]
```

## Configuration

Edit `openseismo/config.py` to:
- Change map center/zoom
- Adjust magnitude thresholds
- Update API endpoints
- Configure cache settings
- Enable/disable features

Common configurations:
```python
MAGNITUDE_THRESHOLD_LOW = 4.0
CACHE_EXPIRE_SECONDS = 3600
FLASK_PORT = 5000
MAP_DEFAULT_ZOOM = 3
```

## Debugging

### Development Mode
```python
# In config.py
FLASK_DEBUG = True  # Enables auto-reload and error messages
```

### Browser Console
```javascript
// Check app status
console.log(app.initialized);
console.log(app.modules);
console.log(app.config);

// Manual API calls
API.getEarthquakesCurrent().then(data => console.log(data));
```

### Server Logs
```bash
# Run with verbose output
python -m openseismo.app --debug
```

## Future Enhancements

- [ ] Real-time WebSocket updates instead of polling
- [ ] Offline mode with service workers
- [ ] Advanced waveform visualization
- [ ] Machine learning intensity prediction
- [ ] Mobile app variant
- [ ] Dark mode support
- [ ] i18n (internationalization)
- [ ] User preferences storage

## Migration from Old Structure

Files to phase out:
- `server.py` → Refactored into `openseismo/` modules
- `app.py` → Refactored into `openseismo/app.py`
- `static/` (old) → `openseismo/static/`
- `templates/` (old) → `openseismo/templates/`

Existing imports from old modules still work if they're in the root directory, but new code should use the modular structure.

## Contributing

1. Follow the module structure
2. Keep modules focused and single-purpose
3. Add docstrings to functions and classes
4. Keep configuration in `config.py`
5. Add unit tests in `tests/` (when created)
6. Document new features

## License

Same as main OpenSeismo project
