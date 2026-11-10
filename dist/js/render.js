/* ==========================================================================
   Генерація карток палітри (#palette) та іконок Highlights (#elements)
   ========================================================================== */

/**
 * Рендерить картки основної палітри бренду (Розділ 02)
 */
function renderPalette() {
  const grid = document.querySelector('#palette-grid');
  palette.forEach(([name, hex, description]) => {
    const btn = document.createElement('button');
    btn.className = 'palette-card';
    btn.setAttribute('aria-label', 'Копіювати ' + name + ' ' + hex);

    const textColor = lum(hex) > 0.3 ? '#171717' : '#F4EFE5';
    btn.innerHTML = `
      <div class="color-block" style="background:${hex};color:${textColor}">${hex} ↗</div>
      <strong>${name}</strong>
      <p>${description}</p>
    `;
    btn.onclick = () => copy(hex);
    grid.append(btn);
  });
}

/**
 * Рендерить іконки Instagram Highlights (Розділ 04)
 */
function renderHighlights() {
  const container = document.querySelector('#highlights');
  icons.forEach(([name, ukLabel, viewBox]) => {
    const el = document.createElement('div');
    el.className = 'highlight';
    el.innerHTML = `
      <img src="assets/brands/highlights-covers.svg#svgView(viewBox(${viewBox}))" alt="${ukLabel}">
      <p>${name}</p>
      <small>${ukLabel}</small>
    `;
    container.append(el);
  });
}

