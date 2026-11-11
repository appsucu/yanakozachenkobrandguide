# Live Development Server Specification

## Purpose
The live development server capability provides a zero-dependency local development environment with Server-Sent Events (SSE) live reloading and scroll preservation.

## Requirements

### Requirement: Zero-dependency server execution
The system SHALL run the local development server using only the standard Python 3 runtime without requiring external pip packages or build tool chains.

#### Scenario: Running development script
- **WHEN** developer runs python3 dev.py
- **THEN** an HTTP server starts on port 8000 and serves project files with accurate MIME types

### Requirement: Hot CSS injection
The system SHALL push CSS style sheet updates directly to connected browser clients via SSE without triggering a full page reload.

#### Scenario: CSS file modification
- **WHEN** a stylesheet in the css directory is modified
- **THEN** server detects the change via file watcher and connected browser reloads only the CSS link elements instantaneously

### Requirement: Full page reload with scroll preservation
The system SHALL trigger a page reload when HTML or JavaScript files change while maintaining the user's vertical scroll position.

#### Scenario: Markup or script update
- **WHEN** HTML or JS files are saved
- **THEN** browser reloads the page and restores the prior scroll position from sessionStorage
