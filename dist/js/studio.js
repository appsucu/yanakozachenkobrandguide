/* ==========================================================================
   Розділ 01: Інтерактивна майстерня кольорів (#studio)
   ========================================================================== */

let colors = [...presets[0][1]];

// Відновлення збережених кольорів із localStorage браузера
try {
  const saved = JSON.parse(localStorage.getItem('yk-colors'));
  if (
    Array.isArray(saved) &&
    saved.length === 3 &&
    saved.every((c) => /^#[\da-f]{6}$/i.test(c))
  ) {
    colors = saved;
  }
} catch {}

const preview = document.querySelector('#preview');

/**
 * Оновлює прев’ю макета, вибрані свотчі та показник контрасту
 */
function render() {
  ['bg', 'fg', 'accent'].forEach((prop, i) => {
    preview.style.setProperty('--' + prop, colors[i]);
  });

  document.querySelectorAll('.color-row').forEach((row, i) => {
    row.querySelector('input').value = colors[i];
    row.querySelector('output').textContent = colors[i].toUpperCase();

    row.querySelectorAll('.swatches button').forEach((btn, j) => {
      const active = palette[j][1].toLowerCase() === colors[i].toLowerCase();
      btn.classList.toggle('selected', active);
      btn.setAttribute('aria-pressed', active);
    });
  });

  document.querySelectorAll('#presets button').forEach((btn, i) => {
    const active = presets[i][1].every(
      (c, j) => c.toLowerCase() === colors[j].toLowerCase()
    );
    btn.classList.toggle('active', active);
    btn.setAttribute('aria-pressed', active);
  });

  // Обчислення контрасту між фоном і текстом
  const luminances = colors
    .slice(0, 2)
    .map(lum)
    .sort((a, b) => b - a);
  const ratio = (luminances[0] + 0.05) / (luminances[1] + 0.05);

  document.querySelector('#contrast-value').textContent =
    ratio.toFixed(2) + ' : 1';

  document.querySelector('#contrast-note').textContent =
    ratio >= 4.5
      ? 'Достатній контраст для звичайного тексту (AA).'
      : ratio >= 3
      ? 'Підходить лише для великого тексту (AA).'
      : 'Низький контраст: зміни колір тексту або фону.';

  try {
    localStorage.setItem('yk-colors', JSON.stringify(colors));
  } catch {}
}

/**
 * Ініціалізація кнопок пресетів, контролів кольору та перемикачів формату
 */
function initStudio() {
  // Кнопки готових сценаріїв (Бірюзовий, Редакційний, Темний, Сонячний)
  presets.forEach(([name, presetColors]) => {
    const btn = document.createElement('button');
    btn.textContent = name;
    btn.onclick = () => {
      colors = [...presetColors];
      render();
    };
    document.querySelector('#presets').append(btn);
  });

  // Рядки вибору кольорів (Фон, Текст, Графічний акцент)
  colorControlLabels.forEach((labelName, i) => {
    const row = document.createElement('div');
    row.className = 'color-row';
    row.innerHTML = `
      <div class="color-title">
        <label for="color-${i}">${labelName}</label>
        <div class="custom-color">
          <output></output>
          <input type="color" id="color-${i}" aria-label="${labelName}: власний колір">
        </div>
      </div>
      <div class="swatches" role="group" aria-label="${labelName}"></div>
    `;

    palette.forEach(([colorName, hex]) => {
      const btn = document.createElement('button');
      btn.style.background = hex;
      btn.title = colorName + ' ' + hex;
      btn.setAttribute('aria-label', colorName + ' ' + hex);
      btn.onclick = () => {
        colors[i] = hex;
        render();
      };
      row.querySelector('.swatches').append(btn);
    });

    row.querySelector('input').oninput = (e) => {
      colors[i] = e.target.value;
      render();
    };

    document.querySelector('#color-controls').append(row);
  });

  // Перемикач формату: Допис 4:5 / Сторіз 9:16
  document.querySelectorAll('[data-format]').forEach((btn) => {
    btn.onclick = () => {
      document.querySelectorAll('[data-format]').forEach((tab) => {
        const isCurrent = tab === btn;
        tab.classList.toggle('active', isCurrent);
        tab.setAttribute('aria-pressed', isCurrent);
      });
      preview.classList.toggle('story', btn.dataset.format === 'story');
    };
  });

  // Кнопка скидання кольорів
  document.querySelector('#reset').onclick = () => {
    colors = [...presets[0][1]];
    render();
    toast('Початкові кольори відновлено');
  };

  // Кнопка копіювання вибраної палітри
  document.querySelector('#copy').onclick = () => {
    copy(`Фон: ${colors[0]}\nТекст: ${colors[1]}\nАкцент: ${colors[2]}`);
  };
}

