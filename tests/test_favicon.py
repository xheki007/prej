import unittest
from pathlib import Path
from lxml import html
import struct
ROOT=Path(__file__).resolve().parents[1]
class FaviconTests(unittest.TestCase):
 def test_approved_icon_on_every_page(self):
  pages=[ROOT/'index.html']+[p for lang in ('sq','en','de','it') for p in (ROOT/lang).rglob('index.html')]
  self.assertEqual(len(pages),21)
  for p in pages:
   d=html.fromstring(p.read_text())
   self.assertEqual(d.xpath('//link[@rel="icon"]/@href'),['/assets/favicon-v2.png'])
   self.assertEqual(d.xpath('//link[@rel="icon"]/@sizes'),['48x48'])
   self.assertEqual(d.xpath('//link[@rel="icon"]/@type'),['image/png'])
   self.assertEqual(d.xpath('//link[@rel="apple-touch-icon"]/@href'),['/assets/apple-touch-icon-v2.png'])
 def test_icon_dimensions_and_legacy_container(self):
  for file,size in [('assets/favicon-v2.png',48),('assets/apple-touch-icon-v2.png',180)]:
   self.assertTrue((ROOT/file).exists(),file)
   data=(ROOT/file).read_bytes();self.assertEqual(data[:8],b'\x89PNG\r\n\x1a\n');self.assertEqual(struct.unpack('>II',data[16:24]),(size,size))
  self.assertTrue((ROOT/'favicon.ico').exists())
  data=(ROOT/'favicon.ico').read_bytes();self.assertEqual(struct.unpack('<HHH',data[:6]),(0,1,3));self.assertEqual({(data[6+i*16],data[7+i*16]) for i in range(3)},{(16,16),(32,32),(48,48)})
if __name__=='__main__':unittest.main()
