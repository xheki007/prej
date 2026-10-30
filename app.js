/* PREJ — small, dependency-free interactions; no form data is stored or sent here. */
document.documentElement.classList.add('js');
const translatable = [...document.querySelectorAll('[data-sq]')];
translatable.forEach(el => { el.dataset.en = el.innerHTML; });
const ariaNodes = [...document.querySelectorAll('[data-sq-aria]')];
ariaNodes.forEach(el => { el.dataset.enAria = el.getAttribute('aria-label'); });
const altNodes = [...document.querySelectorAll('[data-sq-alt]')];
altNodes.forEach(el => { el.dataset.enAlt = el.getAttribute('alt'); });
let language = 'en';
const statusCopy = {
  en: {copied:'Project brief copied. Paste it into an email to ferizixhevdet@gmail.com.',manual:'Automatic copying is unavailable. Select and copy the text below.',draft:'Opening your email app. Review and send the draft there; no message has been sent by this site.',name:'Name',email:'Email',project:'Project',idea:'Idea / challenge',subject:'Project enquiry'},
  sq: {copied:'Përshkrimi u kopjua. Ngjite në një email për ferizixhevdet@gmail.com.',manual:'Kopjimi automatik nuk është i disponueshëm. Përzgjidhe dhe kopjoje tekstin më poshtë.',draft:'Po hapet aplikacioni i emailit. Kontrollo dhe dërgoje draftin atje; faqja nuk ka dërguar mesazh.',name:'Emri',email:'Email',project:'Projekti',idea:'Ideja / problemi',subject:'Kërkesë për projekt'}
};
function setLanguage(next, persist = true) {
  language = next === 'sq' ? 'sq' : 'en';
  document.documentElement.lang = language;
  translatable.forEach(el => { if (language === 'sq') el.textContent = el.dataset.sq; else el.innerHTML = el.dataset.en; });
  ariaNodes.forEach(el => el.setAttribute('aria-label', language === 'sq' ? el.dataset.sqAria : el.dataset.enAria));
  altNodes.forEach(el => el.setAttribute('alt', language === 'sq' ? el.dataset.sqAlt : el.dataset.enAlt));
  document.querySelectorAll('[data-lang]').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.lang === language)));
  document.title = language === 'sq' ? 'PREJ — Sisteme komplekse. Zgjidhje të qarta.' : 'PREJ — Complex systems. Clear solutions.';
  document.querySelector('meta[name="description"]').content = language === 'sq' ? 'PREJ është kompani zhvillimi softuerik në Kosovë. Aplikacione mobile, platforma biznesi, sisteme të asistuara nga AI, infrastrukturë e lidhur dhe produkte interaktive 3D.' : 'PREJ is a software development company in Kosovo. Mobile apps, business platforms, AI-assisted systems, connected infrastructure and interactive 3D products.';
  document.querySelector('meta[property="og:title"]').content = document.title;
  document.querySelector('meta[property="og:description"]').content = document.querySelector('meta[name="description"]').content;
  updateMenuLabel();
  updateProjectCount();
  if (document.querySelector('#form-status').dataset.state) showStatus(document.querySelector('#form-status').dataset.state);
  if (persist) { try { localStorage.setItem('prej.language', language); } catch {} }
}
const nav = document.querySelector('#site-nav');
const menu = document.querySelector('.menu-toggle');
function updateMenuLabel() {
  const open = menu.getAttribute('aria-expanded') === 'true';
  menu.setAttribute('aria-label', language === 'sq' ? (open ? 'Mbyll menynë' : 'Hap menynë') : (open ? 'Close menu' : 'Open menu'));
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
document.querySelectorAll('[data-lang]').forEach(button => button.addEventListener('click', () => setLanguage(button.dataset.lang)));
const initialLanguage = new URLSearchParams(location.search).get('lang');
let savedLanguage = 'en'; try { savedLanguage = localStorage.getItem('prej.language') || 'en'; } catch {}
setLanguage(initialLanguage || savedLanguage, false);

// All projects remain available without JavaScript. Filters update existing semantic cards.
function updateProjectCount() {
  const count = [...document.querySelectorAll('.portfolio-card')].filter(card => !card.hidden).length;
  document.querySelector('#project-count').textContent = language === 'sq' ? `${count} projekte të shfaqura` : `${count} projects shown`;
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
  form.elements.name.setCustomValidity(form.elements.name.value.trim() ? '' : (language === 'sq' ? 'Shkruaj emrin.' : 'Please enter your name.'));
  form.elements.message.setCustomValidity(form.elements.message.value.trim().length >= 10 ? '' : (language === 'sq' ? 'Përshkruaje idenë me të paktën 10 karaktere.' : 'Describe your idea in at least 10 characters.'));
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
