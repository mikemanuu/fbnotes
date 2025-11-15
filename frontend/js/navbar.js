// Loads the current user and wires logout. Uses apiFetch from utils and logoutLocal from auth.

import { apiFetch } from './utils.js';
import { logoutLocal } from './auth.js';

async function loadUser() {
  try {
    // call API to get current user
    const user = await apiFetch('/accounts/me/');
    // defensive checks for DOM elements and for missing fields
    const nameEl = document.getElementById('navUsername');
    const avatarEl = document.getElementById('navAvatar');

    if (nameEl) nameEl.textContent = user.username || user.email || 'You';
    if (avatarEl) {
  
      const src = user.profile_photo || user.avatar || '';
      if (src) {

        if (/^https?:\/\//i.test(src)) {
          avatarEl.src = src;
        } else {
          avatarEl.src = (location.origin + src);
        }
      } else {
        avatarEl.src = 'https://via.placeholder.com/40?text=U';
      }
    }
  } catch (err) {
    console.error('User info fetch failed:', err);

    // if unauthorized — force logout so user goes to login
    if (err && err.status === 401) {
      logoutLocal();
    }
  }
}

document.addEventListener('DOMContentLoaded', () => {
  loadUser();

  const logoutBtn = document.getElementById('logoutBtn'); 
  if (logoutBtn) logoutBtn.addEventListener('click', (e) => {
    e.preventDefault();
    logoutLocal();
  });
});
