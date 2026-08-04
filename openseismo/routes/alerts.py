"""Alert-related API routes."""

from flask import Blueprint, jsonify, request

from ..config import EEW_ALERTS, SOUND_ALERTS, TSUNAMI_ALERTS

bp = Blueprint('alerts', __name__, url_prefix='/api')


@bp.route('/alerts/preferences', methods=['GET', 'POST'])
def alert_preferences():
    """Get or set alert preferences."""
    if request.method == 'GET':
        return jsonify({
            'sound_enabled': True,
            'notification_enabled': True,
            'min_magnitude_threshold': 4.5,
            'alert_levels': ['low', 'moderate', 'high', 'critical'],
            'sound_volume': 0.7,
            'auto_mute_after_seconds': 60,
            'vibration_enabled': True,
            'region_filter': None,
        }), 200

    data = request.get_json() or {}
    prefs = {
        'sound_enabled': bool(data.get('sound_enabled', True)),
        'notification_enabled': bool(data.get('notification_enabled', True)),
        'min_magnitude_threshold': float(data.get('min_magnitude_threshold', 4.5)),
        'alert_levels': data.get('alert_levels', ['low', 'moderate', 'high', 'critical']),
        'sound_volume': max(0.0, min(1.0, float(data.get('sound_volume', 0.7)))),
        'auto_mute_after_seconds': int(data.get('auto_mute_after_seconds', 60)),
        'vibration_enabled': bool(data.get('vibration_enabled', True)),
        'region_filter': data.get('region_filter'),
    }
    return jsonify({'status': 'saved', 'preferences': prefs}), 200


@bp.route('/sound-alerts/config')
def sound_alerts_config():
    """Expose sound-alert configuration."""
    return jsonify({
        'sound_alerts': SOUND_ALERTS,
        'supported_alert_types': ['earthquake', 'tsunami', 'aftershock'],
    }), 200


@bp.route('/tsunami-alerts/config')
def tsunami_alerts_config():
    """Expose tsunami alert configuration."""
    return jsonify({
        'tsunami_alerts': TSUNAMI_ALERTS,
        'siren_info': {
            'type': 'frequency sweep',
            'description': 'Japanese-style tsunami warning siren with rising/falling frequency modulation',
        },
    }), 200


@bp.route('/eew-alerts/config')
def eew_alerts_config():
    """Expose EEW alert configuration."""
    return jsonify({
        'eew_alerts': EEW_ALERTS,
        'eew_info': {
            'type': 'rapid beep sequence',
            'description': 'Japanese-style Earthquake Early Warning rapid alert beeps',
            'trigger_magnitude': 5.0,
            'purpose': 'Alerts the user before strong shaking arrives',
        },
    }), 200


@bp.route('/notifications/send', methods=['POST'])
def send_notification():
    """Return notification payload for client-side browser notifications."""
    data = request.get_json() or {}
    if not all(k in data for k in ['title', 'body']):
        return jsonify({'error': 'title and body required'}), 400

    notification = {
        'title': data['title'],
        'body': data['body'],
        'icon': data.get('icon', '/static/earthquake-icon.png'),
        'badge': data.get('badge', '/static/earthquake-badge.png'),
        'tag': data.get('tag', 'earthquake-alert'),
        'requireInteraction': True,
    }
    return jsonify({'notification': notification}), 200
