"""Seismic station routes for OpenSeismo package."""

from flask import Blueprint, jsonify, request

from ..stations.station_manager import StationManager

bp = Blueprint('stations', __name__, url_prefix='/api/stations')

station_manager = StationManager()


@bp.route('', methods=['GET'])
def get_stations():
    """Get normalized seismic station network data."""
    network = request.args.get('network')
    country = request.args.get('country')
    region = request.args.get('region')
    status = request.args.get('status')
    channel = request.args.get('channel')
    tag = request.args.get('tag')
    recent_minutes = request.args.get('recent_minutes', type=int)
    active_recent = request.args.get('active_recent', default='').lower() in {'1', 'true', 'yes', 'on'}

    stations = station_manager.filter_stations(
        network=network,
        country=country,
        region=region,
        status=status,
        channel=channel,
        tag=tag,
        recent_minutes=recent_minutes if active_recent else None,
        active_only=active_recent,
    )

    return jsonify({
        'count': len(stations),
        'stations': stations,
    }), 200
