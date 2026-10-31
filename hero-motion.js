/* Progressive decoration only: native links/forms and the photograph work without this file. */
(() => {
  const stage = document.querySelector('.hero-motion-stage');
  const hero = document.querySelector('.hero');
  if (!stage || !hero) return;
  // Without visibility observation, keep the original static fallback and install no listeners.
  if (!('IntersectionObserver' in window)) return;
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  const fine = window.matchMedia('(hover: hover) and (pointer: fine)');
  let inView = false;
  let frame = 0;
  let x = 0;
  let y = 0;
  const reset = () => {
    cancelAnimationFrame(frame);
    frame = 0;
    x = y = 0;
    stage.style.setProperty('--hero-x', '0px');
    stage.style.setProperty('--hero-y', '0px');
  };
  const update = () => {
    const running = !reduced.matches && inView && !document.hidden;
    stage.dataset.motion = running ? 'running' : 'paused';
    if (!running || !fine.matches) reset();
  };
  // No touch listeners; coarse pointers retain normal scrolling and tapping.
  hero.addEventListener('pointermove', (event) => {
    if (!fine.matches || event.pointerType !== 'mouse' || stage.dataset.motion !== 'running') return;
    const box = hero.getBoundingClientRect();
    x = Math.max(-3, Math.min(3, ((event.clientX - box.left) / box.width - .5) * 6));
    y = Math.max(-3, Math.min(3, ((event.clientY - box.top) / box.height - .5) * 6));
    if (!frame) frame = requestAnimationFrame(() => {
      stage.style.setProperty('--hero-x', x.toFixed(2) + 'px');
      stage.style.setProperty('--hero-y', y.toFixed(2) + 'px');
      frame = 0;
    });
  }, {passive:true});
  hero.addEventListener('pointerleave', reset);
  document.addEventListener('visibilitychange', update);
  reduced.addEventListener('change', update);
  fine.addEventListener('change', update);
  stage.dataset.enhanced = '';
  new IntersectionObserver(([entry]) => {
      inView = entry.isIntersecting;
      update();
  }, {threshold:0}).observe(stage);
  update();
})();
