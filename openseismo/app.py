"""
OpenSeismo Lite - Main Flask Application
Starts the Flask server and serves the web interface
"""

from flask import Flask, send_from_directory, render_template
from pathlib import Path
import sys
import logging

# App initialization
from .config import (
    APP_NAME, APP_VERSION, STATIC_DIR, TEMPLATES_DIR,
    FLASK_HOST, FLASK_PORT, FLASK_DEBUG
)
from .utils.asset_path import get_asset_path


def create_app():
    """Create and configure Flask application"""
    
    app = Flask(
        __name__,
        static_folder=str(STATIC_DIR),
        static_url_path="/static",
        template_folder=str(TEMPLATES_DIR)
    )
    
    # Configuration
    app.config['JSON_SORT_KEYS'] = False
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = FLASK_DEBUG
    
    # Logging
    if not FLASK_DEBUG:
        logging.getLogger('werkzeug').setLevel(logging.ERROR)
    
    # Register blueprints (route modules)
    from .routes import earthquakes, tsunami, intensity, location
    
    app.register_blueprint(earthquakes.bp)
    app.register_blueprint(tsunami.bp)
    app.register_blueprint(intensity.bp)
    app.register_blueprint(location.bp)
    
    # Root routes
    @app.route('/')
    def index():
        """Serve main application page with 3D Globe"""
        return render_template('index.html')
    
    @app.route('/api/app-info')
    def app_info():
        """Get application metadata"""
        return {
            'name': APP_NAME,
            'version': APP_VERSION,
            'timestamp': __import__('datetime').datetime.utcnow().isoformat()
        }
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors"""
        return {'error': 'Not found'}, 404
    
    @app.errorhandler(500)
    def server_error(error):
        """Handle 500 errors"""
        return {'error': 'Server error'}, 500
    
    return app


def run_app(host=FLASK_HOST, port=FLASK_PORT, debug=FLASK_DEBUG):
    """Run the Flask application"""
    app = create_app()
    app.run(host=host, port=port, debug=debug, use_reloader=debug)


if __name__ == '__main__':
    run_app()
