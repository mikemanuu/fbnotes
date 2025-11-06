// js/authGuard.js
import { getAccessToken, refreshAccessToken, logoutLocal } from './utils.js';

export async function ensureAuthenticated() {
  let access = getAccessToken();
  if (!access) {
    logoutLocal('/login.html');
    return;
  }

  // try a small API call to verify token validity
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
        logoutLocal('/login.html');
      }
    } else if (!res.ok) {
      throw new Error(`Auth check failed: ${res.status}`);
    }
  } catch (err) {
    console.error(err);
    logoutLocal('/login.html');
  }
}
