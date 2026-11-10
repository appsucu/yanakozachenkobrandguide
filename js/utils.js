/* ==========================================================================
   Допоміжні функції: спливаючі підказки, копіювання в буфер, контрастність
   ========================================================================== */

let toastTimer;

/**
 * Показує спливаюче повідомлення внизу екрана
 */
function toast(message) {
  const el = document.querySelector('#toast');
  el.textContent = message;
  el.style.display = 'block';
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => {
    el.style.display = 'none';
  }, 2500);
}

/**
 * Копіює текст у буфер обміну та показує повідомлення
 */
async function copy(text) {
  try {
    await navigator.clipboard.writeText(text);
    toast('Скопійовано');
  } catch {
    toast('Не вдалося скопіювати — виділи HEX вручну');
  }
}

/**
 * Обчислює відносну яскравість кольору (WCAG) для перевірки контрасту
 */
function lum(hex) {
  const rgb = hex
    .slice(1)
    .match(/../g)
    .map((x) => parseInt(x, 16) / 255)
    .map((v) => (v <= 0.04045 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4));

  return rgb[0] * 0.2126 + rgb[1] * 0.7152 + rgb[2] * 0.0722;
}

