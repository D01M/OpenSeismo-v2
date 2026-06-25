"""
Location search and geographic information routes
"""

from flask import Blueprint, jsonify, request

bp = Blueprint('location', __name__, url_prefix='/api/location')


@bp.route('/search', methods=['GET', 'POST'])
def search():
    """
    Search for locations by name or coordinates
    GET: ?query=<location name or "lat,lon">
    POST: {"query": "<location name or coordinates>"}
    """
    try:
        if request.method == 'POST':
            data = request.get_json() or {}
            query = data.get('query', '').strip()
        else:
            query = request.args.get('query', '').strip()
        
        if not query:
            return jsonify({"error": "Query parameter required"}), 400
        
        # TODO: Implement location search using LocationSearcher
        return jsonify({
            "query": query,
            "results": []
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route('/info', methods=['POST'])
def info():
    """
    Get comprehensive location information
    JSON: {"latitude": float, "longitude": float}
    """
    try:
        data = request.get_json() or {}
        lat = data.get('latitude')
        lon = data.get('longitude')
        
        if lat is None or lon is None:
            return jsonify({"error": "latitude and longitude required"}), 400
        
        # TODO: Implement location info retrieval
        return jsonify({
            "latitude": lat,
            "longitude": lon,
            "info": {}
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
