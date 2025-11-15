
// Helper functions used across pages

const API_BASE = "http://127.0.0.1:8000/api"; 

export function saveTokens({ access, refresh }) {
  localStorage.setItem("fb_access", access);
  localStorage.setItem("fb_refresh", refresh);
  localStorage.setItem("fb_token_time", Date.now()); // helpful for expiry heuristics
}

export function clearTokens() {
  localStorage.removeItem("fb_access");
  localStorage.removeItem("fb_refresh");
  localStorage.removeItem("fb_token_time");
}

export function getAccessToken() {
  return localStorage.getItem("fb_access");
}

export function getRefreshToken() {
  return localStorage.getItem("fb_refresh");
}

export function authHeaders() {
  const token = getAccessToken();
  return token ? { "Authorization": `Bearer ${token}` } : {};
}

// Convenience: JSON fetch wrapper with auth and error handling
export async function apiFetch(path, options = {}) {
  const url = API_BASE + path;
  const headers = options.headers || {};
  if (options.json !== false) {
    headers["Content-Type"] = headers["Content-Type"] || "application/json";
  }
  Object.assign(headers, authHeaders());
  const opts = {
    credentials: "same-origin",
    ...options,
    headers,
  };
  if (opts.body && headers["Content-Type"] === "application/json" && typeof opts.body !== "string") {
    opts.body = JSON.stringify(opts.body);
  }
  const res = await fetch(url, opts);
  // auto-401 handling could go here (redirect to login)
  if (!res.ok) {
    const text = await res.text();
    let data;
    try { data = JSON.parse(text); } catch(e) { data = text; }
    throw { status: res.status, data };
  }
  // if no content
  if (res.status === 204) return null;
  const contentType = res.headers.get("content-type") || "";
  return contentType.includes("application/json") ? await res.json() : await res.text();
}
