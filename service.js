/* Progressive service-page navigation only; enquiries stay on the localized home page. */
document.documentElement.classList.add('js');
const serviceMessages = JSON.parse(document.querySelector('#service-messages').textContent);
const serviceMenu = document.querySelector('.menu-toggle');
const serviceNav = document.querySelector('#site-nav');
function closeServiceMenu(focus = false) {
  serviceMenu.setAttribute('aria-expanded', 'false');
  serviceMenu.setAttribute('aria-label', serviceMessages.openMenu);
  serviceNav.classList.remove('is-open');
  if (focus) serviceMenu.focus();
}
serviceMenu.addEventListener('click', () => {
  const open = serviceMenu.getAttribute('aria-expanded') !== 'true';
  serviceMenu.setAttribute('aria-expanded', String(open));
  serviceMenu.setAttribute('aria-label', open ? serviceMessages.closeMenu : serviceMessages.openMenu);
  serviceNav.classList.toggle('is-open', open);
});
serviceNav.querySelectorAll('a').forEach(link => link.addEventListener('click', () => closeServiceMenu()));
matchMedia('(max-width: 860px)').addEventListener('change', () => closeServiceMenu());
document.addEventListener('click', event => {
  if (!event.target.closest('.site-header')) closeServiceMenu();
  document.querySelectorAll('.language-picker[open]').forEach(picker => {
    if (!picker.contains(event.target)) picker.open = false;
  });
});
document.addEventListener('keydown', event => {
  if (event.key !== 'Escape') return;
  if (serviceMenu.getAttribute('aria-expanded') === 'true') closeServiceMenu(true);
  document.querySelectorAll('.language-picker[open]').forEach(picker => {
    picker.open = false; picker.querySelector('summary').focus();
  });
});
document.querySelector('#year').textContent = String(new Date().getFullYear());
