"""
Location search and geocoding processing module.
Handles location queries, coordinate conversion, and geographic lookups.
"""

from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut


class LocationSearcher:
    """
    Manages location search and geocoding operations.
    Supports forward and reverse geocoding.
    """
    
    def __init__(self):
        """Initialize location searcher with geocoder."""
        self.geocoder = Nominatim(user_agent="openseismo_lite")
    
    def search(self, query):
        """
        Search for locations by name or address.
        
        Args:
            query (str): Location name or address
            
        Returns:
            list: List of matching locations with coordinates
        """
        try:
            location = self.geocoder.geocode(query)
            if location:
                return [{
                    "name": location.address,
                    "latitude": location.latitude,
                    "longitude": location.longitude,
                    "display_name": location.address
                }]
            return []
        except GeocoderTimedOut:
            return []
        except Exception:
            return []
    
    def reverse_lookup(self, latitude, longitude):
        """
        Get location information from coordinates (reverse geocoding).
        
        Args:
            latitude (float): Latitude coordinate
            longitude (float): Longitude coordinate
            
        Returns:
            dict: Location information
        """
        try:
            location = self.geocoder.reverse(f"{latitude}, {longitude}")
            if location:
                return {
                    "name": location.address,
                    "latitude": latitude,
                    "longitude": longitude,
                    "display_name": location.address
                }
            return None
        except GeocoderTimedOut:
            return None
        except Exception:
            return None
    
    def get_distance(self, lat1, lon1, lat2, lon2):
        """
        Calculate approximate distance between two coordinates (in km).
        Uses Haversine formula approximation.
        
        Args:
            lat1, lon1: First coordinate pair
            lat2, lon2: Second coordinate pair
            
        Returns:
            float: Distance in kilometers
        """
        from math import radians, cos, sin, asin, sqrt
        
        # Convert to radians
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        
        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))
        km = 6371 * c  # Earth radius in km
        
        return km
