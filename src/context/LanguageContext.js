import React, { createContext, useContext, useState } from 'react';

const LanguageContext = createContext();

export const LANGUAGES = {
  en: {
    code: 'en',
    name: 'English',
    nativeName: 'English',
    isRTL: false,
  },
  he: {
    code: 'he',
    name: 'Hebrew',
    nativeName: 'עברית',
    isRTL: true,
  },
  es: {
    code: 'es',
    name: 'Spanish',
    nativeName: 'Español',
    isRTL: false,
  },
};

// Translation strings for UI
export const TRANSLATIONS = {
  en: {
    appTitle: 'BirdLingo',
    endlessQuiz: 'Birds',
    settings: 'Settings',
    selectCategory: 'Select Category',
    all: 'All Birds',
    predator: 'Predators',
    raptor: 'Raptors',
    waterBird: 'Water Birds',
    songbird: 'Songbirds',
    exotic: 'Exotic Birds',
    gameBird: 'Game Birds',
    bigBird: 'Big Birds',
    other: 'Other',
    // Locations
    israel: 'Israel',
    africa: 'Africa',
    us: 'United States',
    europe: 'Europe',
    asia: 'Asia',
    startQuiz: 'Start Quiz',
    correct: 'Correct',
    wrong: 'Wrong',
    next: 'Next',
    backToMenu: 'Back to Menu',
    level: 'Level',
    selectLevel: 'Select Level',
    difficulty: 'Difficulty',
    language: 'Language',
    chooseLanguage: 'Choose Language',
    sessionStats: 'Session Stats',
    correctAnswer: 'Correct Answer',
    yourAnswer: 'Your Answer',
    great: 'Great!',
    tryAgain: 'Incorrect',
    whatBird: 'What bird is this?',
    easy: 'Easy',
    medium: 'Medium',
    hard: 'Hard',
    expert: 'Expert',
    master: 'Master',
    // New Game Modes
    gameFormat: 'Game Format',
    classic: 'Classic (Guess Name)',
    findImage: 'Find the Image',
    typeName: 'Type the Name',
    mixed: 'Mixed Practice',
    typeBirdName: 'Type bird name here...',
    submit: 'Submit',
    iDontKnow: "I don't know",
    attemptsLeft: 'Attempts left',
    birdName: 'Bird',
    whichImage: 'Which image is the',
    // New Levels & Difficulty
    level1Title: 'Common Bird Groups',
    level2Title: 'Less Common Bird Groups',
    level3Title: 'Specific Species',
    level4Title: 'Specific Species',
    beginnerMode: 'Beginner',
    advancedMode: 'Advanced (Species)',
    tier1Mode: 'Level 1',
    tier2Mode: 'Level 2',
    tier3Mode: 'Level 3 (Specific Species)',
    selectDifficulty: 'Select Difficulty',
    noAvailableLevels: 'Not enough birds in this category',
    statistics: 'Statistics',
    statisticsSubtitle: 'Recognition progress by tier',
    birdsRecognized: 'birds recognized',
    viewStatistics: 'View Statistics',
    resetTier: 'Reset Tier',
    resetTierConfirm: 'Reset progress for tier',
    cancel: 'Cancel',
    reset: 'Reset',
    loadingProgress: 'Loading progress...',
  },
  he: {
    appTitle: 'BirdLingo',
    endlessQuiz: 'ציפורים',
    settings: 'הגדרות',
    selectCategory: 'בחר קטגוריה',
    all: 'כל הציפורים',
    predator: 'טורפים',
    raptor: 'דורסים',
    waterBird: 'ציפורי מים',
    songbird: 'ציפורי שיר',
    exotic: 'ציפורים אקזוטיות',
    gameBird: 'עופות ציד',
    bigBird: 'ציפורים גדולות',
    other: 'אחר',
    // Locations
    israel: 'ישראל',
    africa: 'אפריקה',
    us: 'ארצות הברית',
    europe: 'אירופה',
    asia: 'אסיה',
    startQuiz: 'התחל חידון',
    correct: 'נכון',
    wrong: 'שגוי',
    next: 'הבא',
    backToMenu: 'חזרה לתפריט',
    level: 'שלב',
    selectLevel: 'בחר שלב',
    difficulty: 'קושי',
    language: 'שפה',
    chooseLanguage: 'בחר שפה',
    sessionStats: 'סטטיסטיקה',
    correctAnswer: 'תשובה נכונה',
    yourAnswer: 'התשובה שלך',
    great: 'מצוין!',
    tryAgain: 'טעות',
    whatBird: 'איזו ציפור זו?',
    easy: 'קל',
    medium: 'בינוני',
    hard: 'קשה',
    expert: 'מומחה',
    master: 'אמן',
    // New Game Modes
    gameFormat: 'פורמט משחק',
    classic: 'קלאסי (נחש את השם)',
    findImage: 'מצא את התמונה',
    typeName: 'הקלד את השם',
    mixed: 'תרגול מעורב',
    typeBirdName: 'הקלד את שם הציפור כאן...',
    submit: 'אישור',
    iDontKnow: 'לא יודע/ת',
    attemptsLeft: 'ניסיונות שנותרו',
    birdName: 'ציפור',
    whichImage: 'איזו תמונה היא של',
    // New Levels & Difficulty
    level1Title: 'קבוצות ציפורים מוכרות',
    level2Title: 'קבוצות ציפורים פחות מוכרות',
    level3Title: 'מינים ספציפיים',
    level4Title: 'מינים ספציפיים',
    beginnerMode: 'מתחילים',
    advancedMode: 'מתקדמים (מינים)',
    tier1Mode: 'רמה 1',
    tier2Mode: 'רמה 2',
    tier3Mode: 'רמה 3 (מינים ספציפיים)',
    selectDifficulty: 'בחר רמת קושי',
    noAvailableLevels: 'אין מספיק ציפורים בקטגוריה הזו',
    statistics: 'סטטיסטיקה',
    statisticsSubtitle: 'התקדמות זיהוי לפי רמה',
    birdsRecognized: 'ציפורים שזוהו',
    viewStatistics: 'לסטטיסטיקה',
    resetTier: 'איפוס רמה',
    resetTierConfirm: 'לאפס התקדמות עבור רמה',
    cancel: 'ביטול',
    reset: 'איפוס',
    loadingProgress: 'טוען התקדמות...',
  },
  es: {
    appTitle: 'BirdLingo',
    endlessQuiz: 'Aves',
    settings: 'Configuración',
    selectCategory: 'Seleccionar Categoría',
    all: 'Todas las Aves',
    predator: 'Depredadores',
    raptor: 'Rapaces',
    waterBird: 'Aves Acuáticas',
    songbird: 'Pájaros Cantores',
    exotic: 'Aves Exóticas',
    gameBird: 'Aves de Caza',
    bigBird: 'Aves Grandes',
    other: 'Otros',
    // Locations
    israel: 'Israel',
    africa: 'África',
    us: 'Estados Unidos',
    europe: 'Europa',
    asia: 'Asia',
    startQuiz: 'Iniciar Quiz',
    correct: 'Correcto',
    wrong: 'Incorrecto',
    next: 'Siguiente',
    backToMenu: 'Volver al Menú',
    level: 'Nivel',
    selectLevel: 'Seleccionar Nivel',
    difficulty: 'Dificultad',
    language: 'Idioma',
    chooseLanguage: 'Elegir Idioma',
    sessionStats: 'Estadísticas',
    correctAnswer: 'Respuesta Correcta',
    yourAnswer: 'Tu Respuesta',
    great: '¡Genial!',
    tryAgain: 'Incorrecto',
    whatBird: '¿Qué ave es esta?',
    easy: 'Fácil',
    medium: 'Medio',
    hard: 'Difícil',
    expert: 'Experto',
    master: 'Maestro',
    // New Game Modes
    gameFormat: 'Formato de Juego',
    classic: 'Clásico (Adivina el Nombre)',
    findImage: 'Encuentra la Imagen',
    typeName: 'Escribe el Nombre',
    mixed: 'Práctica Mixta',
    typeBirdName: 'Escribe el nombre del ave aquí...',
    submit: 'Enviar',
    iDontKnow: 'No lo sé',
    attemptsLeft: 'Intentos restantes',
    birdName: 'Ave',
    whichImage: '¿Qué imagen es de',
    // New Levels & Difficulty
    level1Title: 'Grupos de aves comunes',
    level2Title: 'Grupos de aves menos comunes',
    level3Title: 'Especies específicas',
    level4Title: 'Especies específicas',
    beginnerMode: 'Principiante',
    advancedMode: 'Avanzado (Especies)',
    tier1Mode: 'Nivel 1',
    tier2Mode: 'Nivel 2',
    tier3Mode: 'Nivel 3 (Especies específicas)',
    selectDifficulty: 'Seleccionar Dificultad',
    noAvailableLevels: 'No hay suficientes aves en esta categoría',
    statistics: 'Estadísticas',
    statisticsSubtitle: 'Progreso de reconocimiento por nivel',
    birdsRecognized: 'aves reconocidas',
    viewStatistics: 'Ver estadísticas',
    resetTier: 'Reiniciar nivel',
    resetTierConfirm: '¿Reiniciar progreso para el nivel',
    cancel: 'Cancelar',
    reset: 'Reiniciar',
    loadingProgress: 'Cargando progreso...',
  },
};

export const LanguageProvider = ({ children }) => {
  const [language, setLanguage] = useState('en');

  const currentLanguage = LANGUAGES[language];
  const t = TRANSLATIONS[language];
  const isRTL = currentLanguage.isRTL;

  // Get text alignment based on RTL
  const getTextAlign = () => (isRTL ? 'right' : 'left');

  // Get bird name in current language
  const getBirdName = (bird) => {
    return bird.names[language] || bird.names.en;
  };

  const value = {
    language,
    setLanguage,
    currentLanguage,
    t,
    isRTL,
    getTextAlign,
    getBirdName,
    languages: LANGUAGES,
  };

  return (
    <LanguageContext.Provider value={value}>
      {children}
    </LanguageContext.Provider>
  );
};

export const useLanguage = () => {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error('useLanguage must be used within a LanguageProvider');
  }
  return context;
};

export default LanguageContext;
