// used by extension content script to extract snippet
function extractSnippet() {
  const selection = window.getSelection().toString().trim();
  if(selection) return selection.slice(0,500);
  const p = document.querySelector('p');
  if(p) return p.innerText.slice(0,500);
  return document.body.innerText.slice(0,500);
}
