# PREJ — Software Engineering

Company website for PREJ SH.P.K., with the Midnight visual identity and Albanian / English / German / Italian content.

**Website:** https://prej-tech.com/

## Publishing
GitHub Pages serves the root of the `main` branch. Push an update to `main` to publish it automatically. `.nojekyll` keeps the site as plain static files. The custom domain is configured by `CNAME`; preserve this file.

## Files
- `index.html` — content, Albanian text alternatives and page metadata.
- `style.css` — responsive desktop and mobile design.
- `portfolio.css` — project illustrations, responsive catalogue and reduced-motion-aware animation.
- `workflow-video.css` — the responsive, click-to-play workflow film in “How we work”.
- `app.js` — language selection, navigation, project filters, scroll reveals and project enquiry draft.
- `assets/` — approved PREJ logo assets and connected-systems illustration.

## Preview locally
Run `python -m http.server 4174` from this directory, then open `http://localhost:4174`.

## Contact behaviour
The enquiry form opens a draft in the visitor's email application; the visitor reviews and sends it. The website does not send or store form contents. A copy option is provided. No language preference is stored in the browser; language is explicit in the URL. No marketing trackers or externally hosted font dependencies are included.

The catalogue describes seven projects: PREJ TaxiApp, Home of Dance, TORQENIX, AKADEMIA, PREJ WiFi, PREJ AI Software Factory and Komisionerët. Each identifies its development stage; interface illustrations explain the products and are not live application screens. No client records or internal project files are published.

Motion uses finite entrances and hover effects, honors `prefers-reduced-motion`, and does not hide content when JavaScript is unavailable. The eight AI agent roles assist the human engineering lead; they are not represented as employees or independent reviewers.

The approved 48-second workflow film uses PREJ motion graphics, original instrumental music and localized on-screen text, without narration or subtitle tracks. Each SQ/EN/DE/IT page selects its matching MP4 and poster through a versioned filename. Only the poster loads initially; JavaScript attaches the media source after Play. Native controls, inline mobile playback and localized direct-file fallbacks remain available. The earlier film is retained only as a rollback asset.


## Multilingual static build
The public domain is **https://prej-tech.com**. Four crawlable pages live at
`/sq/`, `/en/`, `/de/`, and `/it/`; `/` contains the English page with `/en/` as
its canonical. Each locale is self-canonical and links reciprocally to all
four languages; `x-default` is `/en/`. Legacy `?lang=sq` / `?lang=en` links
are redirected client-side, preserving other query parameters and fragments.
Without JavaScript the root remains a complete English page with language links.
No browser language detection or preference storage overrides explicit URLs.

Edit `i18n/template.html` and the locale JSON dictionaries, then run:

```sh
python -m pip install -r requirements-dev.txt
python scripts/build.py
python -m unittest discover -s tests
node --check app.js
python -m http.server 4174
# In another shell, after installing a Playwright Chromium browser:
python tests/browser.py
```

The build uses Python/lxml; the published website has no build/runtime
framework dependency. Generated HTML, sitemap.xml and robots.txt are committed
because GitHub Pages serves main/root directly. Do not edit generated pages.
`tests/browser.py` checks three widths, all languages, native language links,
no-JavaScript access, filters, project details, enquiry-dialog interruptions,
manual-copy fallback and legacy links. It never sends an enquiry.

Flags are decorative language cues, not service-country claims. Native names
remain visible and accessible. No regional offices, clients, ratings, delivery
results or new product-readiness claims are added. Structured data contains
only the company name and existing public contact/location facts.

Image derivatives retain the original artwork and original assets remain in
the repository: responsive WebP hero at 640/1280px, lossless 624px WebP logo,
and 48px PNG favicon. The illustrative workflow film has matching localized on-screen text and music,
explicitly labelled in every locale, and loads only after Play.

## Service pages
Each locale now includes three substantial service pages under
`/{locale}/services/`: `mobile-app-development/`,
`web-platform-development/`, and `api-integrations/`.
`i18n/services-{locale}.json` contains their localized copy;
`scripts/services.py` renders the shared layout after the home pages.
Homepage capability cards retain their existing project/contact links and add
service-detail links. Every service page links to related services, the
relevant portfolio item and the localized home contact section. The existing
enquiry form remains the single enquiry implementation.

`service.css` extends the current visual identity; `service.js` handles only
progressive menu and language-picker behavior. Service content and navigation
remain usable without JavaScript. The sitemap contains 20 canonical URLs
(four homepages, twelve service pages and four Home of Dance case-study pages), with reciprocal language alternates.
The service copy describes intended project scope and process, not a delivery
promise or a claim of commercial deployment for portfolio work.


## Home of Dance case study
`/{locale}/projects/home-of-dance/` presents the custom backoffice and public
course-registration workflow in all four languages. `scripts/cases.py` renders
it from `i18n/case-home-of-dance-{locale}.json`, using the shared service chrome
and `case-study.css`. The Home of Dance portfolio entry and web-platform service
link to the case study. Other project stages remain unchanged.

The project owner confirmed permission for public use of the name, logo and
privacy-safe interface images. The two approved WebP screenshots show only the
public German course catalogue and an empty participant/guardian request form;
they contain no private participant records. Captions explain the original
interface language and that availability/prices can change. Source interface:
https://backoffice.homeofdance.de/buchen

The copy is grounded in the inspected public workflow and backoffice inventory;
electronic contract signing is owner-confirmed functionality, not a legal
assurance or a claim that a signature transaction was tested. Registration
requests require office review and confirmation. Course/payment selection does
not itself confirm a contract or execute payment. No client-side registration,
payment or signing submission is made by `tests/case_browser.py`.
