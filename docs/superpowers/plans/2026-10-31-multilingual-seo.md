# PREJ multilingual SEO implementation plan

Goal: publish complete static SQ/EN/DE/IT HTML while preserving the current
visual design, honest project stages, contact behaviour and CNAME.

Architecture: one existing HTML template, locale dictionaries, a deterministic
Python/lxml generator, committed output served by GitHub Pages. Native links
and a details-based language picker work without JavaScript. English is the
international/default page; explicit URLs never depend on browser storage.

- [x] Write static-page and SEO tests; confirm failures for missing pages/sitemap.
- [x] Translate visible content, accessible labels and interaction messages.
- [x] Generate pages, canonical/hreflang/OG/Organization data and sitemap/robots.
- [x] Preserve legacy queries and fragments; retain interactive product/form flows.
- [x] Produce responsive hero, smaller lossless logo and small favicon derivatives.
- [x] Run generator, static tests and JavaScript syntax validation.
- [ ] Run Chromium desktop/mobile and no-JS journeys; inspect screenshots.
- [ ] Independent review before any merge/deployment.

Review focus: mixed-language content; mobile picker fit; query/hash navigation;
form feedback after close/reopen; correct portfolio pilot/prototype boundaries.
No new services, tracking, fabricated offices, geography doorway pages or claims.
