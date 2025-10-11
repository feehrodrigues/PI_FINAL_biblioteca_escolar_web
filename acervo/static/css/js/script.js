document.addEventListener('DOMContentLoaded', () => {
  const botao = document.getElementById('teste');
  if (botao) {
    botao.addEventListener('click', () => {
      alert('JavaScript funcionando!');
    });
  }
});