import React, { useState, useEffect, useMemo, useCallback } from 'react';
import {
  View,
  Text,
  StyleSheet,
  SafeAreaView,
  TouchableOpacity,
} from 'react-native';
import { StatusBar } from 'expo-status-bar';
import { COLORS, SPACING, BORDER_RADIUS, FONT_SIZES, SHADOWS } from '../theme/theme';
import { useLanguage } from '../context/LanguageContext';
import { Button, BirdImage, SessionStats, FeedbackModal } from '../components';
import birdsData from '../../assets/birds_data.json';
import birdImages from '../../assets/birdImages';
import birdSimilarity from '../../assets/bird_similarity.json';

// Filter out birds that don't have a matching image file
const birdsWithImages = birdsData.filter((bird) => {
  const hasImage = bird.image && birdImages[bird.image];
  if (!hasImage) {
    console.warn(`[BirdLingo] Skipping bird "${bird.names?.en}" (${bird.id}) — no image found for key "${bird.image}"`);
  }
  return hasImage;
});

// Build a lookup map for quick bird access by ID
const birdById = {};
birdsWithImages.forEach((bird) => { birdById[bird.id] = bird; });

// Utility to shuffle array
const shuffleArray = (array) => {
  const shuffled = [...array];
  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
  }
  return shuffled;
};

// Get random items from array excluding certain items
const getRandomItems = (array, count, exclude = []) => {
  const filtered = array.filter((item) => !exclude.includes(item.id));
  const shuffled = shuffleArray(filtered);
  return shuffled.slice(0, count);
};

// Determine how many similar distractors to use based on mode/level
// level1,2: k=0 (all random), level3: k=1, level4: k=2, level5: k=3
// endless: k=2
const getSimilarCount = (mode, level) => {
  if (mode === 'endless') return 3;
  if (mode === 'campaign') {
    if (level <= 2) return 2;
    if (level === 3) return 2;
    if (level === 4) return 3;
    return 5; // level 5
  }
  return 0;
};

// Get wrong options: k similar + (5-k) random
const getWrongOptions = (correctBird, mode, level, excludeIds = []) => {
  const k = getSimilarCount(mode, level);
  const allExclude = [correctBird.id, ...excludeIds];
  const wrongOptions = [];

  // Pick k similar birds from the similarity map
  if (k > 0) {
    const similarIds = birdSimilarity[correctBird.id] || [];
    const availableSimilar = similarIds
      .filter((id) => !allExclude.includes(id) && birdById[id])
      .map((id) => birdById[id]);
    const shuffledSimilar = shuffleArray(availableSimilar);
    const picked = shuffledSimilar.slice(0, k);
    wrongOptions.push(...picked);
  }

  // Fill remaining slots with random birds
  const remaining = 5 - wrongOptions.length;
  const usedIds = [...allExclude, ...wrongOptions.map((b) => b.id)];
  const randomPicks = getRandomItems(birdsWithImages, remaining, usedIds);
  wrongOptions.push(...randomPicks);

  return wrongOptions;
};

const QuizScreen = ({ navigation, route }) => {
  const { mode, category, level, filterType } = route.params;
  const { t, getBirdName, getTextAlign, isRTL } = useLanguage();

  // Filter birds based on mode (only birds with valid images)
  const filteredBirds = useMemo(() => {
    let birds = [...birdsWithImages];

    if (mode === 'endless' && category && category !== 'all') {
      if (filterType === 'location') {
        birds = birds.filter((b) => b.locations && b.locations.includes(category));
      } else if (filterType === 'tag') {
        const tag = category === 'Big Bird' ? 'Big' : category;
        birds = birds.filter((b) => b.tags && b.tags.includes(tag));
      } else {
        birds = birds.filter((b) => b.category === category);
      }
    } else if (mode === 'campaign' && level) {
      birds = birds.filter((bird) => bird.difficulty === level);
    }

    return birds;
  }, [mode, category, level, filterType]);

  // State
  const [currentBird, setCurrentBird] = useState(null);
  const [options, setOptions] = useState([]);
  const [selectedOption, setSelectedOption] = useState(null);
  const [wrongGuesses, setWrongGuesses] = useState([]);
  const [showFeedback, setShowFeedback] = useState(false);
  const [isCorrect, setIsCorrect] = useState(false);
  const [stats, setStats] = useState({ correct: 0, wrong: 0 });
  const [questionIndex, setQuestionIndex] = useState(0);
  const [seenBirds, setSeenBirds] = useState([]);
  const [feedbackBird, setFeedbackBird] = useState(null);
  const [feedbackIsCorrect, setFeedbackIsCorrect] = useState(false);

  // Reset seen birds when category changes
  useEffect(() => {
    setSeenBirds([]);
    setStats({ correct: 0, wrong: 0 });
    setQuestionIndex(0);
    setCurrentBird(null);
  }, [mode, category, level, filterType]);

  // Generate a new question
  const generateQuestion = useCallback(() => {
    if (filteredBirds.length < 6) {
      console.warn('Not enough birds for quiz');
      return;
    }

    // Filter out birds that have already been correctly identified
    let availableBirds = filteredBirds.filter((bird) => !seenBirds.includes(bird.id));

    // If all birds have been seen, reset the seen list
    if (availableBirds.length === 0) {
      availableBirds = filteredBirds;
      setSeenBirds([]);
    }

    if (availableBirds.length === 0) {
      console.warn('No birds available even after reset');
      return;
    }

    // Pick a random bird as the correct answer
    const randomIndex = Math.floor(Math.random() * availableBirds.length);
    const correctBird = availableBirds[randomIndex];

    // Pick a random image index for this bird
    const imageCount = correctBird.images?.length || 1;
    const randomImageIndex = Math.floor(Math.random() * imageCount);
    const birdWithImageIndex = { ...correctBird, imageIndex: randomImageIndex };

    // Get 5 wrong options: k similar + (5-k) random
    const wrongOptions = getWrongOptions(correctBird, mode, level);

    // Combine and shuffle options
    const allOptions = shuffleArray([birdWithImageIndex, ...wrongOptions]);

    setCurrentBird(birdWithImageIndex);
    setOptions(allOptions);
    setSelectedOption(null);
    setWrongGuesses([]);
    setShowFeedback(false);
    setIsCorrect(false);
  }, [filteredBirds, seenBirds]);

  // Initialize first question
  useEffect(() => {
    if (!currentBird) {
      generateQuestion();
    }
  }, [generateQuestion, currentBird]);

  // Handle option selection
  const handleOptionSelect = (option) => {
    if (showFeedback) return; // Prevent clicks during feedback
    if (wrongGuesses.includes(option.id)) return; // Already guessed wrong

    const correct = option.id === currentBird.id;

    if (correct) {
      setSelectedOption(option);
      setIsCorrect(true);

      // Update stats: correct only if no wrong guesses yet
      if (wrongGuesses.length === 0) {
        setStats((prev) => ({ ...prev, correct: prev.correct + 1 }));
      }

      // Add to seen list
      setSeenBirds((prev) => [...prev, currentBird.id]);

      // Set feedback bird to stable current bird for the modal
      setFeedbackBird(currentBird);
      setFeedbackIsCorrect(true);

      // Show feedback after a brief delay
      setTimeout(() => {
        setShowFeedback(true);
      }, 300);
    } else {
      // Wrong guess
      if (!wrongGuesses.includes(option.id)) {
        setWrongGuesses((prev) => [...prev, option.id]);

        // Update stats: wrong only if this is the first wrong guess
        if (wrongGuesses.length === 0) {
          setStats((prev) => ({ ...prev, wrong: prev.wrong + 1 }));
        }
      }
    }
  };

  // Handle next question
  const handleNext = () => {
    setShowFeedback(false);
    setQuestionIndex((prev) => prev + 1);
    generateQuestion();
  };

  // Get button style based on selection state
  const getOptionStyle = (option) => {
    // If feedback is showing (round over)
    if (showFeedback) {
      if (option.id === currentBird.id) {
        return [styles.optionButton, styles.correctOption];
      }
      if (option.id === selectedOption?.id && option.id !== currentBird.id) {
        return [styles.optionButton, styles.wrongOption];
      }
      return [styles.optionButton, styles.disabledOption];
    }

    // During active guessing
    if (wrongGuesses.includes(option.id)) {
      return [styles.optionButton, styles.wrongOption];
    }

    return styles.optionButton;
  };

  const getOptionTextStyle = (option) => {
    // If feedback is showing
    if (showFeedback) {
      if (option.id === currentBird.id) {
        return [styles.optionText, styles.correctOptionText, { textAlign: getTextAlign() }];
      }
      if (option.id === selectedOption?.id && option.id !== currentBird.id) {
        return [styles.optionText, styles.wrongOptionText, { textAlign: getTextAlign() }];
      }
      return [styles.optionText, styles.disabledOptionText, { textAlign: getTextAlign() }];
    }

    // During active guessing
    if (wrongGuesses.includes(option.id)) {
      return [styles.optionText, styles.wrongOptionText, { textAlign: getTextAlign() }];
    }

    return [styles.optionText, { textAlign: getTextAlign() }];
  };

  if (!currentBird) {
    const notEnough = filteredBirds.length < 6;
    return (
      <SafeAreaView style={styles.container}>
        <Text style={styles.loadingText}>
          {notEnough
            ? `Not enough birds in this category (${filteredBirds.length} found, need 6). Try a different category.`
            : 'Loading...'}
        </Text>
        {notEnough && (
          <TouchableOpacity
            onPress={() => navigation.goBack()}
            style={{ alignSelf: 'center', marginTop: 20, padding: 12 }}
          >
            <Text style={{ color: COLORS.primaryGreen, fontSize: 16, fontWeight: '600' }}>
              ← {t.backToMenu}
            </Text>
          </TouchableOpacity>
        )}
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar style="dark" />

      {/* Header with Stats */}
      <View style={styles.header}>
        <TouchableOpacity
          onPress={() => navigation.goBack()}
          style={styles.backButton}
        >
          <Text style={styles.backButtonText}>← {t.backToMenu}</Text>
        </TouchableOpacity>
        <SessionStats correct={stats.correct} wrong={stats.wrong} />
      </View>

      {/* Question */}
      <View style={styles.questionContainer}>
        <Text style={[styles.questionText, { textAlign: getTextAlign() }]}>
          {t.whatBird}
        </Text>
      </View>

      {/* Bird Image */}
      <View style={styles.imageContainer}>
        <BirdImage bird={currentBird} size="large" imageIndex={Number(currentBird.imageIndex) || 0} />
      </View>

      {/* Options */}
      <View style={styles.optionsContainer}>
        {options.map((option, index) => (
          <TouchableOpacity
            key={option.id}
            style={getOptionStyle(option)}
            onPress={() => handleOptionSelect(option)}
            disabled={showFeedback || wrongGuesses.includes(option.id)}
            activeOpacity={0.8}
          >
            <Text style={getOptionTextStyle(option)} numberOfLines={2}>
              {getBirdName(option)}
            </Text>
          </TouchableOpacity>
        ))}
      </View>

      {/* Feedback Modal */}
      <FeedbackModal
        visible={showFeedback}
        isCorrect={feedbackIsCorrect}
        correctBird={feedbackBird || currentBird}
        selectedBird={selectedOption}
        onNext={handleNext}
      />
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  loadingText: {
    fontSize: FONT_SIZES.lg,
    color: COLORS.textSecondary,
    textAlign: 'center',
    marginTop: SPACING.xxl,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: SPACING.md,
    paddingTop: SPACING.md,
    paddingBottom: SPACING.sm,
  },
  backButton: {
    padding: SPACING.sm,
  },
  backButtonText: {
    fontSize: FONT_SIZES.sm,
    color: COLORS.primaryGreen,
    fontWeight: '600',
  },
  questionContainer: {
    paddingHorizontal: SPACING.lg,
    paddingBottom: SPACING.md,
  },
  questionText: {
    fontSize: FONT_SIZES.xl,
    fontWeight: 'bold',
    color: COLORS.textPrimary,
  },
  imageContainer: {
    alignItems: 'center',
    paddingVertical: SPACING.md,
  },
  optionsContainer: {
    flex: 1,
    paddingHorizontal: SPACING.lg,
    paddingTop: SPACING.md,
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
  },
  optionButton: {
    width: '48%',
    backgroundColor: COLORS.white,
    borderRadius: BORDER_RADIUS.lg,
    padding: SPACING.md,
    marginBottom: SPACING.md,
    minHeight: 70,
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 2,
    borderColor: COLORS.white,
    ...SHADOWS.small,
  },
  optionText: {
    fontSize: FONT_SIZES.md,
    fontWeight: '600',
    color: COLORS.textPrimary,
    textAlign: 'center',
  },
  correctOption: {
    backgroundColor: COLORS.successLight,
    borderColor: COLORS.success,
  },
  correctOptionText: {
    color: COLORS.success,
  },
  wrongOption: {
    backgroundColor: COLORS.errorLight,
    borderColor: COLORS.error,
  },
  wrongOptionText: {
    color: COLORS.error,
  },
  disabledOption: {
    opacity: 0.5,
  },
  disabledOptionText: {
    color: COLORS.textSecondary,
  },
});

export default QuizScreen;
