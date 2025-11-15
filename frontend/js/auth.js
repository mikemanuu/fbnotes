import { saveTokens, clearTokens, getRefreshToken, apiFetch } from './utils.js';

// Base URL for Django API
const API_BASE = "http://127.0.0.1:8000/api";

// Endpoints
const LOGIN_URL = "/accounts/login/";
const REGISTER_URL = "/accounts/register/";
const REFRESH_URL = "/accounts/token/refresh/";

// Register new user
export async function registerUser(formData) {
  // formData can be plain object or FormData (if profile_photo)
  if (formData instanceof FormData) {
    // Fetch handles Content-Type for FormData automatically
    const res = await fetch(`${API_BASE}${REGISTER_URL}`, {
      method: "POST",
      body: formData
    });
    if (!res.ok) {
      const txt = await res.text();
      throw { status: res.status, data: txt };
    }
    return await res.json();
  } else {
    return await apiFetch(REGISTER_URL, { method: "POST", body: formData });
  }
}

// Login user
export async function loginUser({ username, password }) {
  const res = await fetch(`${API_BASE}${LOGIN_URL}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password })
  });

  if (!res.ok) {
    const txt = await res.text();
    let data;
    try { 
      data = JSON.parse(txt); 
    } catch(e) { 
      data = txt; 
    }
    throw { status: res.status, data };
  }

  const data = await res.json();
  saveTokens(data);
  return data;
}

// Logout
export function logoutLocal(redirect = "/index.html") {
  clearTokens();
  window.location.href = redirect;
}

// Refresh access token
export async function refreshAccessToken() {
  const refresh = getRefreshToken();
  if (!refresh) throw new Error("No refresh token");

  const res = await fetch(`${API_BASE}${REFRESH_URL}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ refresh })
  });

  if (!res.ok) {
    clearTokens();
    throw new Error("Refresh failed");
  }

  const data = await res.json();
  localStorage.setItem("fb_access", data.access);
  return data.access;
}



///import { apiFetch } from './utils.js';

// Fetch logged-in user's info
export async function getCurrentUser() {
  const data = await apiFetch('/accounts/me/', { method: 'GET' });
  return data; // { username, email, profile_photo, ... }
}

