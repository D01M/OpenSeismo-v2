"""
Earthquake routes - real-time earthquake monitoring and alerts.
"""

from datetime import datetime, timedelta

from flask import Blueprint, jsonify, request
from live_earthquake_detector import LiveEarthquakeDetector

from ..config import SOUND_ALERTS
from ..processors.earthquake import (
    get_alert_level,
    get_all_earthquakes,
    get_earthquakes_since,
)

bp = Blueprint('earthquakes', __name__, url_prefix='/api/earthquakes')


@bp.route('/current', methods=['GET'])
def get_current():
    """Get the latest earthquake data."""
    try:
        earthquakes = get_all_earthquakes()
        return jsonify({
            "count": len(earthquakes),
            "data": earthquakes,
            "timestamp": datetime.utcnow().isoformat()
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route('/since/<minutes>', methods=['GET'])
def get_recent(minutes):
    """Get earthquakes detected in the last N minutes."""
    try:
        minutes_int = int(minutes)
        since_time = datetime.utcnow() - timedelta(minutes=minutes_int)

        earthquakes = get_earthquakes_since(since_time)

        for eq in earthquakes:
            eq['alert_level'] = get_alert_level(eq.get('magnitude', 0))
            eq['sound_alert'] = SOUND_ALERTS.get(eq['alert_level'])

        return jsonify({
            "count": len(earthquakes),
            "since": since_time.isoformat(),
            "current_time": datetime.utcnow().isoformat(),
            "data": earthquakes
        }), 200
    except ValueError:
        return jsonify({"error": "Invalid minutes parameter"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route('/alerts', methods=['GET'])
def get_alerts():
    """Get all significant earthquakes and their alert levels."""
    try:
        earthquakes = get_all_earthquakes()

        alerts = []
        for eq in earthquakes:
            alert_level = get_alert_level(eq.get('magnitude', 0))
            if alert_level:
                eq['alert_level'] = alert_level
                eq['sound_alert'] = SOUND_ALERTS.get(alert_level)
                alerts.append(eq)

        return jsonify({
            "count": len(alerts),
            "alerts": alerts
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route('', methods=['GET'])
def get_earthquakes():
    """Get live earthquakes from USGS with fallback to mock data."""
    try:
        mag_filter = request.args.get('mag_filter', default=0, type=float)
        earthquakes = LiveEarthquakeDetector.get_live_earthquakes(magnitude_filter=mag_filter, enrich=False)

        features = []
        for eq in earthquakes:
            features.append({
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [eq['longitude'], eq['latitude'], eq['depth_km']]
                },
                "properties": {
                    "id": eq['id'],
                    "mag": eq['magnitude'],
                    "place": eq['place'],
                    "time": int(eq['time_ms']),
                    "url": eq['url'],
                    "felt": eq['felt_reports'],
                    "tsunami": eq['tsunami'],
                    "sources": eq['sources'],
                    "risk_assessment": {
                        "level": "moderate" if eq['magnitude'] < 6 else "high",
                        "score": min(10, int(eq['magnitude'] * 1.5)),
                        "description": "Seismic activity detected"
                    }
                }
            })

        if not features:
            mock_earthquakes = [
                {
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": [142.47, 38.27, 15]},
                    "properties": {
                        "id": "us1000mock1",
                        "mag": 5.8,
                        "place": "Eastern Honshu, Japan",
                        "time": 1717604400000,
                        "url": "https://earthquake.usgs.gov/earthquakes/events/us1000mock1/",
                        "felt": 2847,
                        "tsunami": True,
                        "sources": "us,jp",
                        "mmi": 7.2,
                        "cdi": 5.8,
                        "alert": "yellow",
                        "status": "reviewed",
                        "risk_assessment": {"level": "high", "score": 8, "description": "Moderate seismic activity"}
                    }
                },
                {
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": [95.28, 28.45, 32]},
                    "properties": {
                        "id": "us1000mock2",
                        "mag": 6.1,
                        "place": "Central Chile",
                        "time": 1717561200000,
                        "url": "https://earthquake.usgs.gov/earthquakes/events/us1000mock2/",
                        "felt": 5621,
                        "tsunami": False,
                        "sources": "us,cl",
                        "mmi": 7.8,
                        "cdi": 6.1,
                        "alert": "orange",
                        "status": "reviewed",
                        "risk_assessment": {"level": "high", "score": 9, "description": "High seismic activity"}
                    }
                }
            ]
            features = mock_earthquakes

        return jsonify({"type": "FeatureCollection", "features": features}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route('/live', methods=['GET'])
def get_live_earthquakes():
    """Get current live earthquakes with ShakeMax intensities and hexagon grids."""
    try:
        magnitude_filter = request.args.get('magnitude_filter', 4.5, type=float)
        enrich = request.args.get('enrich', 'true').lower() == 'true'

        earthquakes = LiveEarthquakeDetector.get_live_earthquakes(
            magnitude_filter=magnitude_filter,
            enrich=enrich
        )

        return jsonify({
            "status": "success",
            "count": len(earthquakes),
            "timestamp": datetime.utcnow().isoformat() + 'Z',
            "earthquakes": earthquakes
        }), 200
    except Exception as e:
        return jsonify({"error": str(e), "count": 0, "earthquakes": []}), 500


@bp.route('/live/<eq_id>', methods=['GET'])
def get_earthquake_detail(eq_id):
    """Get detailed information for a specific earthquake."""
    try:
        earthquakes = LiveEarthquakeDetector.get_live_earthquakes(magnitude_filter=0, enrich=True)

        for eq in earthquakes:
            if eq['id'] == eq_id:
                return jsonify({"status": "success", "earthquake": eq}), 200

        return jsonify({"error": "Earthquake not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route('/shakemax-grid/<eq_id>', methods=['GET'])
def get_shakemax_grid(eq_id):
    """Get ShakeMax hexagon grid for a specific earthquake."""
    try:
        earthquakes = LiveEarthquakeDetector.get_live_earthquakes(magnitude_filter=0, enrich=False)

        eq = None
        for earthquake in earthquakes:
            if earthquake['id'] == eq_id:
                eq = earthquake
                break

        if not eq:
            return jsonify({"error": "Earthquake not found"}), 404

        grid_radius = request.args.get('grid_radius', 300, type=int)
        hex_size = request.args.get('hex_size', 15, type=int)

        hexagons = LiveEarthquakeDetector.generate_hexagon_grid(
            latitude=eq['latitude'],
            longitude=eq['longitude'],
            magnitude=eq['magnitude'],
            depth_km=eq['depth_km'],
            grid_radius_km=grid_radius,
            hex_size_km=hex_size
        )

        return jsonify({
            "status": "success",
            "earthquake_id": eq_id,
            "magnitude": eq['magnitude'],
            "latitude": eq['latitude'],
            "longitude": eq['longitude'],
            "depth_km": eq['depth_km'],
            "hexagon_count": len(hexagons),
            "grid_radius_km": grid_radius,
            "hexagon_size_km": hex_size,
            "hexagons": hexagons
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route('/shakemax-levels', methods=['GET'])
def get_shakemax_levels():
    """Get ShakeMax intensity level definitions for legend display."""
    try:
        return jsonify({
            "status": "success",
            "levels": LiveEarthquakeDetector.SHAKEMAX_LEVELS
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route('/new-since', methods=['POST'])
def get_new_earthquakes():
    """Get earthquakes detected since a specific time."""
    try:
        data = request.get_json() or {}

        if 'since_timestamp' not in data:
            return jsonify({"error": "since_timestamp required"}), 400

        since_time = datetime.fromisoformat(data['since_timestamp'].replace('Z', '+00:00'))
        min_magnitude = data.get('min_magnitude', 4.0)

        all_earthquakes = LiveEarthquakeDetector.get_live_earthquakes(
            magnitude_filter=min_magnitude,
            enrich=True
        )

        new_earthquakes = []
        for eq in all_earthquakes:
            eq_time = datetime.fromisoformat(eq.get('time_utc', '').replace('Z', '+00:00')) if eq.get('time_utc') else datetime.utcnow()
            if eq_time > since_time:
                alert_level = get_alert_level(eq['magnitude'])
                eq['alert_level'] = alert_level
                eq['sound_alert'] = SOUND_ALERTS.get(alert_level)
                new_earthquakes.append(eq)

        return jsonify({
            "count": len(new_earthquakes),
            "since": since_time.isoformat(),
            "current_time": datetime.utcnow().isoformat(),
            "earthquakes": sorted(new_earthquakes, key=lambda x: x['magnitude'], reverse=True)
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
