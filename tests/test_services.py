import unittest,json
from pathlib import Path
from urllib.parse import urlsplit
from lxml import html,etree
ROOT=Path(__file__).resolve().parents[1]
LANGS=('sq','en','de','it')
SLUGS=('mobile-app-development','web-platform-development','api-integrations')
class ServiceTests(unittest.TestCase):
 def test_complete_localized_service_pages(self):
  titles=set()
  for lang in LANGS:
   for slug in SLUGS:
    with self.subTest(lang=lang,slug=slug):
     path=ROOT/lang/'services'/slug/'index.html';self.assertTrue(path.exists(),'Missing service page')
     d=html.fromstring(path.read_text());base=f'https://prej-tech.com/{lang}/services/{slug}/'
     self.assertEqual(d.get('lang'),lang);self.assertEqual(d.xpath('//link[@rel="canonical"]/@href'),[base])
     alts=dict(zip(d.xpath('//link[@hreflang]/@hreflang'),d.xpath('//link[@hreflang]/@href')))
     self.assertEqual(alts,{**{l:f'https://prej-tech.com/{l}/services/{slug}/' for l in LANGS},'x-default':f'https://prej-tech.com/en/services/{slug}/'})
     self.assertEqual(len(d.xpath('//h1')),1);self.assertNotIn(d.find('head/title').text,titles);titles.add(d.find('head/title').text)
     self.assertGreater(len(d.xpath('//main')[0].text_content().split()),300)
     self.assertEqual(len(d.xpath('//div[@class="language-options"]/a')),8)
     self.assertTrue(d.xpath('//a[@href=$url]',url=f'/{lang}/#contact'))
     self.assertNotIn('/app.js',path.read_text())
     for url in d.xpath('//@href|//@src'):
      if url.startswith('/'):
       u=urlsplit(url);target=ROOT/u.path.lstrip('/');target=target/'index.html' if target.is_dir() else target
       self.assertTrue(target.exists(),url)
       if u.fragment:self.assertTrue(html.fromstring(target.read_text()).xpath('//*[@id=$id]',id=u.fragment),url)
 def test_service_translation_structure(self):
  def shape(value):
   if isinstance(value,dict):return {k:shape(v) for k,v in value.items()}
   if isinstance(value,list):return [shape(v) for v in value]
   self.assertTrue(isinstance(value,str) and value.strip());return 'text'
  baseline=json.loads((ROOT/'i18n/services-en.json').read_text())
  for lang in LANGS:
   translated=json.loads((ROOT/f'i18n/services-{lang}.json').read_text())
   self.assertEqual(shape(baseline),shape(translated))
   for slug in SLUGS:
    for key in ['projectId','projectName']:self.assertEqual(translated['services'][slug][key],baseline['services'][slug][key])
 def test_sitemap_contains_all_sixteen_canonical_pages(self):
  doc=etree.parse(str(ROOT/'sitemap.xml'));urls=doc.xpath('//*[local-name()="loc"]/text()')
  expected=[f'https://prej-tech.com/{l}/' for l in LANGS]+[f'https://prej-tech.com/{l}/services/{s}/' for l in LANGS for s in SLUGS]
  self.assertEqual(set(urls),set(expected));self.assertEqual(len(urls),16)
 def test_homepages_link_to_services(self):
  for lang in LANGS:
   d=html.fromstring((ROOT/lang/'index.html').read_text())
   for slug in SLUGS:self.assertTrue(d.xpath('//a[@href=$url]',url=f'/{lang}/services/{slug}/'))
if __name__=='__main__':unittest.main()
