"""Localized European B2B SEO checks for published static pages."""
import json
import unittest
from pathlib import Path
from lxml import html

ROOT=Path(__file__).resolve().parents[1]
LANGS=('en','de','it','sq')
SERVICES=('mobile-app-development','web-platform-development','api-integrations')
EUROPE={'en':'Europe','de':'Europa','it':'Europa','sq':'Evrop'}

class EuropeSEOTests(unittest.TestCase):
 def test_homepages_are_localized_and_canonical(self):
  data=json.loads((ROOT/'i18n/search-home.json').read_text())
  for lang in LANGS:
   with self.subTest(language=lang):
    doc=html.fromstring((ROOT/lang/'index.html').read_text())
    url='https://prej-tech.com/' if lang=='en' else f'https://prej-tech.com/{lang}/'
    self.assertEqual(doc.xpath('//link[@rel="canonical"]/@href'),[url])
    self.assertEqual(doc.xpath('//title/text()'),[data[lang]['title']])
    self.assertEqual(doc.xpath('//meta[@name="description"]/@content'),[data[lang]['description']])
    self.assertEqual(doc.xpath('//meta[@property="og:description"]/@content'),[data[lang]['description']])
    self.assertEqual(doc.xpath('//p[@class="hero-intro"]/text()'),[data[lang]['intro']])
    self.assertIn(EUROPE[lang].lower(),data[lang]['intro'].lower())
    self.assertEqual(doc.xpath('//link[@hreflang="x-default"]/@href'),['https://prej-tech.com/'])
    self.assertFalse(doc.xpath('//meta[@name="keywords"]'))
  root=(ROOT/'index.html').read_text()
  self.assertEqual(root,(ROOT/'en/index.html').read_text())

 def test_localized_services_describe_europe_and_have_schema(self):
  for lang in LANGS:
   content=json.loads((ROOT/f'i18n/services-{lang}.json').read_text())
   for slug in SERVICES:
    with self.subTest(language=lang,service=slug):
     service=content['services'][slug]
     doc=html.fromstring((ROOT/lang/'services'/slug/'index.html').read_text())
     self.assertEqual(doc.xpath('//meta[@name="description"]/@content'),[service['description']])
     self.assertEqual(doc.xpath('//meta[@property="og:description"]/@content'),[service['description']])
     self.assertEqual(doc.xpath('//p[@class="service-lead"]/text()'),[service['intro']])
     self.assertIn(EUROPE[lang].lower(),service['intro'].lower())
     schema=json.loads(doc.xpath('//script[@id="service-schema"]/text()')[0])
     self.assertEqual(schema['areaServed'],{'@type':'Continent','name':'Europe'})
     self.assertEqual(schema['description'],service['description'])
     self.assertEqual(schema['url'],f'https://prej-tech.com/{lang}/services/{slug}/')
     self.assertNotIn('aggregateRating',schema)

if __name__=='__main__':unittest.main()
