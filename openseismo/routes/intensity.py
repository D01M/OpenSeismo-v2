"""
Intensity scale and seismic analysis routes.
"""

from flask import Blueprint, jsonify, request

from intensity_calculator import AgencySummaryProcessor

from ..processors.intensity import IntensityCalculator

bp = Blueprint('intensity', __name__, url_prefix='/api/intensity')


@bp.route('/mmi-shindo', methods=['POST'])
def calculate_intensity():
    """Calculate MMI and Shindo intensities for an earthquake."""
    try:
        data = request.get_json() or {}

        if not all(k in data for k in ['magnitude', 'depth_km', 'latitude', 'longitude']):
            return jsonify({"error": "Missing required fields: magnitude, depth_km, latitude, longitude"}), 400

        magnitude = data['magnitude']
        depth_km = data['depth_km']
        latitude = data['latitude']
        longitude = data['longitude']
        distance_km = data.get('distance_km', 0.1)

        fault_type, fault_zone_info = IntensityCalculator.classify_fault_type(latitude, longitude, depth_km)
        mmi = IntensityCalculator.calculate_mmi(magnitude, depth_km, distance_km, fault_type)
        shindo = IntensityCalculator.calculate_shindo(magnitude, depth_km, distance_km, fault_type)

        mmi_scale = IntensityCalculator.get_mmi_scale(mmi)
        shindo_scale = IntensityCalculator.get_shindo_scale(shindo)

        result = {
            "magnitude": magnitude,
            "depth_km": depth_km,
            "distance_km": distance_km,
            "latitude": latitude,
            "longitude": longitude,
            "fault_type": fault_type.value,
            "fault_zone": {
                "type": fault_zone_info.fault_type.value,
                "color": fault_zone_info.color,
                "description": fault_zone_info.description,
                "typical_depth_range": f"{fault_zone_info.typical_depth_min}-{fault_zone_info.typical_depth_max} km"
            },
            "mmi": {
                "value": round(mmi, 2),
                "scale": mmi_scale.name,
                "description": mmi_scale.description,
                "color": mmi_scale.color,
                "integer": int(round(mmi))
            },
            "shindo": {
                "value": round(shindo, 2),
                "scale": shindo_scale.name,
                "description": shindo_scale.description,
                "color": shindo_scale.color
            }
        }

        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route('/report', methods=['POST'])
def intensity_report():
    """Generate comprehensive intensity report for an earthquake."""
    try:
        data = request.get_json() or {}

        if not all(k in data for k in ['magnitude', 'depth_km', 'latitude', 'longitude']):
            return jsonify({"error": "Missing required fields"}), 400

        report = IntensityCalculator.get_intensity_report(
            magnitude=data['magnitude'],
            depth_km=data['depth_km'],
            latitude=data['latitude'],
            longitude=data['longitude']
        )

        return jsonify(report), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route('/grid', methods=['POST'])
def intensity_grid():
    """Calculate intensity grid around epicenter."""
    try:
        data = request.get_json() or {}

        if not all(k in data for k in ['magnitude', 'depth_km', 'latitude', 'longitude']):
            return jsonify({"error": "Missing required fields"}), 400

        grid_points = IntensityCalculator.calculate_intensity_grid(
            magnitude=data['magnitude'],
            depth_km=data['depth_km'],
            latitude=data['latitude'],
            longitude=data['longitude'],
            grid_size_km=data.get('grid_size_km', 50),
            max_distance_km=data.get('max_distance_km', 500)
        )

        return jsonify({
            "magnitude": data['magnitude'],
            "depth_km": data['depth_km'],
            "latitude": data['latitude'],
            "longitude": data['longitude'],
            "grid_points": grid_points,
            "point_count": len(grid_points)
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route('/agency-summary', methods=['POST'])
def process_agency_summary():
    """Process intensity calculations from seismic agency summaries."""
    try:
        data = request.get_json() or {}

        required_fields = ['agency', 'magnitude', 'depth_km', 'latitude', 'longitude', 'summary']
        if not all(k in data for k in required_fields):
            return jsonify({"error": f"Missing required fields: {', '.join(required_fields)}"}), 400

        result = AgencySummaryProcessor.process_agency_summary(
            agency_name=data['agency'],
            magnitude=data['magnitude'],
            depth_km=data['depth_km'],
            latitude=data['latitude'],
            longitude=data['longitude'],
            agency_summary=data['summary']
        )

        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route('/agency-info')
def agency_info():
    """Get information about supported seismic agencies and their intensity scales."""
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
    """Get all intensity scales."""
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
