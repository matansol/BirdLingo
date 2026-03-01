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
import { useLanguage } from '../context/LanguageContext';
import { Button } from '../components';

const LEVELS = [
  { level: 1, icon: '🌱', color: '#4CAF50', difficulty: 1 },
  { level: 2, icon: '🌿', color: '#8BC34A', difficulty: 2 },
  { level: 3, icon: '🌳', color: '#FF9800', difficulty: 3 },
  { level: 4, icon: '🔥', color: '#F44336', difficulty: 4 },
  { level: 5, icon: '👑', color: '#9C27B0', difficulty: 5 },
];

const getDifficultyLabel = (t, level) => {
  switch (level) {
    case 1:
      return t.easy;
    case 2:
      return t.medium;
    case 3:
      return t.hard;
    case 4:
      return t.expert;
    case 5:
      return t.master;
    default:
      return '';
  }
};

const LevelSelectScreen = ({ navigation }) => {
  const { t, getTextAlign } = useLanguage();

  const handleLevelSelect = (levelData) => {
    navigation.navigate('Quiz', {
      mode: 'campaign',
      level: levelData.level,
      category: null,
    });
  };

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar style="dark" />

      {/* Header */}
      <View style={styles.header}>
        <Text style={[styles.title, { textAlign: getTextAlign() }]}>
          {t.selectLevel}
        </Text>
        <Text style={[styles.subtitle, { textAlign: getTextAlign() }]}>
          All levels are unlocked!
        </Text>
      </View>

      {/* Levels */}
      <ScrollView
        style={styles.scrollView}
        contentContainerStyle={styles.levelsContainer}
      >
        {LEVELS.map((levelData) => (
          <TouchableOpacity
            key={levelData.level}
            style={[styles.levelCard, { borderColor: levelData.color }]}
            onPress={() => handleLevelSelect(levelData)}
            activeOpacity={0.8}
          >
            <View style={[styles.levelBadge, { backgroundColor: levelData.color }]}>
              <Text style={styles.levelNumber}>{levelData.level}</Text>
            </View>
            <View style={styles.levelInfo}>
              <Text style={[styles.levelTitle, { textAlign: getTextAlign() }]}>
                {t.level} {levelData.level}
              </Text>
              <Text style={[styles.levelDifficulty, { textAlign: getTextAlign() }]}>
                {getDifficultyLabel(t, levelData.level)}
              </Text>
            </View>
            <Text style={styles.levelIcon}>{levelData.icon}</Text>
          </TouchableOpacity>
        ))}
      </ScrollView>

      {/* Back Button */}
      <View style={styles.footer}>
        <Button
          title={t.backToMenu}
          onPress={() => navigation.goBack()}
          variant="outline"
          size="medium"
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
    fontSize: FONT_SIZES.sm,
    color: COLORS.textSecondary,
    marginTop: SPACING.xs,
  },
  scrollView: {
    flex: 1,
  },
  levelsContainer: {
    padding: SPACING.lg,
  },
  levelCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: COLORS.white,
    borderRadius: BORDER_RADIUS.lg,
    padding: SPACING.md,
    marginBottom: SPACING.md,
    borderWidth: 2,
    ...SHADOWS.small,
  },
  levelBadge: {
    width: 50,
    height: 50,
    borderRadius: 25,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: SPACING.md,
  },
  levelNumber: {
    fontSize: FONT_SIZES.xl,
    fontWeight: 'bold',
    color: COLORS.white,
  },
  levelInfo: {
    flex: 1,
  },
  levelTitle: {
    fontSize: FONT_SIZES.lg,
    fontWeight: '600',
    color: COLORS.textPrimary,
  },
  levelDifficulty: {
    fontSize: FONT_SIZES.sm,
    color: COLORS.textSecondary,
    marginTop: SPACING.xs,
  },
  levelIcon: {
    fontSize: 32,
  },
  footer: {
    padding: SPACING.lg,
    alignItems: 'center',
  },
});

export default LevelSelectScreen;
