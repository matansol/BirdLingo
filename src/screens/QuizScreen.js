import React, { useState, useEffect, useMemo, useCallback } from 'react';
import {
  View,
  Text,
  StyleSheet,
  SafeAreaView,
  TouchableOpacity,
  TextInput,
  KeyboardAvoidingView,
  Platform,
} from 'react-native';
import { StatusBar } from 'expo-status-bar';
import { COLORS, SPACING, BORDER_RADIUS, FONT_SIZES, SHADOWS } from '../theme/theme';
import { useLanguage } from '../context/LanguageContext';
import { useProgress } from '../context/ProgressContext';
import { Button, BirdImage, SessionStats, FeedbackModal } from '../components';
import { birdsWithImages, birdById, tierIds } from '../data/birdsCatalog';
import birdSimilarity from '../../assets/bird_similarity.json';

const TYPE_NAME_MAX_ATTEMPTS = 5;

const normalizeAnswer = (value = '') => value
  .toString()
  .trim()
  .toLowerCase()
  .normalize('NFD')
  .replace(/[\u0300-\u036f]/g, '')
  .replace(/[^\p{L}\p{N}\s-]/gu, ' ')
  .replace(/\s+/g, ' ')
  .trim();

const buildCharNgramEmbedding = (value = '', minN = 2, maxN = 3) => {
  const text = normalizeAnswer(value).replace(/\s+/g, '');
  const vector = new Map();

  if (!text) return vector;

  for (let n = minN; n <= maxN; n += 1) {
    if (text.length < n) continue;
    for (let i = 0; i <= text.length - n; i += 1) {
      const gram = text.slice(i, i + n);
      vector.set(gram, (vector.get(gram) || 0) + 1);
    }
  }

  return vector;
};

const cosineSimilarity = (a, b) => {
  if (!a.size || !b.size) return 0;

  let dot = 0;
  let normA = 0;
  let normB = 0;

  a.forEach((value, key) => {
    normA += value * value;
    dot += value * (b.get(key) || 0);
  });

  b.forEach((value) => {
    normB += value * value;
  });

  const denom = Math.sqrt(normA) * Math.sqrt(normB);
  return denom === 0 ? 0 : dot / denom;
};

const isCloseEnoughGuess = (guess, answer) => {
  const normalizedGuess = normalizeAnswer(guess);
  const normalizedAnswer = normalizeAnswer(answer);

  if (!normalizedGuess || !normalizedAnswer) return false;
  if (normalizedGuess === normalizedAnswer) return true;

  const answerTokens = normalizedAnswer.split(' ').filter(Boolean);
  const firstToken = answerTokens[0] || '';

  // Accept leading part of the official name, but not trailing words alone.
  // Example: "בז" should match "בז מצוי", but "מצוי" should not.
  if (firstToken && normalizedGuess === firstToken) return true;
  if (normalizedAnswer.startsWith(`${normalizedGuess} `) && normalizedGuess.length >= 2) return true;

  // Allow close-enough typo tolerance on first token (short single-word guess)
  if (firstToken && !normalizedGuess.includes(' ') && normalizedGuess.length >= 2) {
    const guessVecFirst = buildCharNgramEmbedding(normalizedGuess);
    const firstVec = buildCharNgramEmbedding(firstToken);
    if (cosineSimilarity(guessVecFirst, firstVec) >= 0.78) return true;
  }

  const guessVec = buildCharNgramEmbedding(normalizedGuess);
  const answerVec = buildCharNgramEmbedding(normalizedAnswer);
  const similarity = cosineSimilarity(guessVec, answerVec);

  // Slightly stricter for very short words to avoid false positives
  const minLen = Math.min(normalizedGuess.length, normalizedAnswer.length);
  const threshold = minLen <= 4 ? 0.86 : 0.74;

  return similarity >= threshold;
};

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

// Determine how many similar distractors to use by selected tier
const getSimilarCount = (difficultyType) => {
  if (difficultyType === 'tier3') return 3;
  return 2;
};

// Get wrong options: k similar + (5-k) random
const getWrongOptions = (correctBird, difficultyType, availablePool, excludeIds = []) => {
  const k = getSimilarCount(difficultyType);
  const allExclude = [correctBird.id, ...excludeIds];
  const wrongOptions = [];

  // Pick k similar birds from the similarity map (only if they exist in the available pool)
  if (k > 0) {
    const similarIds = birdSimilarity[correctBird.id] || [];
    const availableSimilar = similarIds
      .filter((id) => !allExclude.includes(id) && availablePool.find(b => b.id === id))
      .map((id) => birdById[id]);
    const shuffledSimilar = shuffleArray(availableSimilar);
    const picked = shuffledSimilar.slice(0, k);
    wrongOptions.push(...picked);
  }

  // Fill remaining slots with random birds from the SAME pool
  const remaining = 5 - wrongOptions.length;
  const usedIds = [...allExclude, ...wrongOptions.map((b) => b.id)];
  const randomPicks = getRandomItems(availablePool, remaining, usedIds);
  wrongOptions.push(...randomPicks);

  return wrongOptions;
};

const QuizScreen = ({ navigation, route }) => {
  const { category, filterType, questionFormat = 'classic', difficultyType } = route.params;
  const { t, getBirdName, getTextAlign } = useLanguage();
  const {
    isLoaded,
    getBirdProgress,
    recordCorrectChoice,
    recordCorrectTyped,
    recordWrong,
  } = useProgress();

  // Filter birds (only birds with valid images)
  const filteredBirds = useMemo(() => {
    let birds = [...birdsWithImages];

    if (difficultyType === 'tier1') {
      birds = birds.filter((b) => tierIds[1].has(b.id));
    } else if (difficultyType === 'tier2') {
      birds = birds.filter((b) => tierIds[2].has(b.id));
    } else if (difficultyType === 'tier3') {
      birds = birds.filter((b) => tierIds[3].has(b.id));
    }

    if (category && category !== 'all') {
      if (filterType === 'location') {
        birds = birds.filter((b) => b.locations && b.locations.includes(category));
      } else if (filterType === 'tag') {
        const tag = category === 'Big Bird' ? 'Big' : category;
        birds = birds.filter((b) => b.tags && b.tags.includes(tag));
      } else {
        birds = birds.filter((b) => b.category === category);
      }
    }

    return birds;
  }, [category, filterType, difficultyType]);

  // State
  const [currentBird, setCurrentBird] = useState(null);
  const [options, setOptions] = useState([]);
  const [selectedOption, setSelectedOption] = useState(null);
  const [wrongGuesses, setWrongGuesses] = useState([]);
  const [showFeedback, setShowFeedback] = useState(false);
  const [isCorrect, setIsCorrect] = useState(false);
  const [stats, setStats] = useState({ correct: 0, wrong: 0 });
  const [questionIndex, setQuestionIndex] = useState(0);
  const [feedbackBird, setFeedbackBird] = useState(null);
  const [feedbackIsCorrect, setFeedbackIsCorrect] = useState(false);
  const [activeFormat, setActiveFormat] = useState('classic');
  const [textInput, setTextInput] = useState('');
  const [typeAttempts, setTypeAttempts] = useState(0);

  // Reset seen birds when category changes
  useEffect(() => {
    setStats({ correct: 0, wrong: 0 });
    setQuestionIndex(0);
    setCurrentBird(null);
    setTypeAttempts(0);
  }, [category, filterType, difficultyType]);

  const revealTypeAnswerAsWrong = useCallback(() => {
    if (!currentBird || showFeedback) return;

    setIsCorrect(false);
    setStats((prev) => ({ ...prev, wrong: prev.wrong + 1 }));
    setFeedbackBird(currentBird);
    setFeedbackIsCorrect(false);
    setShowFeedback(true);
  }, [currentBird, showFeedback]);

  // Generate a new question
  const generateQuestion = useCallback(() => {
    if (filteredBirds.length < 6) {
      console.warn('Not enough birds for quiz');
      return;
    }

    let availableBirds = [...filteredBirds];

    // Avoid immediate repeats when possible
    if (currentBird && availableBirds.length > 1) {
      availableBirds = availableBirds.filter((bird) => bird.id !== currentBird.id);
    }

    if (availableBirds.length === 0) {
      console.warn('No birds available even after reset');
      return;
    }

    const unrecognizedBirds = availableBirds.filter((bird) => !getBirdProgress(bird.id).recognized);
    const recognizedBirds = availableBirds.filter((bird) => getBirdProgress(bird.id).recognized);

    let weightedPool = availableBirds;
    if (unrecognizedBirds.length > 0 && recognizedBirds.length > 0) {
      weightedPool = Math.random() < 0.8 ? unrecognizedBirds : recognizedBirds;
    } else if (unrecognizedBirds.length > 0) {
      weightedPool = unrecognizedBirds;
    } else if (recognizedBirds.length > 0) {
      weightedPool = recognizedBirds;
    }

    const randomIndex = Math.floor(Math.random() * weightedPool.length);
    const correctBird = weightedPool[randomIndex];

    // Pick a random image index for this bird
    // For groups, we might have multiple images. 
    const imageCount = correctBird.images?.length || 1;
    const randomImageIndex = Math.floor(Math.random() * imageCount);
    const birdWithImageIndex = { ...correctBird, imageIndex: randomImageIndex };

    // Get wrong options from the filtered pool so classes (groups vs species) don't mix
    const wrongOptions = getWrongOptions(correctBird, difficultyType, filteredBirds);

    // Combine and shuffle options
    const allOptions = shuffleArray([birdWithImageIndex, ...wrongOptions]);

    // Choose what the format will be
    let nextFormat = questionFormat;
    if (nextFormat === 'mixed') {
      const formats = ['classic', 'find_image', 'type_name'];
      nextFormat = formats[Math.floor(Math.random() * formats.length)];
    }

    // In find_image, we need 4 options not 6, so slice them
    const finalOptions = nextFormat === 'find_image'
      ? shuffleArray([birdWithImageIndex, ...wrongOptions.slice(0, 3)])
      : allOptions;

    setCurrentBird(birdWithImageIndex);
    setOptions(finalOptions);
    setSelectedOption(null);
    setWrongGuesses([]);
    setShowFeedback(false);
    setIsCorrect(false);
    setActiveFormat(nextFormat);
    setTextInput('');
    setTypeAttempts(0);
  }, [filteredBirds, currentBird, questionFormat, difficultyType, getBirdProgress]);

  // Initialize first question
  useEffect(() => {
    if (!isLoaded) return;
    if (!currentBird) {
      generateQuestion();
    }
  }, [generateQuestion, currentBird, isLoaded]);

  // Handle option selection
  const handleOptionSelect = (option) => {
    if (showFeedback) return; // Prevent clicks during feedback
    if (wrongGuesses.includes(option.id)) return; // Already guessed wrong

    const correct = option.id === currentBird.id;

    if (correct) {
      setSelectedOption(option);
      setIsCorrect(true);
      recordCorrectChoice(currentBird.id);

      // Update stats: correct only if no wrong guesses yet
      if (wrongGuesses.length === 0) {
        setStats((prev) => ({ ...prev, correct: prev.correct + 1 }));
      }

      // Set feedback bird to stable current bird for the modal
      setFeedbackBird(currentBird);
      setFeedbackIsCorrect(true);

      // Show feedback after a brief delay
      setTimeout(() => {
        setShowFeedback(true);
      }, 300);
    } else {
      recordWrong(currentBird.id);

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

  // Handle text input submission for type_name format
  const handleTypeSubmit = () => {
    if (showFeedback || !currentBird || !textInput.trim()) return;

    const nextAttempts = typeAttempts + 1;
    setTypeAttempts(nextAttempts);

    const correctName = getBirdName(currentBird);
    const guessedName = textInput;
    const closeEnough = isCloseEnoughGuess(guessedName, correctName);

    if (closeEnough) {
      setIsCorrect(true);
      recordCorrectTyped(currentBird.id);
      setStats((prev) => ({ ...prev, correct: prev.correct + 1 }));
      setFeedbackBird(currentBird);
      setFeedbackIsCorrect(true);
      setTimeout(() => {
        setShowFeedback(true);
      }, 300);
      return;
    }

    recordWrong(currentBird.id);

    if (nextAttempts >= TYPE_NAME_MAX_ATTEMPTS) {
      revealTypeAnswerAsWrong();
      return;
    } else {
      setWrongGuesses(['typed_wrong']); // visual hint while user still has attempts
    }
  };

  const handleIDontKnow = () => {
    if (showFeedback || !currentBird) return;
    setTypeAttempts((prev) => Math.min(prev + 1, TYPE_NAME_MAX_ATTEMPTS));
    recordWrong(currentBird.id);
    revealTypeAnswerAsWrong();
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
          {!isLoaded
            ? 'Loading progress...'
            : notEnough
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
          {activeFormat === 'find_image'
            ? `${t.whichImage} ${getBirdName(currentBird)}?`
            : t.whatBird}
        </Text>
      </View>

      {/* Main Content Area */}
      {activeFormat === 'find_image' ? (
        <View style={styles.imageGridContainer}>
          {options.map((option) => (
            <TouchableOpacity
              key={option.id}
              style={[
                styles.imageOptionWrapper,
                showFeedback && option.id === currentBird.id && styles.correctImageBorder,
                showFeedback && option.id === selectedOption?.id && option.id !== currentBird.id && styles.wrongImageBorder,
                !showFeedback && wrongGuesses.includes(option.id) && styles.wrongImageBorder,
                (showFeedback || wrongGuesses.includes(option.id)) && option.id !== currentBird.id && styles.disabledOption,
              ]}
              onPress={() => handleOptionSelect(option)}
              disabled={showFeedback || wrongGuesses.includes(option.id)}
              activeOpacity={0.8}
            >
              <BirdImage
                bird={option}
                size="medium"
                imageIndex={Number(option.imageIndex) || 0}
                disableInteractions={true}
              />
            </TouchableOpacity>
          ))}
        </View>
      ) : (
        <>
          {/* Bird Image */}
          <View style={styles.imageContainer}>
            <BirdImage bird={currentBird} size="large" imageIndex={Number(currentBird.imageIndex) || 0} />
          </View>

          {/* Options or Text Input */}
          {activeFormat === 'type_name' ? (
            <KeyboardAvoidingView
              behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
              style={styles.keyboardView}
            >
              <View style={styles.typeInputContainer}>
                <TextInput
                  style={[
                    styles.textInput,
                    { textAlign: getTextAlign() },
                    typeAttempts > 0 && !showFeedback && styles.wrongInput
                  ]}
                  value={textInput}
                  onChangeText={setTextInput}
                  placeholder={t.typeBirdName}
                  placeholderTextColor={COLORS.textSecondary}
                  editable={!showFeedback}
                  onSubmitEditing={handleTypeSubmit}
                  returnKeyType="done"
                  autoCapitalize="none"
                  autoCorrect={false}
                />
                <Button
                  title={t.submit}
                  onPress={handleTypeSubmit}
                  variant="primary"
                  size="large"
                  disabled={showFeedback || !textInput.trim()}
                  style={styles.submitButton}
                />
                <Button
                  title={t.iDontKnow || "I don't know"}
                  onPress={handleIDontKnow}
                  variant="outline"
                  size="large"
                  disabled={showFeedback}
                  style={styles.submitButton}
                />
                <Text style={styles.attemptsText}>
                  {(t.attemptsLeft || 'Attempts left')}: {Math.max(0, TYPE_NAME_MAX_ATTEMPTS - typeAttempts)}
                </Text>
              </View>
            </KeyboardAvoidingView>
          ) : (
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
          )}
        </>
      )}

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
  imageGridContainer: {
    flex: 1,
    paddingHorizontal: SPACING.md,
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-around',
    alignItems: 'center',
    paddingBottom: SPACING.xl,
  },
  imageOptionWrapper: {
    padding: 4,
    borderRadius: BORDER_RADIUS.large + 4,
    borderWidth: 4,
    borderColor: 'transparent',
    marginBottom: SPACING.lg,
  },
  correctImageBorder: {
    borderColor: COLORS.success,
  },
  wrongImageBorder: {
    borderColor: COLORS.error,
  },
  keyboardView: {
    flex: 1,
    width: '100%',
  },
  typeInputContainer: {
    paddingHorizontal: SPACING.lg,
    paddingTop: SPACING.md,
    flex: 1,
    alignItems: 'center',
  },
  textInput: {
    width: '100%',
    backgroundColor: COLORS.white,
    borderRadius: BORDER_RADIUS.md,
    padding: SPACING.md,
    fontSize: FONT_SIZES.lg,
    color: COLORS.textPrimary,
    borderWidth: 2,
    borderColor: COLORS.mediumGray,
    marginBottom: SPACING.lg,
    ...SHADOWS.small,
  },
  wrongInput: {
    borderColor: COLORS.error,
    backgroundColor: COLORS.errorLight,
  },
  submitButton: {
    width: '100%',
  },
  attemptsText: {
    marginTop: SPACING.sm,
    fontSize: FONT_SIZES.sm,
    color: COLORS.textSecondary,
    textAlign: 'center',
  },
});

export default QuizScreen;
