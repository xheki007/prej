# PREJ — Software Engineering

Company website for PREJ SH.P.K., with the Midnight visual identity and English / Albanian content.

**Website:** https://xheki007.github.io/prej/

## Publishing
GitHub Pages serves the root of the `main` branch. Push an update to `main` to publish it automatically. `.nojekyll` keeps the site as plain static files. A custom domain is not required.

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
The enquiry form opens a draft in the visitor's email application; the visitor reviews and sends it. The website does not send or store form contents. A copy option is provided. Only language preference is stored locally in the browser. No marketing trackers or externally hosted font dependencies are included.

The catalogue describes seven projects: PREJ TaxiApp, Home of Dance, TORQENIX, AKADEMIA, PREJ WiFi, PREJ AI Software Factory and Komisionerët. Each identifies its development stage; interface illustrations explain the products and are not live application screens. No client records or internal project files are published.

Motion uses finite entrances and hover effects, honors `prefers-reduced-motion`, and does not hide content when JavaScript is unavailable. The eight AI agent roles assist the human engineering lead; they are not represented as employees or independent reviewers.

The 60-second workflow film is an illustrative animation with a generic rear-view character, English captions and an original ambient score. It contains no personal portrait or client records. Only its lightweight poster loads with the page; JavaScript attaches the MP4 source after the visitor presses Play. Playback uses native controls, works inline on mobile and has a direct-file fallback when JavaScript is unavailable or playback fails. The title, button, description and accessibility labels follow the site's English / Albanian language selection.
