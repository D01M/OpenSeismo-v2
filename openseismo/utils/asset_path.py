"""
Asset path helper - handles both development and PyInstaller packaged modes
"""

import sys
from pathlib import Path


def get_asset_path(*path_parts):
    """
    Get absolute path to an asset file.
    Works correctly both during development and when packaged with PyInstaller.
    
    Usage:
        css_path = get_asset_path('static', 'css', 'base.css')
        json_path = get_asset_path('data', 'stations.json')
    
    Args:
        *path_parts: Path segments to join
        
    Returns:
        Path object pointing to the asset
    """
    if getattr(sys, 'frozen', False):
        # Running as PyInstaller executable
        base_dir = Path(sys._MEIPASS) / "openseismo"
    else:
        # Running as normal Python script
        base_dir = Path(__file__).parent
    
    return base_dir.joinpath(*path_parts)


def get_static_url(relative_path):
    """
    Get static file URL for HTML templates.
    
    Args:
        relative_path: Path relative to static/ directory
        
    Returns:
        URL string for use in templates
    """
    return f"/static/{relative_path}"


def ensure_data_dir():
    """
    Ensure data directory exists and is writable.
    Create it if necessary.
    """
    data_dir = get_asset_path('data')
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir
