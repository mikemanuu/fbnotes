const apiBase = "http://127.0.0.1:8000/api/notes/";

// DOM elements
const notesList = document.getElementById("notesList");
const addNoteBtn = document.getElementById("addNoteBtn");
const saveNoteBtn = document.getElementById("saveNoteBtn");
const modalTitle = document.getElementById("modalTitle");

const noteIdField = document.getElementById("noteId");
const noteTitleField = document.getElementById("noteTitle");
const noteContentField = document.getElementById("noteContent");

let noteModal = new bootstrap.Modal(document.getElementById("noteModal"));


// Load notes on page load
document.addEventListener("DOMContentLoaded", loadNotes);


function loadNotes() {
  apiFetch(apiBase)
    .then(res => res.json())
    .then(notes => {
      renderNotes(notes);
    })
    .catch(err => console.error("Error fetching notes:", err));
}


function renderNotes(notes) {
  notesList.innerHTML = "";

  if (notes.length === 0) {
    notesList.innerHTML = "<p>No notes available.</p>";
    return;
  }

  notes.forEach(note => {
    const card = document.createElement("div");
    card.className = "card mb-3";
    card.innerHTML = `
      <div class="card-body">
        <h5 class="card-title">${note.title}</h5>
        <p class="card-text">${note.content}</p>
        <button class="btn btn-sm btn-warning me-2" onclick="editNote(${note.id})">Edit</button>
        <button class="btn btn-sm btn-danger" onclick="deleteNote(${note.id})">Delete</button>
      </div>
    `;
    notesList.appendChild(card);
  });
}


addNoteBtn.addEventListener("click", () => {
  modalTitle.textContent = "Add Note";
  noteIdField.value = "";
  noteTitleField.value = "";
  noteContentField.value = "";
  noteModal.show();
});


saveNoteBtn.addEventListener("click", () => {
  const id = noteIdField.value;
  const title = noteTitleField.value;
  const content = noteContentField.value;

  if (!title || !content) {
    alert("Both fields are required.");
    return;
  }

  const payload = { title, content };

  if (id) {
    updateNote(id, payload);
  } else {
    createNote(payload);
  }
});


function createNote(payload) {
  apiFetch(apiBase, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  })
    .then(res => res.json())
    .then(() => {
      noteModal.hide();
      loadNotes();
    })
    .catch(err => console.error("Error creating note:", err));
}


function editNote(id) {
  apiFetch(`${apiBase}${id}/`)
    .then(res => res.json())
    .then(note => {
      modalTitle.textContent = "Edit Note";
      noteIdField.value = note.id;
      noteTitleField.value = note.title;
      noteContentField.value = note.content;
      noteModal.show();
    })
    .catch(err => console.error("Error fetching note:", err));
}


function updateNote(id, payload) {
  apiFetch(`${apiBase}${id}/`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  })
    .then(res => res.json())
    .then(() => {
      noteModal.hide();
      loadNotes();
    })
    .catch(err => console.error("Error updating note:", err));
}


function deleteNote(id) {
  if (!confirm("Delete this note?")) return;

  apiFetch(`${apiBase}${id}/`, {
    method: "DELETE"
  })
    .then(() => loadNotes())
    .catch(err => console.error("Error deleting note:", err));
}
