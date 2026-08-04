"""Metadata and map-layer API routes."""

from flask import Blueprint, jsonify

bp = Blueprint('metadata', __name__, url_prefix='/api')


@bp.route('/volcanoes')
def get_volcanoes():
    """Return sample volcano metadata for the map."""
    volcanoes = {
        'type': 'FeatureCollection',
        'features': [
            {
                'type': 'Feature',
                'geometry': {'type': 'Point', 'coordinates': [139.4928, 35.3607]},
                'properties': {'name': 'Mount Fuji', 'status': 'dormant', 'alert_level': 1, 'last_eruption': '1707'},
            },
            {
                'type': 'Feature',
                'geometry': {'type': 'Point', 'coordinates': [122.7597, 5.3521]},
                'properties': {'name': 'Mount Pinatubo', 'status': 'active', 'alert_level': 2, 'last_eruption': '1991'},
            },
            {
                'type': 'Feature',
                'geometry': {'type': 'Point', 'coordinates': [103.8343, 3.2675]},
                'properties': {'name': 'Mount Merapi', 'status': 'active', 'alert_level': 3, 'last_eruption': '2010'},
            },
        ],
    }
    return jsonify(volcanoes), 200


@bp.route('/faults')
def get_faults():
    """Return sample fault metadata."""
    faults = {
        'type': 'FeatureCollection',
        'features': [
            {
                'type': 'Feature',
                'geometry': {'type': 'Point', 'coordinates': [-115.5, 32.5]},
                'properties': {'name': 'San Andreas Fault', 'type': 'transform', 'activity': 'high'},
            },
            {
                'type': 'Feature',
                'geometry': {'type': 'Point', 'coordinates': [142.5, 38.5]},
                'properties': {'name': 'Japan Trench', 'type': 'subduction', 'activity': 'very_high'},
            },
        ],
    }
    return jsonify(faults), 200


@bp.route('/disaster-risks')
def get_disaster_risks():
    """Return disaster risk metadata."""
    risks = {
        'type': 'FeatureCollection',
        'features': [
            {
                'type': 'Feature',
                'geometry': {'type': 'Point', 'coordinates': [139.7674, 35.6764]},
                'properties': {'name': 'Tokyo High Risk', 'risk_level': 'high', 'hazard': 'earthquake'},
            },
            {
                'type': 'Feature',
                'geometry': {'type': 'Point', 'coordinates': [121.5645, 25.0443]},
                'properties': {'name': 'Taiwan Moderate Risk', 'risk_level': 'moderate', 'hazard': 'earthquake'},
            },
        ],
    }
    return jsonify(risks), 200


@bp.route('/safety-summary')
def get_safety_summary():
    """Return a compact safety summary."""
    summary = {
        'summary': [
            {
                'kind': 'Seismic Activity',
                'risk_level': 'moderate',
                'name': 'Global seismic activity elevated',
                'score': 6,
                'safety': [
                    'Monitor official earthquake agencies',
                    'Review preparedness plans in seismic zones',
                ],
            },
            {
                'kind': 'Tsunami Risk',
                'risk_level': 'low',
                'name': 'No active tsunami threats',
                'score': 2,
                'safety': ['Coastal monitoring systems operational'],
            },
        ]
    }
    return jsonify(summary), 200
