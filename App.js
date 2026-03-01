import React from 'react';
import { View, StyleSheet } from 'react-native';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { LanguageProvider } from './src/context/LanguageContext';
import AppNavigator from './src/navigation/AppNavigator';
import { LanguageSwitcher } from './src/components';

export default function App() {
  return (
    <SafeAreaProvider>
      <LanguageProvider>
        <View style={styles.container}>
          <AppNavigator />
          <LanguageSwitcher />
        </View>
      </LanguageProvider>
    </SafeAreaProvider>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
});
