const BASE_URL = "http://localhost:8000/api";   

async function apiFetch(endpoint, options = {}) {
    const token = localStorage.getItem("token");

    const headers = {
        "Content-Type": "application/json",
        ...(token ? { Authorization: `Bearer ${token}` } : {})
    };

    const response = await fetch(`${BASE_URL}${endpoint}`, {
        headers,
        ...options
    });

    if (!response.ok) {
        console.error("API error", response.status, response.statusText);
        throw new Error(`API request failed: ${endpoint}`);
    }

    return response.json();
}

// EXPORTS
export const getMetrics = () => apiFetch("/analytics/");
export const getActivity = () => apiFetch("/activity/");
export const getAnnouncements = () => apiFetch("/announcements/");
export const getCategories = () => apiFetch("/categories/");
export const getAnalytics = () => apiFetch("/analytics/");
export const getBookmarks = () => apiFetch("/bookmarks/");
export const getNotes = () => apiFetch("/notes/");

// CRUD 
export const deleteNote = (id) =>
    apiFetch(`/notes/${id}/`, { method: "DELETE" });

export const deleteBookmark = (id) =>
    apiFetch(`/bookmarks/${id}/`, { method: "DELETE" });
