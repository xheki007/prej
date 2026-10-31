/* PREJ — small, dependency-free interactions; no form data is stored or sent here. */
document.documentElement.classList.add('js');
const language = document.documentElement.lang;
const messages = JSON.parse(document.querySelector('#locale-messages').textContent);
const statusCopy = {[language]: messages};
// Honor old shared links without letting browser storage override a crawlable URL.
const legacyLanguage = new URLSearchParams(location.search).get('lang');
if (['sq','en','de','it'].includes(legacyLanguage)) {
  const target = new URL(`/${legacyLanguage}/`, location.origin);
  const params = new URLSearchParams(location.search); params.delete('lang');
  target.search = params.toString(); target.hash = location.hash;
  location.replace(target.href);
}
const nav = document.querySelector('#site-nav');
const menu = document.querySelector('.menu-toggle');
function updateMenuLabel() {
  const open = menu.getAttribute('aria-expanded') === 'true';
  menu.setAttribute('aria-label', open ? messages.closeMenu : messages.openMenu);
}
function closeMenu(returnFocus = false) {
  menu.setAttribute('aria-expanded','false'); nav.classList.remove('is-open'); updateMenuLabel();
  if (returnFocus) menu.focus();
}
menu.addEventListener('click', () => { const open = menu.getAttribute('aria-expanded') !== 'true'; menu.setAttribute('aria-expanded', String(open)); nav.classList.toggle('is-open', open); updateMenuLabel(); });
nav.querySelectorAll('a').forEach(link => link.addEventListener('click', () => closeMenu()));
document.addEventListener('keydown', e => { if (e.key === 'Escape' && menu.getAttribute('aria-expanded') === 'true') closeMenu(true); });
document.addEventListener('click', e => { if (menu.getAttribute('aria-expanded') === 'true' && !e.target.closest('.site-header')) closeMenu(); });
const mobileLayout = matchMedia('(max-width: 860px)');
mobileLayout.addEventListener('change', () => closeMenu());
document.querySelectorAll('.language-options a').forEach(link => link.addEventListener('click', () => {
  link.hash = location.hash;
}));
document.addEventListener('click', event => document.querySelectorAll('.language-picker[open]').forEach(picker => {
  if (!picker.contains(event.target)) picker.open = false;
}));
document.addEventListener('keydown', event => {
  if (event.key === 'Escape') document.querySelectorAll('.language-picker[open]').forEach(picker => {
    picker.open = false; picker.querySelector('summary').focus();
  });
});

// All projects remain available without JavaScript. Filters update existing semantic cards.
function updateProjectCount() {
  const count = [...document.querySelectorAll('.portfolio-card')].filter(card => !card.hidden).length;
  document.querySelector('#project-count').textContent = messages.projectsShown.replace('{count}', count);
}
function filterProjects(category) {
  document.querySelectorAll('[data-filter]').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.filter === category)));
  document.querySelectorAll('.portfolio-card').forEach(card => {
    card.hidden = category !== 'all' && card.dataset.category !== category;
    if (!card.hidden) card.classList.add('is-revealed');
  });
  updateProjectCount();
}
document.querySelectorAll('[data-filter]').forEach(button => button.addEventListener('click', () => filterProjects(button.dataset.filter)));
document.querySelectorAll('[data-filter-link]').forEach(link => link.addEventListener('click', () => filterProjects(link.dataset.filterLink)));
updateProjectCount();

// Motion is progressive enhancement, finite, and respects live system preference changes.
const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
const revealTargets = [...document.querySelectorAll('.section-heading, .capability, .portfolio-card, .process-grid article, .accountability, .stack-grid article')];
let revealObserver;
function configureMotion() {
  revealObserver?.disconnect();
  if (reducedMotion.matches || !('IntersectionObserver' in window)) {
    revealTargets.forEach(el => { el.classList.remove('reveal-ready'); el.classList.add('is-revealed'); });
    return;
  }
  revealObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) { entry.target.classList.add('is-revealed'); revealObserver.unobserve(entry.target); }
    });
  }, {threshold: 0.06, rootMargin: '0px 0px -24px 0px'});
  revealTargets.forEach(el => {
    // Already-seen content never disappears when preferences change.
    if (!el.classList.contains('is-revealed')) { el.classList.add('reveal-ready'); revealObserver.observe(el); }
  });
}
configureMotion();
reducedMotion.addEventListener('change', configureMotion);
document.addEventListener('focusin', event => event.target.closest('.reveal-ready')?.classList.add('is-revealed'));

const dialog = document.querySelector('#brief-dialog');
const form = document.querySelector('#brief-form');
let dialogOpener;
document.querySelectorAll('[data-open-brief]').forEach(button => button.addEventListener('click', () => { dialogOpener = button; dialog.showModal(); }));
dialog.querySelector('.close-dialog').addEventListener('click', () => dialog.close());
dialog.addEventListener('click', e => { if (e.target === dialog) { const box = dialog.getBoundingClientRect(); if (e.clientX < box.left || e.clientX > box.right || e.clientY < box.top || e.clientY > box.bottom) dialog.close(); } });
dialog.addEventListener('close', () => dialogOpener?.focus());
function showStatus(state) { const el = document.querySelector('#form-status'); el.dataset.state = state; el.textContent = statusCopy[language][state] || ''; }
function projectBrief() {
  const values = new FormData(form); const t = statusCopy[language];
  return `${t.name}: ${String(values.get('name')).trim()}\n${t.email}: ${String(values.get('email')).trim()}\n${t.project}: ${form.elements.service.selectedOptions[0].textContent}\n\n${t.idea}:\n${String(values.get('message')).trim()}`;
}
function validateBrief() {
  form.elements.email.setCustomValidity('');
  form.elements.email.setCustomValidity(!form.elements.email.value.trim() ? messages.requiredEmail : (form.elements.email.validity.typeMismatch ? messages.invalidEmail : ''));
  form.elements.name.setCustomValidity(form.elements.name.value.trim() ? '' : messages.requiredName);
  form.elements.message.setCustomValidity(form.elements.message.value.trim().length >= 10 ? '' : messages.requiredIdea);
  return form.reportValidity();
}
function clearBriefFeedback(e) {
  if (e.target.setCustomValidity) e.target.setCustomValidity('');
  const status = document.querySelector('#form-status');
  status.textContent = ''; delete status.dataset.state;
  document.querySelector('#manual-copy').hidden = true;
  document.querySelector('#manual-brief').value = '';
}
form.addEventListener('input', clearBriefFeedback);
form.addEventListener('change', clearBriefFeedback);
form.addEventListener('submit', e => {
  e.preventDefault(); if (!validateBrief()) return;
  const subject = `${statusCopy[language].subject} — PREJ`;
  const href = `mailto:ferizixhevdet@gmail.com?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(projectBrief())}`;
  showStatus('draft'); window.location.href = href;
});
document.querySelector('#copy-brief').addEventListener('click', async () => {
  if (!validateBrief()) return;
  const brief = projectBrief();
  try { await navigator.clipboard.writeText(brief); document.querySelector('#manual-copy').hidden = true; showStatus('copied'); }
  catch { document.querySelector('#manual-copy').hidden = false; const text = document.querySelector('#manual-brief'); text.value = brief; text.focus(); text.select(); showStatus('manual'); }
});
document.querySelector('#year').textContent = String(new Date().getFullYear());

// Attach the movie only after an explicit play request. Page loads fetch no video.
const workflowVideo = document.querySelector('#workflow-video');
const workflowPlay = document.querySelector('.workflow-play');
const workflowVideoError = document.querySelector('#workflow-video-error');
function showWorkflowVideoError() {
  workflowPlay.hidden = false;
  workflowVideo.controls = false;
  workflowVideo.setAttribute('aria-hidden', 'true');
  workflowVideo.tabIndex = -1;
  workflowVideoError.hidden = false;
}
workflowVideo.addEventListener('error', showWorkflowVideoError);
workflowPlay.addEventListener('click', async () => {
  workflowVideoError.hidden = true;
  workflowPlay.hidden = true;
  workflowVideo.controls = true;
  workflowVideo.removeAttribute('aria-hidden');
  workflowVideo.tabIndex = 0;
  if (!workflowVideo.getAttribute('src') || workflowVideo.error) {
    workflowVideo.src = workflowVideo.dataset.src;
  }
  try {
    await workflowVideo.play();
    workflowVideo.focus({preventScroll: true});
  } catch {
    showWorkflowVideoError();
    workflowPlay.focus({preventScroll: true});
  }
});

