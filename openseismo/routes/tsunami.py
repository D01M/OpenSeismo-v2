"""
Tsunami and early warning routes.
"""

from datetime import datetime

from flask import Blueprint, jsonify, request

from ..config import TSUNAMI_ALERTS
from ..processors.tsunami import TsunamiWarningSystem

bp = Blueprint('tsunami', __name__, url_prefix='/api/tsunami')

tsunami_system = TsunamiWarningSystem()


@bp.route('/warnings', methods=['GET'])
def get_warnings():
    """Get active tsunami warnings."""
    try:
        warnings = tsunami_system.get_warnings()
        return jsonify({
            "count": len(warnings),
            "warnings": warnings
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route('/forecast/<region>', methods=['GET'])
def get_forecast(region):
    """Get tsunami forecast for a specific region."""
    try:
        forecast = tsunami_system.get_forecast(region)
        return jsonify(forecast), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route('/evaluate', methods=['POST'])
def evaluate_tsunami():
    """Evaluate tsunami risk for an earthquake."""
    try:
        data = request.get_json() or {}

        if not all(k in data for k in ['magnitude', 'depth_km', 'latitude', 'longitude']):
            return jsonify({"error": "Missing required fields"}), 400

        result = TsunamiWarningSystem.evaluate_earthquake(
            magnitude=data['magnitude'],
            depth_km=data['depth_km'],
            latitude=data['latitude'],
            longitude=data['longitude']
        )

        result['time'] = data.get('time', '')
        result['analysis_time'] = datetime.utcnow().isoformat()

        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route('/info')
def tsunami_info():
    """Get tsunami warning system information and thresholds."""
    info = {
        "system": "JMA-inspired Tsunami Warning System",
        "warning_levels": {
            "MAJOR_WARNING": {
                "description": "Major tsunami warning - expect destructive waves",
                "wave_height_threshold_m": 3.0,
                "color": "#DC2626"
            },
            "WARNING": {
                "description": "Tsunami warning - dangerous waves expected",
                "wave_height_threshold_m": 1.0,
                "color": "#EA580C"
            },
            "ADVISORY": {
                "description": "Tsunami advisory - minor waves may occur",
                "wave_height_threshold_m": 0.5,
                "color": "#F59E0B"
            },
            "NO_WARNING": {
                "description": "No tsunami threat detected",
                "wave_height_threshold_m": 0.0,
                "color": "#10B981"
            }
        },
        "monitored_regions": [
            "Japan", "Indonesia", "Philippines", "New Zealand",
            "US West Coast", "Chile", "Thailand"
        ],
        "minimum_magnitude_for_warning": 6.5,
        "note": "This is an educational tsunami warning system and NOT an official EEW/TWS system"
    }
    return jsonify(info), 200


@bp.route('/alerts-config', methods=['GET'])
def alerts_config():
    """Get tsunami alert sound configuration."""
    return jsonify(TSUNAMI_ALERTS), 200
