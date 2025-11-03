// Minimal AJAX client - uses fetch and JWT stored in localStorage under 'access'
document.addEventListener('DOMContentLoaded', ()=> {
  const addBtn = document.getElementById('addBookmark');
  const createModalEl = document.getElementById('createModal');
  const createForm = document.getElementById('createForm');
  const modal = new bootstrap.Modal(createModalEl);

  addBtn.addEventListener('click', ()=> modal.show());

  createForm.addEventListener('submit', async (e)=>{
    e.preventDefault();
    const url = document.getElementById('postUrl').value;
    const notes = document.getElementById('postNotes').value;
    const tags = document.getElementById('postTags').value.split(',').map(t=>t.trim()).filter(Boolean);
    const payload = {url, notes:[notes].filter(Boolean), tags};
    const token = localStorage.getItem('access');
    const res = await fetch('/api/v1/bookmarks/', {
      method:'POST',
      headers:{
        'Content-Type':'application/json',
        'Authorization': token ? `Bearer ${token}` : ''
      },
      body: JSON.stringify(payload)
    });
    if(res.ok){
      await loadBookmarks();
      modal.hide();
    } else {
      const err = await res.json();
      alert('Error: '+ JSON.stringify(err));
    }
  });

  async function loadBookmarks(){
    const token = localStorage.getItem('access');
    const res = await fetch('/api/v1/bookmarks/', {
      headers:{
        'Authorization': token ? `Bearer ${token}` : ''
      }
    });
    if(!res.ok) return;
    const data = await res.json();
    const cards = document.getElementById('cards');
    cards.innerHTML = '';
    data.results.forEach(b=>{
      const col = document.createElement('div'); col.className='col';
      col.innerHTML = `
      <div class="card">
        <div class="card-body">
          <h5 class="card-title">${b.title || b.url}</h5>
          <p class="card-text">${(b.excerpt||'').slice(0,140)}</p>
          <div>${(b.tags||[]).map(t=>`<span class="badge bg-secondary">${t.name}</span>`).join(' ')}</div>
          <div class="d-flex justify-content-end mt-2">
            <a href="/bookmark/${b.id}" class="btn btn-sm btn-outline-primary">View</a>
          </div>
        </div>
      </div>`;
      cards.appendChild(col);
    });
  }

  loadBookmarks();
});
