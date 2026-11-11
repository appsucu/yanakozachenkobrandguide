# Color Studio Specification

## Purpose
The color studio capability provides an interactive design workshop allowing users to test color combinations, check WCAG contrast, switch preview formats, select presets, and persist themes.

## Requirements

### Requirement: Live color preview
The system SHALL dynamically update CSS variables for background, text, and accent colors in the mockup preview when any color control is modified.

#### Scenario: Color value change
- **WHEN** user selects a new color for background, text, or accent
- **THEN** preview container styles update immediately with the selected colors

### Requirement: Aspect ratio format toggle
The system SHALL support switching the visual mockup container between Instagram Post (4:5) and Stories (9:16) aspect ratios.

#### Scenario: Format selection
- **WHEN** user selects the stories format button
- **THEN** preview container dimensions and layout adapt to a 9:16 vertical stories format

### Requirement: Preset color themes
The system SHALL provide ready-to-use color presets (Бірюзовий, Редакційний, Темний, Сонячний) that configure all three color roles in a single click.

#### Scenario: Preset selection
- **WHEN** user clicks a preset theme button
- **THEN** background, text, and accent colors update to the predetermined preset values and the button indicates active state

### Requirement: Color picker and swatch selection
The system SHALL allow users to choose from official brand color swatches or enter custom HEX values using native color pickers.

#### Scenario: Swatch click
- **WHEN** user clicks an official palette swatch button
- **THEN** corresponding color role adopts the swatch HEX value and updates input text

#### Scenario: Custom color input
- **WHEN** user inputs a custom color using the native color picker
- **THEN** custom HEX value is reflected in the active preview and output indicator

### Requirement: WCAG contrast calculation
The system SHALL calculate the relative luminance contrast ratio between the chosen background and text colors and display standard WCAG AA compliance notes.

#### Scenario: High contrast colors
- **WHEN** contrast ratio between background and text is at or above 4.5:1
- **THEN** contrast indicator reports ratio and confirms sufficient contrast for normal text (AA)

#### Scenario: Low contrast colors
- **WHEN** contrast ratio between background and text falls below 3.0:1
- **THEN** contrast indicator issues a warning advising to adjust text or background colors

### Requirement: State persistence
The system SHALL persist user-selected colors in browser localStorage and automatically restore them on subsequent page visits.

#### Scenario: Page reload
- **WHEN** user refreshes the page after customizing colors
- **THEN** previously customized colors are restored from localStorage into the studio controls

### Requirement: Clipboard copy and reset
The system SHALL provide a copy button that writes current color roles to the clipboard with toast feedback, and a reset button restoring defaults.

#### Scenario: Copy colors
- **WHEN** user clicks the copy button
- **THEN** formatted text with background, text, and accent HEX codes is copied to the clipboard and a confirmation toast is shown

#### Scenario: Reset colors
- **WHEN** user clicks the reset button
- **THEN** colors revert to initial defaults and confirmation toast is displayed
