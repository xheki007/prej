# Existing hero, restrained motion
Approved direction: preserve the original photograph and copy, add light impulses only along the two existing turquoise conduits, gentle icon illumination and fine-pointer parallax (maximum 3 px per axis, below 4 px). No new network, image generation, canvas or dependencies.

1. RED: static tests require one intrinsic 1280×853 image/SVG stage, measured paths, four localized native pause/resume controls; services/cases must not load these resources.
2. Build homepage-only markup through scripts/hero.py; hero-motion.css owns decoration and hero-motion.js owns user preference, visibility, intersection and pointer state. Keep figure caption unchanged and put the control below existing copy.
3. Progressive enhancement: SVG hidden without JS; reduced-motion stays original static image. User pause persists while scrolling or changing preference; pausing resets parallax. Offscreen/hidden stops all animation; touch never receives parallax handlers.
4. Add CI browser checks across languages/widths: aligned boxes, animated dash changes, pause/resume, offscreen, document hidden, reduced-motion, bounded fine-pointer movement, touch hit targets, no-JS static.
5. Separate hero artifact: known-frame PNGs plus two short desktop/mobile WebM previews. Existing browser suites remain.
6. Run static/syntax/deterministic build checks. Parent owns CI, independent review and publication gate. No local browser launch.
