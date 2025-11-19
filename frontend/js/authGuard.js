// js/authGuard.js
import { refreshAccessToken, logoutLocal } from './auth.js';
import { getAccessToken } from './utils.js';

export async function ensureAuthenticated() {
  let access = getAccessToken();
  if (!access) {
    logoutLocal('http://127.0.0.1:5500/frontend/index.html');
    return;
  }

  // try API call to verify token validity
  try {
    const res = await fetch(`${location.origin}/api/accounts/me/`, {
      headers: { "Authorization": `Bearer ${access}` }
    });

    if (res.status === 401) {
      // Try refreshing token
      try {
        await refreshAccessToken();
      } catch (err) {
        console.error("Token refresh failed:", err);
        logoutLocal('http://127.0.0.1:5500/frontend/index.html');
      }
    } else if (!res.ok) {
      throw new Error(`Auth check failed: ${res.status}`);
    }
  } catch (err) {
    console.error(err);
    logoutLocal('http://127.0.0.1:5500/frontend/index.html');
  }
}

export function ensureAuthenticated() {
    const token = localStorage.getItem("token");

    if (!token) {
        window.location.href = "/index.html";
        return false;
    }

    return true;
}
