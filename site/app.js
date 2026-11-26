const button = document.getElementById('toggle-code');
button.addEventListener('click', () => {
  const blocks = [...document.querySelectorAll('details.code')];
  const expand = !blocks.every(block => block.open);
  blocks.forEach(block => { block.open = expand; });
  button.textContent = expand ? 'Collapse all Python code' : 'Expand all Python code';
  button.setAttribute('aria-pressed', String(expand));
});
