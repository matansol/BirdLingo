import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  SafeAreaView,
  ImageBackground,
} from 'react-native';
import { StatusBar } from 'expo-status-bar';
import { COLORS, SPACING, BORDER_RADIUS, FONT_SIZES, SHADOWS } from '../theme/theme';
import { useLanguage } from '../context/LanguageContext';
import { Button } from '../components';

const MainMenuScreen = ({ navigation }) => {
  const { t, getTextAlign } = useLanguage();

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar style="dark" />

      {/* Header with Title */}
      <View style={styles.header}>
        <Text style={styles.appIcon}>🦜</Text>
        <Text style={[styles.title, { textAlign: getTextAlign() }]}>
          {t.appTitle}
        </Text>
        <Text style={[styles.subtitle, { textAlign: getTextAlign() }]}>
          Learn Bird Species
        </Text>
      </View>

      {/* Decorative birds */}
      <View style={styles.decoration}>
        <Text style={styles.decorIcon}>🐦</Text>
        <Text style={[styles.decorIcon, styles.decorIcon2]}>🦅</Text>
        <Text style={[styles.decorIcon, styles.decorIcon3]}>🦉</Text>
      </View>

      {/* Menu Buttons */}
      <View style={styles.menuContainer}>
        <Button
          title={`🎯  ${t.endlessQuiz}`}
          onPress={() => navigation.navigate('GameFormatSelect', { mode: 'endless' })}
          variant="primary"
          size="large"
          style={styles.menuButton}
        />

        <Button
          title={`🏆  ${t.campaignMode}`}
          onPress={() => navigation.navigate('GameFormatSelect', { mode: 'campaign' })}
          variant="primary"
          size="large"
          style={styles.menuButton}
        />

        <Button
          title={`⚙️  ${t.settings}`}
          onPress={() => navigation.navigate('Settings')}
          variant="outline"
          size="large"
          style={styles.menuButton}
        />
      </View>

      {/* Footer */}
      <View style={styles.footer}>
        <Text style={styles.footerText}>198 Bird Species to Learn</Text>
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
    alignItems: 'center',
    paddingTop: SPACING.xxl,
    paddingBottom: SPACING.lg,
  },
  appIcon: {
    fontSize: 80,
    marginBottom: SPACING.md,
  },
  title: {
    fontSize: FONT_SIZES.xxxl,
    fontWeight: 'bold',
    color: COLORS.primaryGreen,
    marginBottom: SPACING.xs,
  },
  subtitle: {
    fontSize: FONT_SIZES.md,
    color: COLORS.textSecondary,
  },
  decoration: {
    position: 'absolute',
    top: 120,
    left: 0,
    right: 0,
    flexDirection: 'row',
    justifyContent: 'space-around',
    opacity: 0.3,
  },
  decorIcon: {
    fontSize: 30,
  },
  decorIcon2: {
    marginTop: 40,
  },
  decorIcon3: {
    marginTop: 20,
  },
  menuContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: SPACING.xl,
  },
  menuButton: {
    width: '100%',
    marginBottom: SPACING.md,
  },
  footer: {
    alignItems: 'center',
    paddingBottom: SPACING.xl,
  },
  footerText: {
    fontSize: FONT_SIZES.sm,
    color: COLORS.textSecondary,
  },
});

export default MainMenuScreen;
