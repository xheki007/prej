import unittest
from pathlib import Path
from urllib.parse import urlparse, parse_qs, unquote
from lxml import html

ROOT = Path(__file__).resolve().parents[1]
LANGS = ('sq', 'en', 'de')
SLUGS = ('privacy', 'delete-account', 'support')

def route(slug, lang):
    return f'/taxi/{slug}/' + (f'{lang}/' if lang != 'sq' else '')

class TaxiPagesTests(unittest.TestCase):
    def doc(self, slug, lang):
        return html.fromstring((ROOT / route(slug, lang).lstrip('/') / 'index.html').read_text(encoding='utf-8'))

    def test_static_localized_routes_and_assets(self):
        for slug in SLUGS:
            for lang in LANGS:
                with self.subTest(slug=slug, lang=lang):
                    doc = self.doc(slug, lang)
                    self.assertEqual(doc.get('lang'), lang)
                    self.assertEqual(len(doc.xpath('//h1')), 1)
                    self.assertEqual(doc.xpath('//link[@rel="canonical"]/@href'), ['https://prej-tech.com' + route(slug, lang)])
                    alternates = dict(zip(doc.xpath('//link[@hreflang]/@hreflang'), doc.xpath('//link[@hreflang]/@href')))
                    self.assertEqual(alternates, {**{l: 'https://prej-tech.com' + route(slug, l) for l in LANGS}, 'x-default': 'https://prej-tech.com' + route(slug, 'sq')})
                    self.assertTrue(doc.xpath('//main[@id="main"]'))
                    self.assertIn('PREJ SH.P.K.', doc.text_content())
                    self.assertFalse(doc.xpath('//form|//script|//iframe'))
                    for link in doc.xpath('//@href|//@src'):
                        if link.startswith('/'):
                            self.assertTrue((ROOT / link.lstrip('/').split('#')[0]).exists(), link)
                        elif link.startswith('#'):
                            self.assertTrue(doc.xpath('//*[@id=$id]', id=link[1:]))

    def test_deletion_email_draft_and_manual_fallback(self):
        for lang in LANGS:
            doc = self.doc('delete-account', lang)
            link = doc.xpath('//a[@id="request-email"]/@href')[0]
            parsed = urlparse(link)
            self.assertEqual(parsed.scheme, 'mailto')
            self.assertEqual(parsed.path, 'ferizixhevdet@gmail.com')
            query = parse_qs(parsed.query)
            self.assertIn('PREJ', query['subject'][0])
            self.assertIn('PREJ Taxi', query['body'][0])
            self.assertIn('PREJ Driver', query['body'][0])
            self.assertNotIn('cc', query)
            self.assertNotIn('bcc', query)
            self.assertTrue(doc.xpath('//*[@id="manual-email"]'))
            self.assertIn('ferizixhevdet@gmail.com', doc.xpath('//*[@id="manual-email"]')[0].text_content())
            self.assertTrue(doc.xpath('//*[@id="send-explanation"]'))
            self.assertTrue(doc.xpath('//*[@id="request-scope"]'))
            self.assertTrue(doc.xpath('//*[@id="sensitive-warning"]'))
            self.assertFalse(doc.xpath('//*[@role="alert" or @role="status"]'))

    def test_privacy_draft_is_visible_and_app_scope_is_explicit(self):
        for lang in LANGS:
            doc = self.doc('privacy', lang)
            self.assertTrue(doc.xpath('//*[@id="policy-status" and @data-status="draft"]'))
            self.assertTrue(doc.xpath('//meta[@name="robots" and @content="noindex, follow"]'))
            self.assertIn('PREJ Taxi', doc.text_content())
            self.assertIn('PREJ Driver', doc.text_content())
            for section in ('location', 'data', 'sharing', 'retention', 'rights'):
                self.assertTrue(doc.xpath('//*[@id=$id]', id=section))

if __name__ == '__main__':
    unittest.main()
