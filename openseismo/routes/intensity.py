"""
Intensity scale and seismic analysis routes
"""

from flask import Blueprint, jsonify

bp = Blueprint('intensity', __name__, url_prefix='/api/intensity')


@bp.route('/agency-info')
def agency_info():
    """Get information about supported seismic agencies and their intensity scales"""
    return jsonify({
        "supported_agencies": {
            "USGS": {
                "name": "United States Geological Survey",
                "description": "Operates ShakeMap for earthquake early warning",
                "region": "Primarily USA and global coverage",
                "intensity_scale": "MMI (Modified Mercalli Intensity)",
                "data_fields": ["max_mmi_intensity"]
            },
            "ESMC": {
                "name": "European Seismic Commission",
                "description": "European earthquake monitoring",
                "region": "Europe and Mediterranean",
                "intensity_scale": "EMS-98",
                "data_fields": ["ems98_intensity"]
            },
            "CSEM": {
                "name": "Swiss Seismological Commission",
                "description": "Alpine earthquake monitoring",
                "region": "Switzerland and Alpine region",
                "intensity_scale": "Swiss scale (1-12)",
                "data_fields": ["csem_intensity"]
            },
            "JMA": {
                "name": "Japan Meteorological Agency",
                "description": "Official earthquake and tsunami early warning",
                "region": "Japan and surrounding regions",
                "intensity_scale": "Shindo Scale (0-7)",
                "data_fields": ["shindo_scale"]
            }
        }
    }), 200


@bp.route('/scales')
def scales():
    """Get all intensity scales"""
    return jsonify({
        "mmi": {
            "name": "Modified Mercalli Intensity Scale",
            "range": "I to XII"
        },
        "shindo": {
            "name": "Japan Meteorological Agency Shindo Scale",
            "range": "0 to 7"
        }
    }), 200
