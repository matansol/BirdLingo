# Workspace Instructions (Birdlingo)

This file configures GitHub Copilot to understand the architectural setup, conventions, and operational characteristics of this React Native/Python application workspace.

## Architectural Overview
This application is "Birdlingo", a mobile app for identifying and learning bird species. It consists of:
1. **Frontend App**: Built with React Native and Expo.
2. **Data Pipeline**: Python-based scripts that procure, clean, and format datasets (`assets/birds_data.json`) and media (`assets/birds/*`).

## Project-Specific Conventions

### React Native / Frontend
- **State Management**: Use React Context via the Provider pattern (e.g. `LanguageProvider`, `ProgressProvider`). Avoid deep prop drilling.
- **Styling**: Always consume centralized theme constants (e.g., `COLORS`, `SPACING`, `BORDER_RADIUS`, `FONT_SIZES`) imported from `src/theme/`. Avoid hard-coded inline values.
- **Component Design**: Build modular, variant-driven components. Prefer functional components and hooks. Export from `src/components/index.js` (barrel exports).
- **Navigation**: Uses React Navigation (`@react-navigation/native-stack`). Check `src/navigation/` for route definitions.

### Python / Data Pipeline
- **Type Hints**: Always use typing (`def _fetch_bird(bird: str) -> list[dict]:`) to ensure clarity.
- **Docstrings**: Provide clear, standard docstrings for all pipeline modules and major functions.
- **Encapsulation**: Private helper functions must start with an underscore (e.g., `_is_bad_image`).
- **Code Organization**: Use Markdown-style section headers in scripts (e.g., `# ── Media Helpers ────`) to divide logic.

## Build and Developer Commands
- Run Expo App: `npm start` (or `npx expo start`)
- Run iOS Bundle: `npm run ios`
- Run Android Bundle: `npm run android`
- Python Environment: `conda activate courses`
- Run Python Script: `python scripts/<script>.py`
- Run Python Tests: `pytest data_tests/`

## Pitfalls & Best Practices
- **Asset Boundaries**: Bundled images in React Native must be statically analyzed. Handle the difference between `require()` calls and dynamic remote URIs carefully in `BirdImage` component implementations.
- **Virtual Environments**: Use the `courses` conda environment, which contains all the necessary PyTorch dependencies for data and image processing.
Activate with: `conda activate courses`
