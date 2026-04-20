/* ─────────────────────────────────────────────
   Railway Reservation System — Shared JS
   ───────────────────────────────────────────── */

const API_BASE = 'http://localhost:5000';

/* ── Active nav link ── */
document.addEventListener('DOMContentLoaded', () => {
  const path = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-links a').forEach(a => {
    if (a.getAttribute('href') === path) a.classList.add('active');
  });
});

/* ─────────────────────────
   API HELPERS
───────────────────────── */
async function apiFetch(url, options = {}) {
  const res = await fetch(API_BASE + url, {
    headers: { 'Content-Type': 'application/json' },
    ...options
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || 'API error');
  return data;
}

/* ─────────────────────────
   FORM VALIDATION
───────────────────────── */
function validateRequired(fields) {
  let valid = true;
  fields.forEach(id => {
    const el = document.getElementById(id);
    if (!el) return;
    if (!el.value.trim()) {
      el.style.borderColor = '#dc3545';
      valid = false;
    } else {
      el.style.borderColor = '';
    }
  });
  return valid;
}

function validateAge(ageId) {
  const el = document.getElementById(ageId);
  if (!el) return true;
  const v = parseInt(el.value);
  if (isNaN(v) || v <= 0 || v > 120) {
    el.style.borderColor = '#dc3545';
    return false;
  }
  el.style.borderColor = '';
  return true;
}

/* ─────────────────────────
   ALERTS
───────────────────────── */
function showAlert(containerId, message, type = 'info') {
  const icons = { success: '✅', error: '❌', info: 'ℹ️' };
  const container = document.getElementById(containerId);
  if (!container) return;
  container.innerHTML = `
    <div class="alert alert-${type}">
      ${icons[type]} ${message}
    </div>`;
  setTimeout(() => { container.innerHTML = ''; }, 4500);
}

/* ─────────────────────────
   FARE CALCULATOR
───────────────────────── */
function calcFare(classType) {
  const fares = { 'Sleeper': 300, 'AC 3-Tier': 500, 'AC 2-Tier': 800 };
  return fares[classType] || 300;
}

/* ─────────────────────────
   FORMAT DATE
───────────────────────── */
function fmtDate(d) {
  if (!d) return '—';
  const dt = new Date(d);
  return dt.toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' });
}

/* ─────────────────────────
   LOCALSTORAGE HELPERS
───────────────────────── */
function saveLS(key, val) {
  localStorage.setItem(key, JSON.stringify(val));
}

function loadLS(key) {
  try { return JSON.parse(localStorage.getItem(key)); }
  catch { return null; }
}
