const BASE_URL = "http://localhost:8000/api";


// Token Helpers
function getAccessToken() {
    return localStorage.getItem("token");
}

function getRefreshToken() {
    return localStorage.getItem("refresh");
}

function saveAccessToken(token) {
    localStorage.setItem("token", token);
}

function clearTokens() {
    localStorage.removeItem("token");
    localStorage.removeItem("refresh");
}


// Refresh Token Function
async function refreshAccessToken() {
    const refresh = getRefreshToken();
    if (!refresh) throw new Error("No refresh token stored");

    const res = await fetch(`${BASE_URL}/auth/refresh/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ refresh })
    });

    if (!res.ok) throw new Error("Refresh token invalid");

    const data = await res.json();
    saveAccessToken(data.access);
}


// Main API Function
export async function apiFetch(endpoint, options = {}) {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 8000);

    const token = getAccessToken();

    const headers = {
        "Content-Type": "application/json",
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
        ...(options.headers || {})
    };

    let response;

    try {
        response = await fetch(`${BASE_URL}${endpoint}`, {
            ...options,
            headers,
            signal: controller.signal
        });
    } catch (err) {
        clearTimeout(timeout);
        console.error("Network error:", err);
        throw err;
    }

    clearTimeout(timeout);

    // If unauthorized, attempt token refresh once
    if (response.status === 401) {
        try {
            await refreshAccessToken();

            // Retry the request with new access token
            const newToken = getAccessToken();

            const retryHeaders = {
                ...headers,
                Authorization: `Bearer ${newToken}`
            };

            response = await fetch(`${BASE_URL}${endpoint}`, {
                ...options,
                headers: retryHeaders
            });
        } catch (refreshErr) {
            console.error("Failed to refresh token:", refreshErr);
            clearTokens();
            window.location.href = "index.html";
            return;
        }
    }

    if (!response.ok) {
        const text = await response.text();
        console.error("API error:", response.status, text);

        try {
            throw { status: response.status, data: JSON.parse(text) };
        } catch {
            throw { status: response.status, data: text };
        }
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
export const deleteNote = (id) => apiFetch(`/notes/${id}/`, { method: "DELETE" });
export const deleteBookmark = (id) => apiFetch(`/bookmarks/${id}/`, { method: "DELETE" });
