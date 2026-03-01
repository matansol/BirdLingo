import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { COLORS, SPACING, BORDER_RADIUS, FONT_SIZES, SHADOWS } from '../theme/theme';
import { useLanguage } from '../context/LanguageContext';

const SessionStats = ({ correct, wrong }) => {
  const { t } = useLanguage();
  const total = correct + wrong;
  const percentage = total > 0 ? Math.round((correct / total) * 100) : 0;

  return (
    <View style={styles.container}>
      <View style={styles.statItem}>
        <Text style={styles.label}>{t.correct}:</Text>
        <Text style={[styles.value, styles.correctValue]}>{correct}</Text>
      </View>
      <View style={styles.divider} />
      <View style={styles.statItem}>
        <Text style={styles.label}>{t.wrong}:</Text>
        <Text style={[styles.value, styles.wrongValue]}>{wrong}</Text>
      </View>
      {total > 0 && (
        <>
          <View style={styles.divider} />
          <View style={styles.statItem}>
            <Text style={styles.percentageValue}>{percentage}%</Text>
          </View>
        </>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    backgroundColor: COLORS.white,
    borderRadius: BORDER_RADIUS.md,
    paddingVertical: SPACING.sm,
    paddingHorizontal: SPACING.md,
    alignItems: 'center',
    ...SHADOWS.small,
  },
  statItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: SPACING.sm,
  },
  label: {
    fontSize: FONT_SIZES.sm,
    color: COLORS.textSecondary,
    marginRight: SPACING.xs,
  },
  value: {
    fontSize: FONT_SIZES.md,
    fontWeight: 'bold',
  },
  correctValue: {
    color: COLORS.success,
  },
  wrongValue: {
    color: COLORS.error,
  },
  percentageValue: {
    fontSize: FONT_SIZES.md,
    fontWeight: 'bold',
    color: COLORS.primaryGreen,
  },
  divider: {
    width: 1,
    height: 20,
    backgroundColor: COLORS.lightGray,
  },
});

export default SessionStats;
