import React from 'react';
import { View, Text, StyleSheet, Modal, TouchableOpacity } from 'react-native';
import { COLORS, SPACING, BORDER_RADIUS, FONT_SIZES, SHADOWS } from '../theme/theme';
import { useLanguage } from '../context/LanguageContext';
import Button from './Button';
import BirdImage from './BirdImage';

const FeedbackModal = ({
  visible,
  isCorrect,
  correctBird,
  selectedBird,
  onNext,
}) => {
  const { t, getBirdName, getTextAlign, language } = useLanguage();

  return (
    <Modal
      visible={visible}
      transparent={true}
      animationType="fade"
      statusBarTranslucent={true}
    >
      <View style={styles.overlay}>
        <View style={styles.container}>
          {/* Icon */}
          <View
            style={[
              styles.iconContainer,
              isCorrect ? styles.successIcon : styles.errorIcon,
            ]}
          >
            <Text style={styles.icon}>{isCorrect ? '✓' : '✗'}</Text>
          </View>

          {/* Title */}
          <Text style={[styles.title, { textAlign: getTextAlign() }]}>
            {isCorrect ? t.great : t.tryAgain}
          </Text>

          {/* Correct Answer */}
          {!isCorrect && correctBird && (
            <View style={styles.answerContainer}>
              <Text style={[styles.label, { textAlign: getTextAlign() }]}>
                {t.correctAnswer}:
              </Text>
              <Text style={[styles.birdName, { textAlign: getTextAlign() }]}>
                {getBirdName(correctBird)}
              </Text>
            </View>
          )}

          {/* Bird Image */}
          {correctBird && (
            <View style={styles.imageWrapper}>
              <BirdImage
                bird={correctBird}
                size="medium"
                imageIndex={Number(correctBird.imageIndex) || 0}
              />
            </View>
          )}

          {/* Description or Scientific Name */}
          {correctBird && (
            <Text style={[styles.description, { textAlign: getTextAlign() }]}>
              {correctBird.description?.[language] || `(${correctBird.scientificName})`}
            </Text>
          )}

          {/* Next Button */}
          <Button
            title={t.next}
            onPress={onNext}
            variant="primary"
            size="large"
            style={styles.nextButton}
          />
        </View>
      </View>
    </Modal>
  );
};

const styles = StyleSheet.create({
  overlay: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    justifyContent: 'center',
    alignItems: 'center',
    padding: SPACING.lg,
  },
  container: {
    backgroundColor: COLORS.white,
    borderRadius: BORDER_RADIUS.xl,
    padding: SPACING.xl,
    alignItems: 'center',
    width: '100%',
    maxWidth: 350,
    ...SHADOWS.large,
  },
  iconContainer: {
    width: 80,
    height: 80,
    borderRadius: 40,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: SPACING.md,
  },
  successIcon: {
    backgroundColor: COLORS.successLight,
  },
  errorIcon: {
    backgroundColor: COLORS.errorLight,
  },
  icon: {
    fontSize: 48,
    color: COLORS.white,
  },
  title: {
    fontSize: FONT_SIZES.xxl,
    fontWeight: 'bold',
    color: COLORS.textPrimary,
    marginBottom: SPACING.md,
  },
  answerContainer: {
    alignItems: 'center',
    marginBottom: SPACING.sm,
  },
  label: {
    fontSize: FONT_SIZES.sm,
    color: COLORS.textSecondary,
    marginBottom: SPACING.xs,
  },
  birdName: {
    fontSize: FONT_SIZES.xl,
    fontWeight: 'bold',
    color: COLORS.primaryGreen,
  },
  description: {
    fontSize: FONT_SIZES.md,
    color: COLORS.textSecondary,
    marginBottom: SPACING.lg,
    paddingHorizontal: SPACING.sm,
    lineHeight: 22,
  },
  imageWrapper: {
    marginVertical: SPACING.sm,
    alignItems: 'center',
    justifyContent: 'center',
  },
  nextButton: {
    width: '100%',
    marginTop: SPACING.md,
  },
});

export default FeedbackModal;
