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
import { MaterialCommunityIcons } from '@expo/vector-icons';
import { COLORS, SPACING, BORDER_RADIUS, FONT_SIZES, SHADOWS } from '../theme/theme';
import { useLanguage } from '../context/LanguageContext';
import { Button } from '../components';

import birdsData from '../../assets/birds_data.json';

const MIN_BIRDS_COUNT = 10;

const CATEGORIES = [
  { id: 'all', key: 'all', icon: 'bird', color: COLORS.primaryGreen, type: 'category' },
  { id: 'Raptor', key: 'raptor', icon: 'owl', color: '#D32F2F', type: 'category' },
  { id: 'Water Bird', key: 'waterBird', icon: 'duck', color: '#1976D2', type: 'category' },
  { id: 'Songbird', key: 'songbird', icon: 'music', color: '#7B1FA2', type: 'category' },
  { id: 'Exotic Bird', key: 'exotic', icon: 'palette', color: '#F57C00', type: 'category' },
  // { id: 'Game Bird', key: 'gameBird', icon: 'feather', color: '#795548', type: 'category' }, // Removed
  { id: 'Big Bird', key: 'bigBird', icon: 'image-size-select-actual', color: '#795548', type: 'tag' }, // Added Big Bird
  // Locations
  { id: 'Israel', key: 'israel', icon: 'earth', color: '#0038B8', type: 'location' },
  { id: 'Africa', key: 'africa', icon: 'earth', color: '#FFB300', type: 'location' },
  { id: 'US', key: 'us', icon: 'earth', color: '#BF0A30', type: 'location' },
  { id: 'Europe', key: 'europe', icon: 'earth', color: '#003399', type: 'location' },
  { id: 'Asia', key: 'asia', icon: 'earth', color: '#D32F2F', type: 'location' },
];

const CategorySelectScreen = ({ navigation, route }) => {
  const { t, getTextAlign } = useLanguage();
  const { mode } = route.params;

  const handleCategorySelect = (category) => {
    navigation.navigate('Quiz', {
      mode,
      category: category.id,
      filterType: category.type || 'category',
      level: null
    });
  };

  // Filter categories based on minimum bird count
  const filteredCategories = CATEGORIES.filter(cat => {
    if (cat.id === 'all') return true;

    let count = 0;
    if (cat.type === 'location') {
      count = birdsData.filter(b => b.locations && b.locations.includes(cat.id)).length;
    } else if (cat.type === 'tag') {
      // Filter by tag (e.g. "Big")
      // cat.id is "Big Bird", but tag is "Big"
      // Or I can map "Big Bird" -> "Big"
      const tag = cat.id === 'Big Bird' ? 'Big' : cat.id;
      count = birdsData.filter(b => b.tags && b.tags.includes(tag)).length;
    } else {
      count = birdsData.filter(b => b.category === cat.id).length;
    }
    return count >= MIN_BIRDS_COUNT;
  });

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
});

export default CategorySelectScreen;
