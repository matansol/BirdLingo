import React, {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
} from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { getTierBirdIds } from '../data/birdsCatalog';

const STORAGE_KEY = 'birdlingo_progress_v1';
const RECOGNIZED_STREAK = 3;

const ProgressContext = createContext();

const normalizeProgress = (rawProgress) => {
  if (!rawProgress || typeof rawProgress !== 'object') return {};

  const normalized = {};
  Object.entries(rawProgress).forEach(([birdId, value]) => {
    const streak = Math.max(0, Number(value?.streak) || 0);
    normalized[birdId] = {
      streak,
      recognized: streak >= RECOGNIZED_STREAK,
    };
  });

  return normalized;
};

export const ProgressProvider = ({ children }) => {
  const [progress, setProgress] = useState({});
  const [isLoaded, setIsLoaded] = useState(false);

  useEffect(() => {
    let isMounted = true;

    const loadProgress = async () => {
      try {
        const raw = await AsyncStorage.getItem(STORAGE_KEY);
        if (!isMounted) return;

        if (!raw) {
          setProgress({});
        } else {
          const parsed = JSON.parse(raw);
          setProgress(normalizeProgress(parsed));
        }
      } catch (error) {
        console.warn('[BirdLingo] Failed to load progress from storage:', error);
        if (isMounted) {
          setProgress({});
        }
      } finally {
        if (isMounted) {
          setIsLoaded(true);
        }
      }
    };

    loadProgress();

    return () => {
      isMounted = false;
    };
  }, []);

  useEffect(() => {
    if (!isLoaded) return;

    AsyncStorage.setItem(STORAGE_KEY, JSON.stringify(progress)).catch((error) => {
      console.warn('[BirdLingo] Failed to save progress to storage:', error);
    });
  }, [progress, isLoaded]);

  const getBirdProgress = useCallback(
    (birdId) => progress[birdId] || { streak: 0, recognized: false },
    [progress]
  );

  const updateBirdStreak = useCallback((birdId, delta) => {
    if (!birdId) return;

    setProgress((prev) => {
      const currentStreak = Math.max(0, Number(prev[birdId]?.streak) || 0);
      const nextStreak = Math.max(0, currentStreak + delta);

      return {
        ...prev,
        [birdId]: {
          streak: nextStreak,
          recognized: nextStreak >= RECOGNIZED_STREAK,
        },
      };
    });
  }, []);

  const recordCorrectChoice = useCallback((birdId) => {
    updateBirdStreak(birdId, 1);
  }, [updateBirdStreak]);

  const recordCorrectTyped = useCallback((birdId) => {
    updateBirdStreak(birdId, 2);
  }, [updateBirdStreak]);

  const recordWrong = useCallback((birdId) => {
    updateBirdStreak(birdId, -2);
  }, [updateBirdStreak]);

  const resetTier = useCallback((tier) => {
    const tierBirdIds = getTierBirdIds(tier);

    setProgress((prev) => {
      if (!tierBirdIds.length) return prev;
      const next = { ...prev };
      tierBirdIds.forEach((birdId) => {
        delete next[birdId];
      });
      return next;
    });
  }, []);

  const tierStats = useMemo(() => {
    const createTierStat = (tier) => {
      const tierBirdIds = getTierBirdIds(tier);
      const total = tierBirdIds.length;
      const recognized = tierBirdIds.reduce((count, birdId) => {
        return count + (progress[birdId]?.recognized ? 1 : 0);
      }, 0);

      const percentage = total > 0 ? Math.round((recognized / total) * 100) : 0;

      return {
        total,
        recognized,
        percentage,
      };
    };

    return {
      1: createTierStat(1),
      2: createTierStat(2),
      3: createTierStat(3),
    };
  }, [progress]);

  const value = {
    progress,
    isLoaded,
    getBirdProgress,
    recordCorrectChoice,
    recordCorrectTyped,
    recordWrong,
    resetTier,
    tierStats,
  };

  return (
    <ProgressContext.Provider value={value}>
      {children}
    </ProgressContext.Provider>
  );
};

export const useProgress = () => {
  const context = useContext(ProgressContext);

  if (!context) {
    throw new Error('useProgress must be used within ProgressProvider');
  }

  return context;
};
