"""
Tsunami and early warning routes
"""

from flask import Blueprint, jsonify, request
from ..processors.tsunami import TsunamiWarningSystem
from ..config import TSUNAMI_ALERTS

bp = Blueprint('tsunami', __name__, url_prefix='/api/tsunami')

tsunami_system = TsunamiWarningSystem()


@bp.route('/warnings', methods=['GET'])
def get_warnings():
    """Get active tsunami warnings"""
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
    """Get tsunami forecast for a specific region"""
    try:
        forecast = tsunami_system.get_forecast(region)
        return jsonify(forecast), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route('/alerts-config', methods=['GET'])
def alerts_config():
    """Get tsunami alert sound configuration"""
    return jsonify(TSUNAMI_ALERTS), 200
