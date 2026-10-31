import json,unittest
from pathlib import Path
from urllib.parse import urlsplit
from lxml import html,etree
ROOT=Path(__file__).resolve().parents[1]
LANGS=('sq','en','de','it')
SUFFIX='projects/home-of-dance/'
class CaseStudyTests(unittest.TestCase):
 def test_four_complete_case_studies(self):
  for lang in LANGS:
   with self.subTest(lang=lang):
    file=ROOT/lang/SUFFIX/'index.html';self.assertTrue(file.exists(),'Missing Home of Dance case study')
    d=html.fromstring(file.read_text());url=f'https://prej-tech.com/{lang}/{SUFFIX}'
    self.assertEqual(d.get('lang'),lang);self.assertEqual(len(d.xpath('//h1')),1)
    self.assertTrue(d.xpath('//*[@id="top"]'))
    for value in d.xpath('//a[starts-with(@href,"#")]/@href'):self.assertTrue(d.xpath('//*[@id=$id]',id=value[1:]),value)
    self.assertEqual(d.xpath('//link[@rel="canonical"]/@href'),[url])
    self.assertEqual(d.xpath('//meta[@property="og:url"]/@content'),[url])
    alts=dict(zip(d.xpath('//link[@hreflang]/@hreflang'),d.xpath('//link[@hreflang]/@href')))
    self.assertEqual(alts,{**{l:f'https://prej-tech.com/{l}/{SUFFIX}' for l in LANGS},'x-default':f'https://prej-tech.com/en/{SUFFIX}'})
    self.assertGreater(len(d.xpath('//main')[0].text_content().split()),400)
    self.assertEqual(len(d.xpath('//main//img')),2)
    self.assertTrue(d.xpath('//a[@href=$href]',href=f'/{lang}/services/web-platform-development/'))
    self.assertTrue(d.xpath('//a[@href="https://backoffice.homeofdance.de/buchen"]'))
    for attr in ['href','src']:
     for value in d.xpath('//@'+attr):
      if value.startswith('/'):
       u=urlsplit(value);p=ROOT/u.path.lstrip('/');p=p/'index.html' if p.is_dir() else p
       self.assertTrue(p.exists(),value)
       if u.fragment:self.assertTrue(html.fromstring(p.read_text()).xpath('//*[@id=$id]',id=u.fragment),value)
 def test_case_discovery_links(self):
  for lang in LANGS:
   target=f'/{lang}/{SUFFIX}'
   for path in [ROOT/lang/'index.html',ROOT/lang/'services/web-platform-development/index.html']:
    self.assertTrue(html.fromstring(path.read_text()).xpath('//a[@href=$url]',url=target))
 def test_localized_case_content_shape(self):
  def shape(value):
   if isinstance(value,dict):return {k:shape(v) for k,v in value.items()}
   if isinstance(value,list):return [shape(v) for v in value]
   self.assertTrue(isinstance(value,str) and value.strip());return 'text'
  self.assertTrue((ROOT/'i18n/case-home-of-dance-en.json').exists(),'Missing localized case content')
  source=json.loads((ROOT/'i18n/case-home-of-dance-en.json').read_text())
  for lang in LANGS:self.assertEqual(shape(source),shape(json.loads((ROOT/f'i18n/case-home-of-dance-{lang}.json').read_text())))
 def test_sitemap_has_twenty_urls(self):
  urls=etree.parse(str(ROOT/'sitemap.xml')).xpath('//*[local-name()="loc"]/text()')
  self.assertEqual(len(urls),20)
  for lang in LANGS:self.assertIn(f'https://prej-tech.com/{lang}/{SUFFIX}',urls)
if __name__=='__main__':unittest.main()
