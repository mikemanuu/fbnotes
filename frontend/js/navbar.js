// navbar.js
import { apiFetch } from './js/utils.js';
import { logoutLocal } from './js/auth.js';

async function loadUserInfo() {
  try {
    const user = await apiFetch('/accounts/me/');
    const infoDiv = document.getElementById('user-info');

    if (!user) {
      infoDiv.textContent = 'Guest';
      return;
    }

    let html = '';
    if (user.profile_photo) {
      html += `<img src="${user.profile_photo}" alt="profile" class="rounded-circle me-2" width="32" height="32">`;
    }
    html += `<span>${user.username}</span>`;
    infoDiv.innerHTML = html;

  } catch (err) {
    console.error('Failed to load user info:', err);
    if (err.status === 401) {
      logoutLocal('login.html');
    }
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const logoutBtn = document.getElementById('logout-btn');
  if (logoutBtn) {
    logoutBtn.addEventListener('click', () => logoutLocal());
  }
  loadUserInfo();
});
