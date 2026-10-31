import unittest,json
from pathlib import Path
from lxml import html
ROOT=Path(__file__).resolve().parents[1]
LANGS=('sq','en','de','it')
SLUGS=('mobile-app-development','web-platform-development','api-integrations')
class SearchCoverageTests(unittest.TestCase):
 def test_home_has_specific_service_heading(self):
  terms={'sq':'softuer','en':'software','de':'Software','it':'Software'}
  for lang in LANGS:
   d=html.fromstring((ROOT/lang/'index.html').read_text())
   self.assertIn(terms[lang].lower(),d.xpath('//h1')[0].text_content().lower())
 def test_service_coverage_and_schema(self):
  for lang in LANGS:
   for slug in SLUGS:
    with self.subTest(lang=lang,slug=slug):
     d=html.fromstring((ROOT/lang/'services'/slug/'index.html').read_text())
     faqs=d.xpath('//section[@class="service-faq"]/details')
     self.assertGreaterEqual(len(faqs),5)
     self.assertTrue(all(len(x.xpath('./p')[0].text_content())>100 for x in faqs))
     self.assertGreaterEqual(len(d.xpath('//article[@class="service-feature"]')),5)
     data=[json.loads(s) for s in d.xpath('//script[@type="application/ld+json"]/text()')]
     service=[x for x in data if x.get('@type')=='Service'];self.assertEqual(len(service),1)
     self.assertEqual(service[0]['url'],f'https://prej-tech.com/{lang}/services/{slug}/')
     self.assertEqual(service[0]['name'],d.xpath('//h1')[0].text_content())
     self.assertNotIn('offers',service[0]);self.assertNotIn('aggregateRating',service[0])
     crumbs=[x for x in data if x.get('@type')=='BreadcrumbList'];self.assertEqual(len(crumbs),1)
     self.assertEqual(crumbs[0]['itemListElement'][-1]['item'],service[0]['url'])
     self.assertFalse(d.xpath('//meta[@name="keywords"]'))
 def test_case_does_not_inherit_service_schema(self):
  for lang in LANGS:
   d=html.fromstring((ROOT/lang/'projects/home-of-dance/index.html').read_text())
   data=[json.loads(s) for s in d.xpath('//script[@type="application/ld+json"]/text()')]
   self.assertFalse([x for x in data if x.get('@type')=='Service'])
if __name__=='__main__':unittest.main()
