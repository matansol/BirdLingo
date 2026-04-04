import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  SafeAreaView,
  ScrollView,
  Alert,
} from 'react-native';
import { StatusBar } from 'expo-status-bar';
import { COLORS, SPACING, BORDER_RADIUS, FONT_SIZES, SHADOWS } from '../theme/theme';
import { useLanguage } from '../context/LanguageContext';
import { useProgress } from '../context/ProgressContext';
import { Button } from '../components';

const StatisticsScreen = ({ navigation }) => {
  const { t, getTextAlign } = useLanguage();
  const { tierStats, resetTier, isLoaded } = useProgress();

  const tierRows = [
    { tier: 1, title: t.level1Title },
    { tier: 2, title: t.level2Title },
    { tier: 3, title: t.level3Title },
  ];

  const handleResetTier = (tier) => {
    Alert.alert(
      t.resetTier,
      `${t.resetTierConfirm} ${tier}?`,
      [
        { text: t.cancel, style: 'cancel' },
        {
          text: t.reset,
          style: 'destructive',
          onPress: () => resetTier(tier),
        },
      ]
    );
  };

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar style="dark" />

      <View style={styles.header}>
        <Text style={[styles.title, { textAlign: getTextAlign() }]}>
          {t.statistics}
        </Text>
        <Text style={[styles.subtitle, { textAlign: getTextAlign() }]}>
          {t.statisticsSubtitle}
        </Text>
      </View>

      {!isLoaded ? (
        <View style={styles.loadingWrap}>
          <Text style={styles.loadingText}>{t.loadingProgress}</Text>
        </View>
      ) : (
        <ScrollView style={styles.scrollView} contentContainerStyle={styles.scrollContent}>
          {tierRows.map(({ tier, title }) => {
            const stats = tierStats[tier] || { total: 0, recognized: 0, percentage: 0 };
            return (
              <View key={tier} style={styles.tierCard}>
                <Text style={[styles.tierTitle, { textAlign: getTextAlign() }]}>
                  {title}
                </Text>

                <Text style={[styles.percentage, { textAlign: getTextAlign() }]}>
                  {stats.percentage}%
                </Text>

                <Text style={[styles.countText, { textAlign: getTextAlign() }]}>
                  {stats.recognized} / {stats.total} {t.birdsRecognized}
                </Text>

                <Button
                  title={`${t.resetTier} ${tier}`}
                  onPress={() => handleResetTier(tier)}
                  variant="outline"
                  size="medium"
                  style={styles.resetButton}
                />
              </View>
            );
          })}
        </ScrollView>
      )}

      <View style={styles.footer}>
        <Button
          title={t.backToMenu}
          onPress={() => navigation.goBack()}
          variant="primary"
          size="large"
        />
      </View>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  header: {
    paddingHorizontal: SPACING.lg,
    paddingTop: SPACING.xl,
    paddingBottom: SPACING.md,
  },
  title: {
    fontSize: FONT_SIZES.xxl,
    fontWeight: 'bold',
    color: COLORS.primaryGreen,
  },
  subtitle: {
    marginTop: SPACING.xs,
    fontSize: FONT_SIZES.sm,
    color: COLORS.textSecondary,
  },
  loadingWrap: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingText: {
    fontSize: FONT_SIZES.md,
    color: COLORS.textSecondary,
  },
  scrollView: {
    flex: 1,
  },
  scrollContent: {
    paddingHorizontal: SPACING.lg,
    paddingBottom: SPACING.md,
  },
  tierCard: {
    backgroundColor: COLORS.white,
    borderRadius: BORDER_RADIUS.xl,
    padding: SPACING.lg,
    marginBottom: SPACING.md,
    ...SHADOWS.medium,
  },
  tierTitle: {
    fontSize: FONT_SIZES.lg,
    color: COLORS.textPrimary,
    fontWeight: '700',
    marginBottom: SPACING.md,
  },
  percentage: {
    fontSize: FONT_SIZES.xxxl,
    fontWeight: 'bold',
    color: COLORS.primaryGreen,
  },
  countText: {
    marginTop: SPACING.sm,
    marginBottom: SPACING.md,
    fontSize: FONT_SIZES.md,
    color: COLORS.textSecondary,
  },
  resetButton: {
    width: '100%',
  },
  footer: {
    padding: SPACING.lg,
    alignItems: 'center',
  },
});

export default StatisticsScreen;
