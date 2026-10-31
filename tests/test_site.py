import unittest,json
from pathlib import Path
from lxml import html
ROOT=Path(__file__).resolve().parents[1]
LANGS=('sq','en','de','it')
class SiteTests(unittest.TestCase):
 def test_static_locales_and_seo(self):
  for lang in LANGS:
   with self.subTest(lang=lang):
    file=ROOT/lang/'index.html'; self.assertTrue(file.exists(),f'Missing static {lang} page')
    doc=html.fromstring(file.read_text()); self.assertEqual(doc.get('lang'),lang)
    self.assertEqual(doc.xpath('//link[@rel="canonical"]/@href'),[f'https://prej-tech.com/{lang}/'])
    alternates=dict(zip(doc.xpath('//link[@hreflang]/@hreflang'),doc.xpath('//link[@hreflang]/@href')))
    self.assertEqual(alternates,{**{l:f'https://prej-tech.com/{l}/' for l in LANGS},'x-default':'https://prej-tech.com/en/'})
    self.assertEqual(len(doc.xpath('//h1')),1)
    self.assertNotIn('60',doc.xpath('//*[@id="workflow-film-title"]')[0].text_content())
    self.assertTrue(doc.xpath('//form[@id="brief-form" and @novalidate]'))
    runtime=json.loads(doc.xpath('//script[@id="locale-messages"]/text()')[0])
    self.assertIn('requiredEmail',runtime)
    self.assertIn('invalidEmail',runtime)
    self.assertEqual(len(doc.xpath('//article[contains(@class,"portfolio-card")]')),7)
    self.assertFalse(doc.xpath('//@data-sq'))
    self.assertEqual(len(doc.xpath('//div[contains(@class,"language-switch")]//a')),8)
    self.assertNotIn('github.io',file.read_text())
    self.assertEqual(doc.xpath('//script[@src]/@src'),['/app.js?v=4','/hero-motion.js?v=1'])
    for attr in ('href','src','poster','data-src'):
     for url in doc.xpath('//@'+attr):
      if url.startswith('/'):
       p=ROOT/url.lstrip('/').split('?')[0].split('#')[0]
       self.assertTrue(p.exists(),url)
      elif url.startswith('#'): self.assertTrue(doc.xpath('//*[@id=$id]',id=url[1:]),url)
 def test_translation_coverage_and_runtime(self):
  en=json.loads((ROOT/'i18n/en.json').read_text())
  base=json.loads((ROOT/'i18n/runtime-en.json').read_text())
  for lang in LANGS:
   messages=json.loads((ROOT/f'i18n/{lang}.json').read_text())
   self.assertEqual(set(en),set(messages))
   self.assertTrue(all(messages.values()))
   runtime=json.loads((ROOT/f'i18n/runtime-{lang}.json').read_text())
   self.assertEqual(set(base),set(runtime))
   self.assertIn('{count}',runtime['projectsShown'])
 def test_root_and_domain_preserved(self):
  root=html.fromstring((ROOT/'index.html').read_text())
  self.assertEqual(root.xpath('//link[@rel="canonical"]/@href'),['https://prej-tech.com/en/'])
  self.assertEqual((ROOT/'CNAME').read_text().strip(),'prej-tech.com')
 def test_sitemap(self):
  self.assertTrue((ROOT/'sitemap.xml').exists())
  self.assertIn('https://prej-tech.com/sitemap.xml',(ROOT/'robots.txt').read_text())
if __name__=='__main__':unittest.main()
