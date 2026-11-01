/* Decorative progressive enhancement; no network, storage or pointer handlers. */
(() => {
  'use strict';
  const hosts = [...document.querySelectorAll('.ambient-host')];
  if (!hosts.length) return;
  const preference = window.matchMedia('(prefers-reduced-motion: reduce)');
  const visible = new Set();
  let suspended = false;
  const sync = () => {
    const allowed = !preference.matches && !document.hidden && !suspended;
    hosts.forEach(host => {
      host.dataset.ambientMotion = allowed && visible.has(host) ? 'running' : 'paused';
    });
  };
  // Without observation support, retain the static decoration rather than animate offscreen.
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) visible.add(entry.target);
        else visible.delete(entry.target);
      });
      sync();
    }, {threshold: 0});
    hosts.forEach(host => observer.observe(host));
  }
  preference.addEventListener('change', sync);
  document.addEventListener('visibilitychange', sync);
  window.addEventListener('pagehide', () => { suspended = true; sync(); });
  window.addEventListener('pageshow', () => { suspended = false; sync(); });
  sync();
})();
