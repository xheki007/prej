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
  document.querySelector('meta[name="description"]').content = language === 'sq' ? 'PREJ është kompani softuerike në Kosovë, e drejtuar nga themeluesi. Aplikacione mobile, platforma web dhe sisteme të ndërlidhura.' : 'PREJ is a founder-led software engineering company in Kosovo. Mobile applications, web platforms and connected systems, designed with purpose and built with care.';
  document.querySelector('meta[property="og:title"]').content = document.title;
  document.querySelector('meta[property="og:description"]').content = document.querySelector('meta[name="description"]').content;
  updateMenuLabel();
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

const projectTabs = [...document.querySelectorAll('[data-project]')];
function selectProject(id, moveFocus = false) {
  if (!projectTabs.some(tab => tab.dataset.project === id)) return;
  projectTabs.forEach(tab => { const active = tab.dataset.project === id; tab.setAttribute('aria-selected',String(active)); tab.tabIndex = active ? 0 : -1; document.getElementById(tab.getAttribute('aria-controls')).hidden = !active; if (active && moveFocus) tab.focus(); });
}
projectTabs.forEach((tab, index) => {
  tab.addEventListener('click', () => selectProject(tab.dataset.project));
  tab.addEventListener('keydown', e => { let next; if (e.key === 'ArrowRight') next = (index + 1) % projectTabs.length; if (e.key === 'ArrowLeft') next = (index + projectTabs.length - 1) % projectTabs.length; if (e.key === 'Home') next = 0; if (e.key === 'End') next = projectTabs.length - 1; if (next !== undefined) { e.preventDefault(); selectProject(projectTabs[next].dataset.project, true); } });
});
document.querySelectorAll('[data-show-project]').forEach(link => link.addEventListener('click', () => selectProject(link.dataset.showProject)));
selectProject('mobility');

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
