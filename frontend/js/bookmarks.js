const bookmarksApi = "http://127.0.0.1:8000/api/bookmarks/";
import { apiFetch } from "./utils";

// DOM elements
const bookmarksList = document.getElementById("bookmarksList");
const addBookmarkBtn = document.getElementById("addBookmarkBtn");
const saveBookmarkBtn = document.getElementById("saveBookmarkBtn");

const bookmarkIdField = document.getElementById("bookmarkId");
const bookmarkTitleField = document.getElementById("bookmarkTitle");
const bookmarkUrlField = document.getElementById("bookmarkUrl");
const bookmarkDescriptionField = document.getElementById("bookmarkDescription");

const bookmarkModalTitle = document.getElementById("bookmarkModalTitle");
let bookmarkModal = new bootstrap.Modal(document.getElementById("bookmarkModal"));

document.addEventListener("DOMContentLoaded", loadBookmarks);

// Fetch bookmarks
function loadBookmarks() {
  apiFetch(bookmarksApi)
    .then(res => res.json())
    .then(bookmarks => renderBookmarks(bookmarks))
    .catch(err => console.error("Error fetching bookmarks:", err));
}

function renderBookmarks(bookmarks) {
  bookmarksList.innerHTML = "";

  if (bookmarks.length === 0) {
    bookmarksList.innerHTML = "<p>No bookmarks yet.</p>";
    return;
  }

  bookmarks.forEach(b => {
    const card = document.createElement("div");
    card.className = "card mb-3";
    card.innerHTML = `
      <div class="card-body">
        <h5 class="card-title">${b.title}</h5>
        <p class="card-text">${b.description || ""}</p>
        <a href="${b.url}" target="_blank" class="btn btn-sm btn-info me-2">
          Visit
        </a>
        <button class="btn btn-sm btn-warning me-2" onclick="editBookmark(${b.id})">
          Edit
        </button>
        <button class="btn btn-sm btn-danger" onclick="deleteBookmark(${b.id})">
          Delete
        </button>
      </div>
    `;
    bookmarksList.appendChild(card);
  });
}

// Add bookmark button
addBookmarkBtn.addEventListener("click", () => {
  bookmarkModalTitle.textContent = "Add Bookmark";
  bookmarkIdField.value = "";
  bookmarkTitleField.value = "";
  bookmarkUrlField.value = "";
  bookmarkDescriptionField.value = "";
  bookmarkModal.show();
});

// Save bookmark
saveBookmarkBtn.addEventListener("click", () => {
  const id = bookmarkIdField.value;
  const title = bookmarkTitleField.value.trim();
  const url = bookmarkUrlField.value.trim();
  const description = bookmarkDescriptionField.value.trim();

  if (!title || !url) {
    alert("Title and URL are required.");
    return;
  }

  const payload = { title, url, description };

  id ? updateBookmark(id, payload) : createBookmark(payload);
});

// Create bookmark
function createBookmark(payload) {
  apiFetch(bookmarksApi, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  })
    .then(res => res.json())
    .then(() => {
      bookmarkModal.hide();
      loadBookmarks();
    })
    .catch(err => console.error("Create bookmark error:", err));
}

// Edit bookmark
function editBookmark(id) {
  apiFetch(`${bookmarksApi}${id}/`)
    .then(res => res.json())
    .then(b => {
      bookmarkModalTitle.textContent = "Edit Bookmark";
      bookmarkIdField.value = b.id;
      bookmarkTitleField.value = b.title;
      bookmarkUrlField.value = b.url;
      bookmarkDescriptionField.value = b.description || "";
      bookmarkModal.show();
    })
    .catch(err => console.error("Fetch bookmark error:", err));
}

// Update bookmark
function updateBookmark(id, payload) {
  apiFetch(`${bookmarksApi}${id}/`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  })
    .then(res => res.json())
    .then(() => {
      bookmarkModal.hide();
      loadBookmarks();
    })
    .catch(err => console.error("Update error:", err));
}

// Delete bookmark
function deleteBookmark(id) {
  if (!confirm("Delete bookmark?")) return;

  apiFetch(`${bookmarksApi}${id}/`, { method: "DELETE" })
    .then(() => loadBookmarks())
    .catch(err => console.error("Delete error:", err));
}
