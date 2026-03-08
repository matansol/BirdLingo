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

const FORMATS = [
    { id: 'classic', key: 'classic', icon: 'check-circle-outline', color: COLORS.primaryGreen },
    { id: 'find_image', key: 'findImage', icon: 'image-search', color: '#1976D2' },
    { id: 'type_name', key: 'typeName', icon: 'keyboard-outline', color: '#F57C00' },
    { id: 'mixed', key: 'mixed', icon: 'shuffle-variant', color: '#7B1FA2' },
];

const GameFormatSelectScreen = ({ navigation, route }) => {
    const { t, getTextAlign } = useLanguage();
    const { mode } = route.params;

    const handleFormatSelect = (formatId) => {
        // If endless quiz, go to CategorySelect
        if (mode === 'endless') {
            navigation.navigate('CategorySelect', {
                mode,
                questionFormat: formatId,
            });
        } else {
            // If campaign, go to LevelSelect
            navigation.navigate('LevelSelect', {
                mode,
                questionFormat: formatId,
            });
        }
    };

    return (
        <SafeAreaView style={styles.container}>
            <StatusBar style="dark" />

            {/* Header */}
            <View style={styles.header}>
                <Text style={[styles.title, { textAlign: getTextAlign() }]}>
                    {t.gameFormat}
                </Text>
            </View>

            {/* Formats */}
            <ScrollView
                style={styles.scrollView}
                contentContainerStyle={styles.formatsContainer}
            >
                {FORMATS.map((format) => (
                    <TouchableOpacity
                        key={format.id}
                        style={[styles.formatCard, { borderLeftColor: format.color }]}
                        onPress={() => handleFormatSelect(format.id)}
                        activeOpacity={0.8}
                    >
                        <MaterialCommunityIcons
                            name={format.icon}
                            size={40}
                            color={format.color}
                            style={styles.formatIcon}
                        />
                        <Text style={[styles.formatName, { textAlign: getTextAlign() }]}>
                            {t[format.key]}
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
    formatsContainer: {
        padding: SPACING.lg,
    },
    formatCard: {
        flexDirection: 'row',
        alignItems: 'center',
        backgroundColor: COLORS.white,
        borderRadius: BORDER_RADIUS.lg,
        padding: SPACING.lg,
        marginBottom: SPACING.md,
        borderLeftWidth: 4,
        ...SHADOWS.small,
    },
    formatIcon: {
        marginRight: SPACING.md,
    },
    formatName: {
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

export default GameFormatSelectScreen;
