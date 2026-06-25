"""
Earthquake data processing and analysis
"""

from datetime import datetime, timedelta
from pathlib import Path
import sys

# Add parent directory to path for imports from root
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    from live_earthquake_detector import LiveEarthquakeDetector
except ImportError:
    LiveEarthquakeDetector = None


earthquake_cache = {
    "earthquakes": [],
    "last_update": None
}


def get_alert_level(magnitude):
    """Determine alert level based on magnitude"""
    if magnitude >= 7.0:
        return "critical"
    elif magnitude >= 6.0:
        return "high"
    elif magnitude >= 5.0:
        return "moderate"
    elif magnitude >= 4.0:
        return "low"
    return None


def get_all_earthquakes():
    """
    Fetch all earthquakes from multiple sources.
    Uses cache when available, returns mock data if live detector unavailable.
    """
    if LiveEarthquakeDetector:
        try:
            detector = LiveEarthquakeDetector()
            earthquakes = detector.detect_all()
            return earthquakes
        except Exception:
            pass
    
    # Return mock data for demonstration
    return [
        {
            "id": "usgs_mock_1",
            "latitude": 35.6895,
            "longitude": 139.6917,
            "magnitude": 5.2,
            "depth_km": 15,
            "time_utc": (datetime.utcnow() - timedelta(hours=2)).isoformat() + "Z",
            "location": "Tokyo, Japan",
            "source": "mock"
        },
        {
            "id": "usgs_mock_2",
            "latitude": -33.8688,
            "longitude": 151.2093,
            "magnitude": 4.8,
            "depth_km": 20,
            "time_utc": (datetime.utcnow() - timedelta(hours=4)).isoformat() + "Z",
            "location": "Sydney, Australia",
            "source": "mock"
        },
        {
            "id": "usgs_mock_3",
            "latitude": 37.3611,
            "longitude": -122.0363,
            "magnitude": 4.5,
            "depth_km": 12,
            "time_utc": (datetime.utcnow() - timedelta(hours=1)).isoformat() + "Z",
            "location": "San Francisco, USA",
            "source": "mock"
        },
        {
            "id": "usgs_mock_4",
            "latitude": -12.0464,
            "longitude": -77.0428,
            "magnitude": 6.1,
            "depth_km": 45,
            "time_utc": (datetime.utcnow() - timedelta(hours=6)).isoformat() + "Z",
            "location": "Lima, Peru",
            "source": "mock"
        },
        {
            "id": "usgs_mock_5",
            "latitude": 37.7749,
            "longitude": -122.4194,
            "magnitude": 4.2,
            "depth_km": 10,
            "time_utc": (datetime.utcnow() - timedelta(hours=3)).isoformat() + "Z",
            "location": "San Francisco Bay",
            "source": "mock"
        }
    ]


def get_earthquakes_since(since_time):
    """Get earthquakes that occurred after a specific time"""
    all_earthquakes = get_all_earthquakes()
    
    filtered = []
    for eq in all_earthquakes:
        try:
            eq_time = datetime.fromisoformat(
                eq.get('time_utc', '').replace('Z', '+00:00')
            ) if eq.get('time_utc') else datetime.utcnow()
            
            if eq_time > since_time:
                filtered.append(eq)
        except:
            pass
    
    return filtered
