# Brand Palette Specification

## Purpose
The brand palette capability displays the official color palette of the brand with color swatches, usage descriptions, dynamic text contrast, and one-click HEX copying.

## Requirements

### Requirement: Core brand palette display
The system SHALL display all 6 core brand colors: Ink (#171717), Warm Cream (#F4EFE5), Signature Yellow (#F4C900), Turquoise (#4FC3D6), Dark Navy (#13304E), and White (#FFFFFF).

#### Scenario: Palette rendering
- **WHEN** user views the brand palette section
- **THEN** all 6 brand colors are displayed with names, hex codes, and usage role descriptions

### Requirement: Dynamic text contrast on color cards
The system SHALL compute the luminance of each swatch color block and apply contrasting text color to guarantee readability of the hex label.

#### Scenario: Swatch label readability
- **WHEN** swatch blocks are rendered
- **THEN** light swatches display dark text and dark swatches display light text based on relative luminance

### Requirement: Click-to-copy color code
The system SHALL copy the selected HEX color code to the user clipboard when a palette card is clicked and display a toast notification.

#### Scenario: Palette card click
- **WHEN** user clicks on any brand color card
- **THEN** HEX code is written to the system clipboard and a confirmation toast message appears
