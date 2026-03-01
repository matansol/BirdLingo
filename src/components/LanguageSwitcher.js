import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Modal,
  Pressable,
} from 'react-native';
import { COLORS, SPACING, BORDER_RADIUS, FONT_SIZES, SHADOWS } from '../theme/theme';
import { useLanguage, LANGUAGES } from '../context/LanguageContext';

const LANGUAGE_FLAGS = {
  en: '🇬🇧',
  he: '🇮🇱',
  es: '🇪🇸',
};

const LanguageSwitcher = () => {
  const { language, setLanguage } = useLanguage();
  const [modalVisible, setModalVisible] = useState(false);

  const handleLanguageSelect = (langCode) => {
    setLanguage(langCode);
    setModalVisible(false);
  };

  return (
    <>
      {/* Floating Button */}
      <TouchableOpacity
        style={styles.floatingButton}
        onPress={() => setModalVisible(true)}
        activeOpacity={0.8}
      >
        <Text style={styles.flagIcon}>{LANGUAGE_FLAGS[language]}</Text>
      </TouchableOpacity>

      {/* Language Selection Modal */}
      <Modal
        visible={modalVisible}
        transparent={true}
        animationType="fade"
        onRequestClose={() => setModalVisible(false)}
      >
        <Pressable
          style={styles.modalOverlay}
          onPress={() => setModalVisible(false)}
        >
          <View style={styles.modalContent}>
            <Text style={styles.modalTitle}>Select Language</Text>
            
            {Object.values(LANGUAGES).map((lang) => (
              <TouchableOpacity
                key={lang.code}
                style={[
                  styles.languageOption,
                  language === lang.code && styles.selectedOption,
                ]}
                onPress={() => handleLanguageSelect(lang.code)}
                activeOpacity={0.7}
              >
                <Text style={styles.optionFlag}>{LANGUAGE_FLAGS[lang.code]}</Text>
                <View style={styles.optionTextContainer}>
                  <Text
                    style={[
                      styles.optionName,
                      language === lang.code && styles.selectedText,
                    ]}
                  >
                    {lang.name}
                  </Text>
                  <Text style={styles.optionNative}>{lang.nativeName}</Text>
                </View>
                {language === lang.code && (
                  <Text style={styles.checkmark}>✓</Text>
                )}
              </TouchableOpacity>
            ))}
          </View>
        </Pressable>
      </Modal>
    </>
  );
};

const styles = StyleSheet.create({
  floatingButton: {
    position: 'absolute',
    bottom: 30,
    left: 20,
    width: 56,
    height: 56,
    borderRadius: 28,
    backgroundColor: COLORS.white,
    justifyContent: 'center',
    alignItems: 'center',
    ...SHADOWS.large,
    zIndex: 1000,
    borderWidth: 2,
    borderColor: COLORS.primaryGreen,
  },
  flagIcon: {
    fontSize: 28,
  },
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  modalContent: {
    backgroundColor: COLORS.white,
    borderRadius: BORDER_RADIUS.xl,
    padding: SPACING.lg,
    width: '80%',
    maxWidth: 320,
    ...SHADOWS.large,
  },
  modalTitle: {
    fontSize: FONT_SIZES.lg,
    fontWeight: 'bold',
    color: COLORS.textPrimary,
    textAlign: 'center',
    marginBottom: SPACING.md,
  },
  languageOption: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: SPACING.md,
    borderRadius: BORDER_RADIUS.md,
    marginBottom: SPACING.sm,
    backgroundColor: COLORS.offWhite,
  },
  selectedOption: {
    backgroundColor: COLORS.paleGreen,
    borderWidth: 2,
    borderColor: COLORS.primaryGreen,
  },
  optionFlag: {
    fontSize: 32,
    marginRight: SPACING.md,
  },
  optionTextContainer: {
    flex: 1,
  },
  optionName: {
    fontSize: FONT_SIZES.md,
    fontWeight: '600',
    color: COLORS.textPrimary,
  },
  optionNative: {
    fontSize: FONT_SIZES.sm,
    color: COLORS.textSecondary,
  },
  selectedText: {
    color: COLORS.primaryGreen,
  },
  checkmark: {
    fontSize: FONT_SIZES.xl,
    color: COLORS.primaryGreen,
    fontWeight: 'bold',
  },
});

export default LanguageSwitcher;
