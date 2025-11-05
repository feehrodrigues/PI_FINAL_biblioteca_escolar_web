// ARQUIVO: acervo/static/js/script.js

const toastElement = document.getElementById('live-toast');
const liveToast = toastElement ? new bootstrap.Toast(toastElement, { delay: 4000 }) : null;

function showNotification(message, type = 'info') {
  if (!liveToast) return;
  liveToast.hide();
  const toastBody = toastElement.querySelector('.toast-body');
  const details = {
    success: { icon: '✅', bg: 'bg-success' },
    danger:  { icon: '❌', bg: 'bg-danger' },
    warning: { icon: '⚠️', bg: 'bg-warning' },
    info:    { icon: 'ℹ️', bg: 'bg-primary' },
  };
  const config = details[type] || details.info;
  toastBody.innerHTML = `<span class="me-2">${config.icon}</span> ${message}`;
  toastElement.className = 'toast align-items-center text-white border-0';
  toastElement.classList.add(config.bg);
  liveToast.show();
}

document.addEventListener('DOMContentLoaded', () => {
  // --- Acessibilidade Visual (Fontes e Contraste) ---
  const increaseFontBtn = document.getElementById('increase-font');
  const decreaseFontBtn = document.getElementById('decrease-font');
  const toggleContrastBtn = document.getElementById('toggle-contrast');
  const htmlElement = document.documentElement;

  const initialFontSize = parseFloat(getComputedStyle(htmlElement).fontSize);
  let currentFontSize = parseFloat(localStorage.getItem('fontSize')) || initialFontSize;

  function applySavedSettings() {
    htmlElement.style.fontSize = `${currentFontSize}px`;
    if (localStorage.getItem('highContrast') === 'true') document.body.classList.add('high-contrast');
  }

  function increaseFontSize() {
    if (currentFontSize < initialFontSize + 8) {
      currentFontSize += 2;
      htmlElement.style.fontSize = `${currentFontSize}px`;
      localStorage.setItem('fontSize', currentFontSize);
      showNotification('Fonte aumentada');
    } else { showNotification('Tamanho máximo da fonte atingido', 'warning'); }
  }

  function decreaseFontSize() {
    if (currentFontSize > initialFontSize - 4) {
      currentFontSize -= 2;
      htmlElement.style.fontSize = `${currentFontSize}px`;
      localStorage.setItem('fontSize', currentFontSize);
      showNotification('Fonte diminuída');
    } else { showNotification('Tamanho mínimo da fonte atingido', 'warning'); }
  }

  function toggleContrast() {
    const isContrastOn = document.body.classList.toggle('high-contrast');
    localStorage.setItem('highContrast', isContrastOn);
    showNotification(isContrastOn ? 'Alto contraste ativado' : 'Alto contraste desativado');
  }

  if (increaseFontBtn) increaseFontBtn.addEventListener('click', increaseFontSize);
  if (decreaseFontBtn) decreaseFontBtn.addEventListener('click', decreaseFontSize);
  if (toggleContrastBtn) toggleContrastBtn.addEventListener('click', toggleContrast);

  document.addEventListener('keydown', (e) => {
    if (e.altKey) {
      const keyMap = { '=': increaseFontSize, '-': decreaseFontSize, 'c': toggleContrast, 'C': toggleContrast };
      if (keyMap[e.key]) { e.preventDefault(); keyMap[e.key](); }
    }
  });

  applySavedSettings();

  // --- Leitor de Conteúdo Global (TTS) ---
  if ('speechSynthesis' in window) {
    const startBtn = document.getElementById('leitor-global-btn');
    const mainContent = document.getElementById('main-content');
    const player = document.getElementById('global-tts-player');
    const pauseBtn = document.getElementById('global-tts-pause');
    const resumeBtn = document.getElementById('global-tts-resume');
    const stopBtn = document.getElementById('global-tts-stop');

    const updatePlayerControls = (state) => {
      if (!player) return;
      pauseBtn.classList.toggle('d-none', state !== 'playing');
      resumeBtn.classList.toggle('d-none', state !== 'paused');
    };

    if (startBtn && mainContent && player) {
      startBtn.addEventListener('click', () => {
        if (window.speechSynthesis.speaking) {
          window.speechSynthesis.cancel();
          player.classList.add('d-none');
          return;
        }
        
        let textToRead = mainContent.innerText;
        // Limpa múltiplos espaços em branco para uma leitura mais fluida
        textToRead = textToRead.replace(/\s+/g, ' ').trim();
        
        let utterance = new SpeechSynthesisUtterance(textToRead);
        utterance.lang = 'pt-BR';
        
        utterance.onstart = () => {
          player.classList.remove('d-none');
          updatePlayerControls('playing');
        };
        utterance.onpause = () => updatePlayerControls('paused');
        utterance.onresume = () => updatePlayerControls('playing');
        utterance.onend = () => player.classList.add('d-none');
        utterance.onerror = () => player.classList.add('d-none');

        window.speechSynthesis.speak(utterance);
      });

      pauseBtn.addEventListener('click', () => window.speechSynthesis.pause());
      resumeBtn.addEventListener('click', () => window.speechSynthesis.resume());
      stopBtn.addEventListener('click', () => window.speechSynthesis.cancel());
    }

    window.addEventListener('beforeunload', () => {
      window.speechSynthesis.cancel();
    });

  } else {
    const startBtn = document.getElementById('leitor-global-btn');
    if(startBtn) startBtn.style.display = 'none';
  }
});