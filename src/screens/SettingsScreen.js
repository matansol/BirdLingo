import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  SafeAreaView,
  TouchableOpacity,
  ScrollView,
} from 'react-native';
import { StatusBar } from 'expo-status-bar';
import { COLORS, SPACING, BORDER_RADIUS, FONT_SIZES, SHADOWS } from '../theme/theme';
import { useLanguage, LANGUAGES } from '../context/LanguageContext';
import { Button } from '../components';

const SettingsScreen = ({ navigation }) => {
  const { t, language, setLanguage, getTextAlign } = useLanguage();

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar style="dark" />

      {/* Header */}
      <View style={styles.header}>
        <Text style={[styles.title, { textAlign: getTextAlign() }]}>
          {t.settings}
        </Text>
      </View>

      <ScrollView style={styles.scrollView}>
        {/* Language Section */}
        <View style={styles.section}>
          <Text style={[styles.sectionTitle, { textAlign: getTextAlign() }]}>
            {t.chooseLanguage}
          </Text>
          
          <View style={styles.languageOptions}>
            {Object.values(LANGUAGES).map((lang) => (
              <TouchableOpacity
                key={lang.code}
                style={[
                  styles.languageOption,
                  language === lang.code && styles.selectedLanguage,
                ]}
                onPress={() => setLanguage(lang.code)}
                activeOpacity={0.8}
              >
                <View style={styles.languageInfo}>
                  <Text
                    style={[
                      styles.languageName,
                      language === lang.code && styles.selectedLanguageText,
                    ]}
                  >
                    {lang.name}
                  </Text>
                  <Text
                    style={[
                      styles.languageNative,
                      language === lang.code && styles.selectedLanguageNative,
                    ]}
                  >
                    {lang.nativeName}
                  </Text>
                </View>
                {language === lang.code && (
                  <Text style={styles.checkmark}>✓</Text>
                )}
              </TouchableOpacity>
            ))}
          </View>
        </View>

        {/* Info Section */}
        <View style={styles.section}>
          <View style={styles.infoCard}>
            <Text style={styles.infoIcon}>🐦</Text>
            <Text style={[styles.infoTitle, { textAlign: getTextAlign() }]}>
              BirdLingo
            </Text>
            <Text style={[styles.infoText, { textAlign: getTextAlign() }]}>
              Learn to identify 199 bird species from around the world!
            </Text>
            <View style={styles.statsRow}>
              <View style={styles.statItem}>
                <Text style={styles.statNumber}>199</Text>
                <Text style={styles.statLabel}>Birds</Text>
              </View>
              <View style={styles.statItem}>
                <Text style={styles.statNumber}>4</Text>
                <Text style={styles.statLabel}>Levels</Text>
              </View>
              <View style={styles.statItem}>
                <Text style={styles.statNumber}>4</Text>
                <Text style={styles.statLabel}>Categories</Text>
              </View>
            </View>
          </View>
        </View>
      </ScrollView>

      {/* Back Button */}
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
  scrollView: {
    flex: 1,
  },
  section: {
    paddingHorizontal: SPACING.lg,
    marginBottom: SPACING.lg,
  },
  sectionTitle: {
    fontSize: FONT_SIZES.lg,
    fontWeight: '600',
    color: COLORS.textPrimary,
    marginBottom: SPACING.md,
  },
  languageOptions: {
    gap: SPACING.sm,
  },
  languageOption: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: COLORS.white,
    borderRadius: BORDER_RADIUS.lg,
    padding: SPACING.md,
    marginBottom: SPACING.sm,
    borderWidth: 2,
    borderColor: COLORS.white,
    ...SHADOWS.small,
  },
  selectedLanguage: {
    borderColor: COLORS.primaryGreen,
    backgroundColor: COLORS.paleGreen,
  },
  languageInfo: {
    flex: 1,
  },
  languageName: {
    fontSize: FONT_SIZES.md,
    fontWeight: '600',
    color: COLORS.textPrimary,
  },
  languageNative: {
    fontSize: FONT_SIZES.sm,
    color: COLORS.textSecondary,
    marginTop: SPACING.xs,
  },
  selectedLanguageText: {
    color: COLORS.primaryGreen,
  },
  selectedLanguageNative: {
    color: COLORS.primaryGreenDark,
  },
  checkmark: {
    fontSize: FONT_SIZES.xl,
    color: COLORS.primaryGreen,
    fontWeight: 'bold',
  },
  infoCard: {
    backgroundColor: COLORS.white,
    borderRadius: BORDER_RADIUS.xl,
    padding: SPACING.xl,
    alignItems: 'center',
    ...SHADOWS.medium,
  },
  infoIcon: {
    fontSize: 60,
    marginBottom: SPACING.md,
  },
  infoTitle: {
    fontSize: FONT_SIZES.xl,
    fontWeight: 'bold',
    color: COLORS.primaryGreen,
    marginBottom: SPACING.sm,
  },
  infoText: {
    fontSize: FONT_SIZES.sm,
    color: COLORS.textSecondary,
    textAlign: 'center',
    marginBottom: SPACING.lg,
  },
  statsRow: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    width: '100%',
  },
  statItem: {
    alignItems: 'center',
  },
  statNumber: {
    fontSize: FONT_SIZES.xxl,
    fontWeight: 'bold',
    color: COLORS.primaryGreen,
  },
  statLabel: {
    fontSize: FONT_SIZES.xs,
    color: COLORS.textSecondary,
    marginTop: SPACING.xs,
  },
  footer: {
    padding: SPACING.lg,
    alignItems: 'center',
  },
});

export default SettingsScreen;
