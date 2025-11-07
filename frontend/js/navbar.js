// navbar.js
import { apiFetch, logoutLocal } from './utils.js';

async function loadUser() {
  try {
    const user = await apiFetch('/accounts/me/');
    const username = document.getElementById('username');
    const avatar = document.getElementById('user-avatar');

    username.textContent = user.username;
    avatar.src = user.profile_photo
      ? user.profile_photo
      : 'https://via.placeholder.com/36?text=U'; // fallback avatar
  } catch (err) {
    console.error('User info fetch failed:', err);
  }
}

document.addEventListener('DOMContentLoaded', () => {
  loadUser();

  const logoutBtn = document.getElementById('logout-btn');
  if (logoutBtn) logoutBtn.addEventListener('click', () => logoutLocal());
});

