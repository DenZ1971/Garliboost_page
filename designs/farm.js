'use strict';

// Work in tenths of a kilogram. Integer arithmetic keeps decimal inputs stable.
function parseWeight(raw) {
  const normalized = raw.trim().replace(',', '.');
  if (!/^\d+(?:\.\d)?$/.test(normalized)) return null;
  const [whole, fraction = '0'] = normalized.split('.');
  const tenths = Number(whole) * 10 + Number(fraction);
  return Number.isSafeInteger(tenths) && tenths >= 1 && tenths <= 20000 ? tenths : null;
}

function formatTenths(value) {
  return new Intl.NumberFormat('ru-RU', { maximumFractionDigits: 1 }).format(value / 10);
}

function dividedDose(tenths, divisor) {
  if (tenths < divisor) return '<0,1';
  const rounded = Math.floor((tenths * 2 + divisor) / (2 * divisor));
  return (tenths % divisor ? '≈' : '') + formatTenths(rounded);
}

const weight = document.getElementById('weight');
function updateDose() {
  const tenths = parseWeight(weight.value);
  const valid = tenths !== null;
  weight.setAttribute('aria-invalid', String(!valid));
  document.getElementById('weight-error').textContent = valid ? '' :
    'Введите массу от 0,1 до 2 000 кг, не более одного знака после запятой.';
  document.getElementById('course').textContent = valid ? formatTenths(tenths) : '—';
  document.getElementById('daily').textContent = valid ? dividedDose(tenths, 7) : '—';
  document.getElementById('single').textContent = valid ? dividedDose(tenths, 14) : '—';
}
weight.addEventListener('input', updateDose);
updateDose();

const tabs = [...document.querySelectorAll('[role="tab"]')];
function activateTab(tab) {
  tabs.forEach(item => {
    const selected = item === tab;
    item.setAttribute('aria-selected', String(selected));
    item.tabIndex = selected ? 0 : -1;
    document.getElementById(item.getAttribute('aria-controls')).hidden = !selected;
  });
}
tabs.forEach((tab, index) => {
  tab.addEventListener('click', () => activateTab(tab));
  tab.addEventListener('keydown', event => {
    let next;
    if (event.key === 'ArrowRight') next = (index + 1) % tabs.length;
    if (event.key === 'ArrowLeft') next = (index + tabs.length - 1) % tabs.length;
    if (event.key === 'Home') next = 0;
    if (event.key === 'End') next = tabs.length - 1;
    if (next === undefined) return;
    event.preventDefault();
    activateTab(tabs[next]);
    tabs[next].focus();
  });
});

document.querySelectorAll('[data-expand-video]').forEach(button => {
  button.addEventListener('click', async () => {
    const video = button.closest('.video-feature').querySelector('video');
    try {
      if (video.requestFullscreen) await video.requestFullscreen();
      else if (video.webkitEnterFullscreen) video.webkitEnterFullscreen();
    } catch { /* Inline controls remain available if fullscreen is unavailable. */ }
    try { await video.play(); } catch { video.focus(); }
  });
});
document.querySelectorAll('video').forEach(video => video.addEventListener('play', () => {
  document.querySelectorAll('video').forEach(other => { if (other !== video) other.pause(); });
}));

document.getElementById('materials-link').addEventListener('click', () => {
  document.getElementById('materials').open = true;
});
if (location.hash === '#materials') document.getElementById('materials').open = true;

document.getElementById('farm-form').addEventListener('submit', event => {
  event.preventDefault();
  document.getElementById('form-status').textContent =
    'Дизайн-макет: данные не отправлены. Подключение формы — на этапе разработки сайта.';
});
document.querySelector('.languages').addEventListener('change', event => {
  alert('Это русскоязычный макет. Полные переводы на EN, SK, CS, HU и DE пока не подключены.');
  event.target.value = 'RU';
});

// Native WebVTT tracks stay switchable, including in fullscreen.
document.querySelectorAll('.caption-toggle').forEach(toggle => {
  const video = toggle.closest('.video-stage').querySelector('video');
  const apply = () => { for (const track of video.textTracks) track.mode = toggle.checked ? 'showing' : 'disabled'; };
  toggle.addEventListener('change', apply);
  video.addEventListener('loadedmetadata', apply);
  video.querySelector('track').addEventListener('load', apply);
  apply();
});

// Compact navigation for widths where the desktop links no longer fit.
const menuToggle = document.querySelector('.menu-toggle');
const primaryNav = document.getElementById('primary-nav');
const mobileNavQuery = matchMedia('(max-width: 1050px)');
function closeMenu(returnFocus = false) {
  primaryNav.classList.remove('is-open');
  menuToggle.setAttribute('aria-expanded', 'false');
  menuToggle.setAttribute('aria-label', 'Открыть меню');
  if (returnFocus) menuToggle.focus();
}
menuToggle.addEventListener('click', () => {
  const open = menuToggle.getAttribute('aria-expanded') !== 'true';
  primaryNav.classList.toggle('is-open', open);
  menuToggle.setAttribute('aria-expanded', String(open));
  menuToggle.setAttribute('aria-label', open ? 'Закрыть меню' : 'Открыть меню');
});
primaryNav.querySelectorAll('a').forEach(link => link.addEventListener('click', () => closeMenu()));
addEventListener('hashchange', () => closeMenu());
addEventListener('keydown', event => { if (event.key === 'Escape' && primaryNav.classList.contains('is-open')) closeMenu(true); });
document.addEventListener('click', event => { if (!event.target.closest('header')) closeMenu(); });
mobileNavQuery.addEventListener('change', () => closeMenu());
