"""
Earthquake routes - Real-time earthquake monitoring and alerts
"""

from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
from ..processors.earthquake import (
    get_all_earthquakes,
    get_earthquakes_since,
    get_alert_level
)
from ..config import SOUND_ALERTS

bp = Blueprint('earthquakes', __name__, url_prefix='/api/earthquakes')


@bp.route('/current', methods=['GET'])
def get_current():
    """Get the latest earthquake data"""
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
    """Get earthquakes detected in the last N minutes"""
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
    """Get all significant earthquakes and their alert levels"""
    try:
        earthquakes = get_all_earthquakes()
        
        alerts = []
        for eq in earthquakes:
            alert_level = get_alert_level(eq.get('magnitude', 0))
            if alert_level:  # Only include significant earthquakes
                eq['alert_level'] = alert_level
                eq['sound_alert'] = SOUND_ALERTS.get(alert_level)
                alerts.append(eq)
        
        return jsonify({
            "count": len(alerts),
            "alerts": alerts
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
