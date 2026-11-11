# Repository Guidelines — Yana Kozachenko Visual Guide

## Project Structure & Module Organization

This is a zero-dependency static visual brand guide and interactive color studio.
- Root files: `index.html` (semantic page markup and text), `style.css` (master stylesheet importing modules), `app.js` (entry point orchestrating initialization), `dev.py` (live-reload development server).
- `js/`: Modular Vanilla JavaScript (ES6+):
  - `data.js`: Core brand color palette, workshop presets, highlights icons metadata.
  - `studio.js`: Color workshop interaction, 4:5 vs 9:16 format switching, WCAG contrast calculation, localStorage persistence (`yk-colors`).
  - `render.js`: Dynamic DOM rendering for palette cards and Highlights circles.
  - `utils.js`: Toast notifications, clipboard copying, and relative luminance math.
- `css/`: Modular styles (`base.css`, `hero.css`, `studio.css`, `palette.css`, `typography.css`, `elements.css`, `feed.css`, `rules.css`, `responsive.css`).
- `assets/`: Vector SVG icons, WebP photography, and brand board images.
- `.github/workflows/deploy.yml`: Deploys root directory directly to GitHub Pages.

## Build, Test, and Development Commands

- `python3 dev.py`: Starts zero-dependency HTTP server with SSE Live Reload on port 8000.
  - CSS modifications inject hot updates without reloading the page.
  - HTML and JS modifications reload the page while preserving scroll position.
- `node --check app.js js/*.js`: Checks JavaScript syntax.
- `python3 -m py_compile dev.py`: Validates Python syntax for dev server.
- `openspec validate --specs`: Validates OpenSpec specification compliance.

## Coding Style & Naming Conventions

- Use semantic HTML5, CSS custom properties (`:root`), and pure Vanilla JavaScript without external dependencies.
- Ukrainian interface copy and accessible labels (`aria-label`, `aria-pressed`).
- Keep brand palette definitions synchronized between `index.html`, `js/data.js`, and `css/`.
- Ensure all color combinations pass WCAG AA contrast standards (minimum 4.5:1 for normal text, 3:1 for large text).
