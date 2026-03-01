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
    endlessQuiz: 'Endless Quiz',
    campaignMode: 'Campaign Mode',
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
    tryAgain: 'Try Again',
    whatBird: 'What bird is this?',
    easy: 'Easy',
    medium: 'Medium',
    hard: 'Hard',
    expert: 'Expert',
    master: 'Master',
  },
  he: {
    appTitle: 'BirdLingo',
    endlessQuiz: 'חידון אינסופי',
    campaignMode: 'מסע משחק',
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
    tryAgain: 'נסה שוב',
    whatBird: 'איזו ציפור זו?',
    easy: 'קל',
    medium: 'בינוני',
    hard: 'קשה',
    expert: 'מומחה',
    master: 'אמן',
  },
  es: {
    appTitle: 'BirdLingo',
    endlessQuiz: 'Quiz Infinito',
    campaignMode: 'Modo Campaña',
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
    tryAgain: 'Intenta de nuevo',
    whatBird: '¿Qué ave es esta?',
    easy: 'Fácil',
    medium: 'Medio',
    hard: 'Difícil',
    expert: 'Experto',
    master: 'Maestro',
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
