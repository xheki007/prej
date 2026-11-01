import unittest
from pathlib import Path
from lxml import html
ROOT=Path(__file__).resolve().parents[1]
class BackgroundTests(unittest.TestCase):
 def test_all_pages_have_decorative_background(self):
  for p in [ROOT/'index.html',*ROOT.glob('*/index.html'),*ROOT.glob('*/services/*/index.html'),*ROOT.glob('*/projects/*/index.html')]:
   d=html.fromstring(p.read_text())
   self.assertEqual(len(d.xpath('//link[@href="/background-motion.css?v=1"]')),1,str(p))
   self.assertEqual(len(d.xpath('//script[@src="/background-motion.js?v=1"]')),1,str(p))
   for host in d.xpath('//main/*[self::section or self::div] | //body/footer'):
    layers=host.xpath('./div[@class="ambient-layer"]')
    self.assertEqual(len(layers),1,str(p))
    self.assertEqual(layers[0].get('aria-hidden'),'true')
    self.assertFalse(layers[0].xpath('.//*[@tabindex or @href]'))
    self.assertTrue(layers[0].xpath('.//*[local-name()="path"]'))
 def test_runtime_is_private_and_motion_safe(self):
  js=(ROOT/'background-motion.js').read_text();css=(ROOT/'background-motion.css').read_text()
  for word in ['prefers-reduced-motion','IntersectionObserver','visibilitychange','pagehide','pageshow']:self.assertIn(word,js)
  for word in ['fetch(', 'localStorage','sessionStorage','setInterval','requestAnimationFrame']:self.assertNotIn(word,js)
  self.assertIn('pointer-events:none',css);self.assertIn('prefers-reduced-motion',css)
  self.assertIn('animation-play-state:paused',css)
