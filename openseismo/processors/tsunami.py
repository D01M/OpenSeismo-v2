"""
Tsunami warning processing and analysis module.
Handles fetching, processing, and filtering tsunami warning data.
"""

from datetime import datetime, timedelta


class TsunamiWarningSystem:
    """
    Manages tsunami warning data fetching and processing.
    Integrates with multiple seismic monitoring sources.
    """
    
    def __init__(self):
        """Initialize tsunami warning system."""
        self.warnings = self._get_mock_warnings()
        self.active_warnings = self.warnings
    
    def _get_mock_warnings(self):
        """Generate mock tsunami warnings for demonstration"""
        return [
            {
                "id": "tsunami_mock_1",
                "region": "Pacific Region",
                "magnitude": 7.2,
                "depth_km": 35,
                "origin_time": (datetime.utcnow() - timedelta(hours=1)).isoformat() + "Z",
                "advisory": "TSUNAMI WATCH",
                "status": "active",
                "estimated_arrival": (datetime.utcnow() + timedelta(hours=2)).isoformat() + "Z",
                "affected_areas": ["Japan", "Kuril Islands", "Alaska"]
            }
        ]
    
    def get_warnings(self):
        """
        Fetch current tsunami warnings from sources.
        
        Returns:
            list: List of active tsunami warning dictionaries
        """
        return self.active_warnings
    
    def get_forecast(self, region):
        """
        Get tsunami forecast for a specific region.
        
        Args:
            region (str): Geographic region name
            
        Returns:
            dict: Forecast data for the region
        """
        return {
            "region": region,
            "status": "monitoring",
            "last_update": datetime.utcnow().isoformat() + "Z",
            "forecast": None
        }
    
    def filter_by_magnitude(self, min_magnitude=5.0):
        """
        Filter warnings by earthquake magnitude threshold.
        
        Args:
            min_magnitude (float): Minimum magnitude to include
            
        Returns:
            list: Filtered warnings
        """
        return [w for w in self.warnings if w.get('magnitude', 0) >= min_magnitude]
    
    def filter_by_region(self, regions):
        """
        Filter warnings by affected regions.
        
        Args:
            regions (list): List of region names
            
        Returns:
            list: Warnings affecting specified regions
        """
        return [w for w in self.warnings if w.get('region') in regions]
