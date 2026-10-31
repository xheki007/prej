from pathlib import Path
import unittest
from lxml import html
ROOT=Path(__file__).resolve().parents[1]
class HeroMotionTests(unittest.TestCase):
 def test_home_scene_without_motion_control(self):
  for lang in ('sq','en','de','it'):
   doc=html.fromstring((ROOT/lang/'index.html').read_text())
   stages=doc.xpath('//*[@class="hero-motion-stage"]')
   self.assertEqual(len(stages),1,'Shared image/overlay stage missing')
   stage=stages[0];img=stage.find('img')
   self.assertEqual((img.get('width'),img.get('height')),('1280','853'))
   svg=stage.find('svg');self.assertEqual(svg.get('viewbox') or svg.get('viewBox'),'0 0 1280 853')
   self.assertEqual(svg.get('aria-hidden'),'true')
   self.assertEqual([p.get('d') for p in svg.findall('.//path')],['M454 459 L584 408 L584 385','M743 500 L828 536'])
   self.assertFalse(doc.xpath('//button[@class="hero-motion-toggle"]'),'User requested no visible motion button')
   self.assertEqual(len(doc.xpath('//script[contains(@src,"hero-motion.js")]')),1)
 def test_not_loaded_on_other_pages(self):
  for page in list(ROOT.glob('*/services/*/index.html'))+list(ROOT.glob('*/projects/*/index.html')):
   self.assertNotIn('hero-motion',page.read_text())
if __name__=='__main__':unittest.main()
