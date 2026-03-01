import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, Image, TouchableOpacity } from 'react-native';
import { COLORS, SPACING, BORDER_RADIUS, FONT_SIZES, SHADOWS } from '../theme/theme';
import birdImages from '../../assets/birdImages';

// Component that loads local bird images (supports multiple images per bird)
const BirdImage = ({ bird, size = 'large', style, imageIndex = 0 }) => {
  const [currentImageIndex, setCurrentImageIndex] = useState(imageIndex);

  // Reset image index when bird or imageIndex prop changes
  useEffect(() => {
    setCurrentImageIndex(imageIndex);
  }, [bird?.id, imageIndex]);
  
  const getSize = () => {
    switch (size) {
      case 'small':
        return { width: 80, height: 80 };
      case 'medium':
        return { width: 150, height: 150 };
      case 'large':
        return { width: 280, height: 280 };
      default:
        return { width: 280, height: 280 };
    }
  };

  const dimensions = getSize();

  // Get local image source from the image map
  const getImageSource = () => {
    const imageKey = bird.image;
    const images = birdImages[imageKey];
    
    if (!images) return null;
    
    // If single image (old format)
    if (!Array.isArray(images)) return images;
    
    // If multiple images (new format)
    return images[currentImageIndex % images.length];
  };

  // Generate a consistent color based on bird name for placeholder
  const getPlaceholderColor = (name) => {
    const colors = [
      '#4CAF50', '#8BC34A', '#CDDC39', '#009688', '#00BCD4',
      '#03A9F4', '#2196F3', '#3F51B5', '#673AB7', '#9C27B0',
      '#E91E63', '#F44336', '#FF5722', '#FF9800', '#FFC107',
    ];
    let hash = 0;
    for (let i = 0; i < name.length; i++) {
      hash = name.charCodeAt(i) + ((hash << 5) - hash);
    }
    return colors[Math.abs(hash) % colors.length];
  };

  // Get first letter of bird name for placeholder
  const getInitial = () => {
    return bird.names.en.charAt(0).toUpperCase();
  };

  const imageSource = getImageSource();
  const imageKey = bird.image;
  const images = birdImages[imageKey];
  const hasMultipleImages = Array.isArray(images) && images.length > 1;

  if (!imageSource) {
    // Fallback: show placeholder with bird initial
    const placeholderColor = getPlaceholderColor(bird.names.en);
    return (
      <View style={[styles.container, style, { ...dimensions }]}>
        <View style={[styles.placeholder, { backgroundColor: placeholderColor, ...dimensions }]}>
          <Text style={styles.placeholderText}>{getInitial()}</Text>
        </View>
      </View>
    );
  }

  return (
    <View style={[styles.container, style]}>
      <TouchableOpacity
        onPress={() => {
          if (hasMultipleImages) {
            setCurrentImageIndex((currentImageIndex + 1) % images.length);
          }
        }}
        disabled={!hasMultipleImages}
      >
        <Image
          source={imageSource}
          style={[styles.image, dimensions, SHADOWS.medium]}
          resizeMode="cover"
        />
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    alignItems: 'center',
    justifyContent: 'center',
  },
  image: {
    borderRadius: BORDER_RADIUS.large,
  },
  placeholder: {
    alignItems: 'center',
    justifyContent: 'center',
    borderRadius: BORDER_RADIUS.large,
  },
  placeholderText: {
    fontSize: FONT_SIZES.xxxlarge,
    fontWeight: 'bold',
    color: COLORS.white,
  },
  imageCounter: {
    position: 'absolute',
    bottom: 8,
    right: 8,
    backgroundColor: 'rgba(0,0,0,0.7)',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: BORDER_RADIUS.small,
  },
  imageCounterText: {
    color: COLORS.white,
    fontSize: FONT_SIZES.small,
    fontWeight: 'bold',
  },
});

export default BirdImage;
