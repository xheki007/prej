# PREJ service-page implementation plan

Goal: provide useful, crawlable service-specific information in SQ/EN/DE/IT.
Architecture: three content records per locale, shared semantic premium layout,
static generated HTML, stable service slugs, existing home/contact workflows.

- [x] Write failing tests for 12 service pages, equivalent hreflang and 16 sitemap URLs.
- [x] Add substantial translated service content with accurate project boundaries.
- [x] Generate pages with unique metadata, breadcrumbs, links and native picker.
- [x] Add service links to homepage capabilities without removing existing links.
- [x] Run deterministic build/static checks; parent runs authorized CI browser QA.
- [ ] Independent content/visual review before parent-controlled publication.

No new offices, testimonials, results, ranking promises or services inferred.
The existing home enquiry form is reused via localized home#contact links rather
than duplicating its stateful script into a different page structure.
