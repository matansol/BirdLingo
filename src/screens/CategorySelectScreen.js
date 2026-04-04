import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  SafeAreaView,
  TouchableOpacity,
  ScrollView,
  Modal,
} from 'react-native';
import { StatusBar } from 'expo-status-bar';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import { COLORS, SPACING, BORDER_RADIUS, FONT_SIZES, SHADOWS } from '../theme/theme';
import { useLanguage } from '../context/LanguageContext';
import { Button } from '../components';
import { birdsWithImages, tierIds } from '../data/birdsCatalog';

const MIN_BIRDS_COUNT = 6;

const CATEGORIES = [
  { id: 'all', key: 'all', icon: 'bird', color: COLORS.primaryGreen, type: 'category' },
  { id: 'Raptor', key: 'raptor', icon: 'owl', color: '#D32F2F', type: 'category' },
  { id: 'Water Bird', key: 'waterBird', icon: 'duck', color: '#1976D2', type: 'category' },
  { id: 'Songbird', key: 'songbird', icon: 'music', color: '#7B1FA2', type: 'category' },
  { id: 'Exotic Bird', key: 'exotic', icon: 'palette', color: '#F57C00', type: 'category' },
  // Locations
  { id: 'Israel', key: 'israel', icon: 'earth', color: '#0038B8', type: 'location' },
  { id: 'Africa', key: 'africa', icon: 'earth', color: '#FFB300', type: 'location' },
  { id: 'US', key: 'us', icon: 'earth', color: '#BF0A30', type: 'location' },
  { id: 'Europe', key: 'europe', icon: 'earth', color: '#003399', type: 'location' },
  { id: 'Asia', key: 'asia', icon: 'earth', color: '#D32F2F', type: 'location' },
];

const CategorySelectScreen = ({ navigation, route }) => {
  const { t, getTextAlign } = useLanguage();
  const { mode, questionFormat } = route.params;

  const [selectedCategory, setSelectedCategory] = useState(null);
  const [modalVisible, setModalVisible] = useState(false);

  const handleCategorySelect = (category) => {
    setSelectedCategory(category);
    setModalVisible(true);
  };

  const startQuiz = (difficultyType) => {
    setModalVisible(false);
    navigation.navigate('Quiz', {
      mode,
      questionFormat,
      category: selectedCategory.id,
      filterType: selectedCategory.type || 'category',
      level: null,
      difficultyType // 'tier1' | 'tier2' | 'tier3'
    });
  };

  const isInCategory = (bird, category) => {
    if (category.id === 'all') return true;

    if (category.type === 'location') {
      return bird.locations && bird.locations.includes(category.id);
    }

    if (category.type === 'tag') {
      const tag = category.id === 'Big Bird' ? 'Big' : category.id;
      return bird.tags && bird.tags.includes(tag);
    }

    return bird.category === category.id;
  };

  const getTierCountForCategory = (tier, category) => {
    const tierSet = tierIds[tier] || new Set();
    return birdsWithImages.filter((b) => tierSet.has(b.id) && isInCategory(b, category)).length;
  };

  // Filter categories based on minimum bird count
  const filteredCategories = CATEGORIES.filter((cat) =>
    [1, 2, 3].some((tier) => getTierCountForCategory(tier, cat) >= MIN_BIRDS_COUNT)
  );

  const tierOptions = selectedCategory
    ? [
      { id: 'tier1', tier: 1, title: t.tier1Mode || 'Level 1', variant: 'primary' },
      { id: 'tier2', tier: 2, title: t.tier2Mode || 'Level 2', variant: 'secondary' },
      { id: 'tier3', tier: 3, title: t.tier3Mode || 'Level 3 (Specific Species)', variant: 'secondary' },
    ].filter((option) => getTierCountForCategory(option.tier, selectedCategory) >= MIN_BIRDS_COUNT)
    : [];

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar style="dark" />

      {/* Header */}
      <View style={styles.header}>
        <Text style={[styles.title, { textAlign: getTextAlign() }]}>
          {t.selectCategory}
        </Text>
      </View>

      {/* Categories */}
      <ScrollView
        style={styles.scrollView}
        contentContainerStyle={styles.categoriesContainer}
      >
        {filteredCategories.map((category) => (
          <TouchableOpacity
            key={category.id}
            style={[styles.categoryCard, { borderLeftColor: category.color }]}
            onPress={() => handleCategorySelect(category)}
            activeOpacity={0.8}
          >
            <MaterialCommunityIcons
              name={category.icon}
              size={40}
              color={category.color}
              style={styles.categoryIcon}
            />
            <Text style={[styles.categoryName, { textAlign: getTextAlign() }]}>
              {t[category.key]}
            </Text>
            <Text style={styles.arrow}>→</Text>
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

      {/* Difficulty Selection Modal */}
      <Modal
        animationType="fade"
        transparent={true}
        visible={modalVisible}
        onRequestClose={() => setModalVisible(false)}
      >
        <View style={styles.modalOverlay}>
          <View style={styles.modalContent}>
            <Text style={[styles.modalTitle, { textAlign: getTextAlign() }]}>
              {t.selectDifficulty}
            </Text>

            <View style={styles.modalButtons}>
              {tierOptions.map((option) => (
                <Button
                  key={option.id}
                  title={option.title}
                  onPress={() => startQuiz(option.id)}
                  variant={option.variant}
                  style={styles.modalButton}
                />
              ))}
              {tierOptions.length === 0 && (
                <Text style={[styles.noLevelsText, { textAlign: getTextAlign() }]}>
                  {t.noAvailableLevels || 'אין מספיק ציפורים בקטגוריה הזו'}
                </Text>
              )}
              <Button
                title={t.backToMenu || 'Cancel'}
                onPress={() => setModalVisible(false)}
                variant="outline"
                style={styles.modalButton}
              />
            </View>
          </View>
        </View>
      </Modal>
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
  categoriesContainer: {
    padding: SPACING.lg,
  },
  categoryCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: COLORS.white,
    borderRadius: BORDER_RADIUS.lg,
    padding: SPACING.lg,
    marginBottom: SPACING.md,
    borderLeftWidth: 4,
    ...SHADOWS.small,
  },
  categoryIcon: {
    fontSize: 40,
    marginRight: SPACING.md,
  },
  categoryName: {
    flex: 1,
    fontSize: FONT_SIZES.lg,
    fontWeight: '600',
    color: COLORS.textPrimary,
  },
  arrow: {
    fontSize: FONT_SIZES.xl,
    color: COLORS.mediumGray,
  },
  footer: {
    padding: SPACING.lg,
    alignItems: 'center',
  },
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    justifyContent: 'center',
    alignItems: 'center',
    padding: SPACING.xl,
  },
  modalContent: {
    backgroundColor: COLORS.white,
    borderRadius: BORDER_RADIUS.xl,
    padding: SPACING.xl,
    width: '100%',
    maxWidth: 400,
    alignItems: 'center',
    ...SHADOWS.large,
  },
  modalTitle: {
    fontSize: FONT_SIZES.xl,
    fontWeight: 'bold',
    color: COLORS.textPrimary,
    marginBottom: SPACING.xl,
  },
  modalButtons: {
    width: '100%',
  },
  modalButton: {
    marginBottom: SPACING.md,
  },
  noLevelsText: {
    marginBottom: SPACING.md,
    color: COLORS.textSecondary,
    fontSize: FONT_SIZES.md,
  },
});

export default CategorySelectScreen;
