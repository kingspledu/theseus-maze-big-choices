
(function () {
  var fontSize = 20;
  try { fontSize = Number(localStorage.getItem('theseus-reader-font-size')) || 20; } catch (_) {}
  function applyTextSize() {
    fontSize = Math.max(16, Math.min(48, fontSize));
    document.documentElement.style.setProperty('--reader-font-size', fontSize + 'px');
    document.querySelectorAll('[data-text-step]').forEach(function (button) {
      button.disabled = Number(button.dataset.textStep) < 0 ? fontSize <= 16 : fontSize >= 48;
    });
    try { localStorage.setItem('theseus-reader-font-size', String(fontSize)); } catch (_) {}
  }
  document.querySelectorAll('[data-text-step]').forEach(function (button) {
    button.addEventListener('click', function () {
      fontSize += Number(button.dataset.textStep) * 2;
      applyTextSize();
    });
  });
  applyTextSize();
})();
