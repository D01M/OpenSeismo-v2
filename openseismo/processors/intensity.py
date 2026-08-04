"""
Intensity scale processing and conversion module.
Handles seismic intensity calculations and agency-specific scales.
"""

from intensity_calculator import AgencySummaryProcessor, IntensityCalculator as _IntensityCalculator


class IntensityCalculator(_IntensityCalculator):
    """Compatibility wrapper around the shared intensity calculator implementation."""

    pass
