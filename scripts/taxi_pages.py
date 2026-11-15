"""Build the isolated PREJ mobile-app support area. No network or user-data input."""
from pathlib import Path
import json
from html import escape
from urllib.parse import urlencode, quote

ROOT = Path(__file__).resolve().parents[1]
LANGUAGES = {'sq': 'Shqip', 'en': 'English', 'de': 'Deutsch'}
SLUGS = ('privacy', 'delete-account', 'support')
CONTACT = 'ferizixhevdet@gmail.com'
ORIGIN = 'https://prej-tech.com'


def page_path(slug, lang):
    return f'/taxi/{slug}/' + (f'{lang}/' if lang != 'sq' else '')


def build_taxi_pages(root=ROOT):
    for lang in LANGUAGES:
        data = json.loads((root / f'i18n/taxi-{lang}.json').read_text(encoding='utf-8'))
        ui = data['ui']
        for slug in SLUGS:
            page = data[slug]
            canonical = ORIGIN + page_path(slug, lang)
            alternates = ''.join(f'<link rel="alternate" hreflang="{code}" href="{ORIGIN}{page_path(slug, code)}">' for code in LANGUAGES)
            language_links = ''.join(f'<a lang="{code}" hreflang="{code}" href="{page_path(slug, code)}"' + (' aria-current="page"' if code == lang else '') + f'>{name}</a>' for code, name in LANGUAGES.items())
            nav = ''.join(f'<a href="{page_path(other, lang)}"' + (' aria-current="page"' if other == slug else '') + f'>{escape(data[other]["nav"])}</a>' for other in SLUGS)
            sections = ''.join(f'<section id="{escape(section["id"])}"><h2>{escape(section["title"])}</h2>' + ''.join(f'<p>{escape(p)}</p>' for p in section['paragraphs']) + '</section>' for section in page['sections'])
            draft = ''
            robots = ''
            if slug == 'privacy':
                draft = f'<aside id="policy-status" data-status="draft"><strong>{escape(page["draftTitle"])}</strong><p>{escape(page["draftText"])}</p></aside>'
                robots = '<meta name="robots" content="noindex, follow">'
            action = ''
            if slug == 'delete-account':
                email = 'mailto:' + CONTACT + '?' + urlencode({'subject': page['subject'], 'body': page['body']}, quote_via=quote)
                action = f'<div class="request-card"><a id="request-email" class="button" href="{escape(email, quote=True)}">{escape(page["button"])}</a><p id="send-explanation">{escape(page["sendExplanation"])}</p><div id="manual-email"><h2>{escape(page["manualTitle"])}</h2><p>{escape(page["manualText"])}</p><a class="email-address" href="mailto:{CONTACT}">{CONTACT}</a><pre>{escape(page["body"])}</pre></div></div>'
            content = f'''<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(page['title'])} | PREJ</title><meta name="description" content="{escape(page['intro'], quote=True)}">{robots}
<link rel="canonical" href="{canonical}">{alternates}<link rel="alternate" hreflang="x-default" href="{ORIGIN}{page_path(slug, 'sq')}">
<meta name="theme-color" content="#061725"><link rel="icon" type="image/png" href="/assets/favicon-v2.png"><link rel="stylesheet" href="/taxi/taxi.css">
</head><body><a class="skip-link" href="#main">{escape(ui['skip'])}</a>
<header><a class="brand" href="/{lang}/" aria-label="PREJ"><img src="/assets/prej-logo-dark.webp" width="624" height="208" alt="PREJ"></a><nav aria-label="{escape(ui['languages'])}">{language_links}</nav></header>
<main id="main"><div class="eyebrow">PREJ TAXI &amp; PREJ DRIVER</div><h1>{escape(page['title'])}</h1><p class="lead">{escape(page['intro'])}</p>
<nav class="page-nav" aria-label="{escape(ui['pages'])}">{nav}</nav>{draft}<div class="document">{sections}{action}</div>
<aside class="contact"><span>{escape(ui['contact'])}</span><strong>PREJ SH.P.K.</strong><a href="mailto:{CONTACT}">{CONTACT}</a><p>Mitrovicë, Kosovë</p></aside></main>
<footer><p>© 2026 PREJ SH.P.K.</p><a href="/{lang}/">{escape(ui['company'])} ↗</a><p>{escape(ui['updated'])}: 15.11.2026</p></footer></body></html>
'''
            target = root / page_path(slug, lang).lstrip('/') / 'index.html'
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding='utf-8')


if __name__ == '__main__':
    build_taxi_pages()
    print('Built 9 static PREJ app support pages (privacy remains a visible draft).')
