"""
Intensity scale processing and conversion module.
Handles seismic intensity calculations and agency-specific scales.
"""

class IntensityCalculator:
    """
    Manages intensity scale conversions and calculations.
    Supports multiple intensity scales: Mercalli (MMI), Shindo, EMS-98.
    """
    
    def __init__(self):
        """Initialize intensity calculator."""
        pass
    
    def magnitude_to_mercalli(self, magnitude):
        """
        Convert earthquake magnitude to Mercalli intensity.
        
        Args:
            magnitude (float): Earthquake magnitude (Richter scale)
            
        Returns:
            dict: Mercalli intensity data
        """
        if magnitude < 2.0:
            level = "I"
            description = "Not felt"
        elif magnitude < 3.0:
            level = "II-III"
            description = "Felt indoors"
        elif magnitude < 4.0:
            level = "IV-V"
            description = "Felt widely"
        elif magnitude < 5.0:
            level = "VI-VII"
            description = "Moderate damage"
        elif magnitude < 6.0:
            level = "VIII"
            description = "Considerable damage"
        elif magnitude < 7.0:
            level = "IX"
            description = "Heavy damage"
        else:
            level = "X+"
            description = "Violent/Total damage"
        
        return {
            "magnitude": magnitude,
            "level": level,
            "description": description
        }
    
    def magnitude_to_shindo(self, magnitude):
        """
        Convert earthquake magnitude to Shindo intensity scale.
        Japanese seismic intensity scale.
        
        Args:
            magnitude (float): Earthquake magnitude
            
        Returns:
            dict: Shindo intensity data
        """
        if magnitude < 2.0:
            level = "0"
            description = "Not felt"
        elif magnitude < 3.0:
            level = "1"
            description = "Felt at night only"
        elif magnitude < 4.0:
            level = "2"
            description = "Felt by most"
        elif magnitude < 4.5:
            level = "3"
            description = "Considerable shaking"
        elif magnitude < 5.0:
            level = "4"
            description = "Strong, some damage"
        elif magnitude < 5.5:
            level = "5-"
            description = "Very strong, considerable damage"
        elif magnitude < 6.0:
            level = "5+"
            description = "Very strong, major damage"
        elif magnitude < 6.5:
            level = "6-"
            description = "Severe, severe damage"
        else:
            level = "6+ / 7"
            description = "Violent, total destruction"
        
        return {
            "magnitude": magnitude,
            "level": level,
            "description": description
        }
    
    def get_intensity_at_distance(self, magnitude, distance_km):
        """
        Estimate intensity at a given distance from epicenter.
        Uses attenuation model.
        
        Args:
            magnitude (float): Earthquake magnitude
            distance_km (float): Distance from epicenter in km
            
        Returns:
            float: Estimated intensity value
        """
        # Simple attenuation model
        # Intensity decreases logarithmically with distance
        if distance_km < 1:
            attenuation = 0
        else:
            attenuation = 2.0 * (magnitude - 1.0) - 2.3 * (distance_km / 10)
        
        return max(0, attenuation)
