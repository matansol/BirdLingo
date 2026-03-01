// Nature-inspired theme colors
export const COLORS = {
  // Primary colors
  primaryGreen: '#2E7D32',
  primaryGreenLight: '#4CAF50',
  primaryGreenDark: '#1B5E20',
  
  // Secondary colors
  leafGreen: '#81C784',
  mintGreen: '#A5D6A7',
  paleGreen: '#C8E6C9',
  
  // Neutrals
  white: '#FFFFFF',
  offWhite: '#F5F5F5',
  lightGray: '#E0E0E0',
  mediumGray: '#9E9E9E',
  darkGray: '#424242',
  black: '#212121',
  
  // Feedback colors
  success: '#4CAF50',
  successLight: '#E8F5E9',
  error: '#F44336',
  errorLight: '#FFEBEE',
  
  // Background
  background: '#F1F8E9',
  cardBackground: '#FFFFFF',
  
  // Text
  textPrimary: '#212121',
  textSecondary: '#616161',
  textLight: '#FFFFFF',
  
  // Shadows
  shadowColor: '#000000',
};

export const SPACING = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
  xxl: 48,
};

export const BORDER_RADIUS = {
  sm: 8,
  md: 12,
  lg: 16,
  xl: 24,
  round: 9999,
};

export const FONT_SIZES = {
  xs: 12,
  sm: 14,
  md: 16,
  lg: 20,
  xl: 24,
  xxl: 32,
  xxxl: 40,
};

export const SHADOWS = {
  small: {
    shadowColor: COLORS.shadowColor,
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 2,
  },
  medium: {
    shadowColor: COLORS.shadowColor,
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.15,
    shadowRadius: 8,
    elevation: 4,
  },
  large: {
    shadowColor: COLORS.shadowColor,
    shadowOffset: { width: 0, height: 6 },
    shadowOpacity: 0.2,
    shadowRadius: 12,
    elevation: 8,
  },
};

export default {
  COLORS,
  SPACING,
  BORDER_RADIUS,
  FONT_SIZES,
  SHADOWS,
};
