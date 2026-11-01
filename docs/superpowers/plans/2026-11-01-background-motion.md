# Approved background motion implementation

Goal: apply the reviewed subtle navy/turquoise data-line concept across all existing PREJ routes without changing content or the separate paused contact work.

Architecture: static decorative SVG inside each main section/content block and footer, above that block's background and below its content. Sparse local layers are isolated; an IntersectionObserver starts only visible pulses. No third-party code, canvas loop, persistence or requests. Reduced motion and no JavaScript use static fine linework.

- [x] Copy verified remote baseline into a separate workspace, preserving paused source.
- [x] Write static coverage/decoration/privacy tests and observe missing-feature failures.
- [ ] Add shared generator, CSS and visibility-aware runtime; rebuild all 21 HTML files.
- [ ] Run full static suite and syntax checks, add real-browser motion/interaction tests.
- [ ] Push draft PR and run exact-head desktop/mobile/no-JS CI; independent visual review.
- [ ] After concrete publication approval, merge and verify live release bytes.

Constraints: preserve SEO, content, assets, original hero motion, URL structure and all interactive controls. Use no visible decorative controls; do not claim full WCAG conformance. Handle reduced-motion changes, hidden tabs, back-forward cache, narrow screens and offscreen content. Keep pulse density lower on mobile. Existing content panels stay opaque so decorative marks cannot obscure copy or images.
