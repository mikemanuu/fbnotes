import { loginUser, logoutLocal } from './auth.js';
import { apiFetch } from './utils.js';

const form = document.getElementById('login-form');
const alertPlaceholder = document.getElementById('alert-placeholder');

function showAlert(message, type = 'danger') {
  alertPlaceholder.innerHTML = `<div class="alert alert-${type}">${message}</div>`;
}

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const username = document.getElementById('username').value.trim();
  const password = document.getElementById('password').value;
  try {
    const tokens = await loginUser({ username, password });
    window.location.href = 'notes.html';
  } catch (err) {
    console.error(err);
    if (err && err.data) {
      showAlert(JSON.stringify(err.data));
    } else {
      showAlert('Login failed. Check credentials.');
    }
  }
});
