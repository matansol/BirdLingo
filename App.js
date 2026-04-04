import React from 'react';
import { View, StyleSheet } from 'react-native';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { LanguageProvider } from './src/context/LanguageContext';
import { ProgressProvider } from './src/context/ProgressContext';
import AppNavigator from './src/navigation/AppNavigator';
import { LanguageSwitcher } from './src/components';

export default function App() {
  return (
    <SafeAreaProvider>
      <ProgressProvider>
        <LanguageProvider>
          <View style={styles.container}>
            <AppNavigator />
            <LanguageSwitcher />
          </View>
        </LanguageProvider>
      </ProgressProvider>
    </SafeAreaProvider>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
});
