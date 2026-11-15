# PREJ Taxi release preparation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Prepare truthful public support/privacy pages and the complete two-app store packet while D-U-N-S is pending.

**Architecture:** Add an isolated static `/taxi/` area to the existing corporate GitHub Pages site. Generate three languages from structured copy; keep release claims and retained-data decisions explicit. The existing native chat owns binaries, mobile links, native permissions and real screenshots.

**Tech Stack:** Python standard library, static HTML/CSS, existing lxml tests, PNG/Sharp release exports.

**Spec:** `docs/superpowers/specs/2026-11-15-taxi-release-pages.md`

## Global Constraints

- Preserve existing corporate pages, `CNAME`, source assets and all production records.
- No new paid services, developer account, fabricated screenshots or Production submission.
- No secret material, identity documents, private test data or signing credentials in source.
- `/taxi/privacy/`, `/taxi/delete-account/`, `/taxi/support/` with Albanian default and English/German variants.
- No false send/delete confirmation or invented retention/legal approval.

## Review Focus

- Without JavaScript or an email handler, the user still sees the address and complete request instructions.
- A shared Rider/Driver account requires explicit deletion scope; disabling login alone is not erasure.
- App-specific location behavior and SDK data collection must match the shipped native build.
- An unavailable URL or draft privacy policy must not be mistaken for a completed Play prerequisite.
- Screenshots must come from the actual release candidate and contain no real personal information.

### Task 1: Static support and deletion request pages

**Files:** `scripts/taxi_pages.py`, `i18n/taxi-{sq,en,de}.json`, `taxi/taxi.css`, generated `taxi/**/index.html`, `tests/test_taxi_pages.py`.

**Interfaces:** `build_taxi_pages(root=ROOT)` creates nine static routes; `page_path(slug, lang)` defines canonical and reciprocal language links. Contact links use a fixed public address and an empty request template.

- [x] Add behavior tests for no-login access, no-script/manual fallback, email draft semantics, local links, per-language canonical URLs and visible draft status.
- [x] Run the tests and observe missing-page failures.
- [x] Implement the generator, source copy and mobile-first styling.
- [x] Run focused tests and the existing corporate suite.
- [x] Visually inspect desktop/mobile layouts and the mailto target without sending a message.

### Task 2: Privacy and operating-policy review

**Files:** `docs/taxi-privacy-operations.md`, `i18n/taxi-*.json`, release packet Data Safety worksheet.

- [x] Map source-confirmed data types, sharing and location modes to the actual app behavior.
- [x] Record unresolved retention, erasure execution, SDK/provider and hosting decisions without claiming completion.
- [ ] Prepare concrete final policy changes for owner review, then obtain only the missing decisions. Proposal and draft prepared; owner asked about 30-day request handling and financial retention.
- [ ] Publish only the authorized factual pages and verify HTTP content from the live domain.

### Task 3: Store packet and native integration

**Files:** `../prej-platform/outputs/play-release-coordination-20261115/` and existing brand exports.

- [x] Prepare SQ/EN/DE titles, short/full descriptions and image manifests for both apps.
- [ ] Validate dimensions, copy limits, hashes and privacy-safe screenshots supplied by the native chat.
- [ ] Integrate its signing/build/test handoff. Keep unresolved external prerequisites as blockers.
- [ ] Request one fresh focused review, resolve substantive findings, record real checks in PREJ.

## Execution ledger

- Corporate repo cloned from existing public `xheki007/prej`; no existing local edits in that checkout.
- Existing testing chat contacted with native ownership and stable URL contract; it is finishing the authorized Samsung cash-trip test first.
- D-U-N-S request already sent with explicit approval; organization conversion remains pending.
- Task 1 complete: missing-page tests observed failing, then all 29 corporate tests passed with `.venv/Scripts/python.exe -X utf8 -m unittest discover -s tests`. UTF-8 mode is required by existing tests on Windows; no production encoding behavior changed.
- Desktop and 390px viewport inspected in browser; German deletion route has no horizontal overflow, language navigation preserves page type, privacy draft is visible. No email sent.
- Store exporter validated 18 text fields and 4 PNG assets with hashes. It explicitly reports `productionReady: false` and leaves screenshots/AAB as blockers.
- Fresh read-only review by `/root/release_review`: no code/content defects in this preparation scope; 3 focused tests passed and assets checked. Final legal policy, actual erasure, production hosting/providers, public availability and native handoff were not certified.
- Ruling: those final release concerns remain open prerequisites, not waived findings. Publishing a draft is not equivalent to satisfying Play policy, and the cost of treating it that way would be a misleading release declaration.
