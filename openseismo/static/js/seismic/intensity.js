/**
 * Intensity Scale Module - Earthquake magnitude to intensity conversion
 * (Placeholder for future implementation)
 */

const IntensityUtil = {
  /**
   * Get Modified Mercalli Intensity from magnitude
   */
  getMercalliIntensity(magnitude) {
    if (magnitude < 1) return 'Not Felt';
    if (magnitude < 2) return 'I (Not felt)';
    if (magnitude < 3) return 'II-III (Weak)';
    if (magnitude < 4) return 'IV-V (Moderate)';
    if (magnitude < 5) return 'VI (Strong)';
    if (magnitude < 6) return 'VII-VIII (Very Strong)';
    if (magnitude < 7) return 'IX (Violent)';
    if (magnitude < 8) return 'X-XI (Extreme)';
    return 'XII (Total Destruction)';
  },

  /**
   * Get Shindo Scale intensity from magnitude
   */
  getShindoIntensity(magnitude) {
    if (magnitude < 2) return '0 (Not felt)';
    if (magnitude < 3) return '1 (Weak)';
    if (magnitude < 4) return '2 (Light)';
    if (magnitude < 4.5) return '3 (Moderate)';
    if (magnitude < 5) return '4 (Strong)';
    if (magnitude < 5.5) return '5- (Strong+)';
    if (magnitude < 6) return '5+ (Very Strong)';
    if (magnitude < 6.5) return '6- (Very Strong+)';
    if (magnitude < 7) return '6+ (Extreme)';
    return '7 (Total/Near Total Destruction)';
  }
};
