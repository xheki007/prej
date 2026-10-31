import unittest,hashlib,json
from pathlib import Path
from lxml import html
ROOT=Path(__file__).resolve().parents[1]
class VideoTests(unittest.TestCase):
 def test_approved_v2_bytes_and_localized_metadata(self):
  media=ROOT/'assets/prej-workflow-v2-en-48s.mp4'
  self.assertTrue(media.exists(),'Missing approved v2 media')
  self.assertEqual(hashlib.sha256(media.read_bytes()).hexdigest(),'b7fd2533241b932cd816a3702178fd787186f0d987df2415b9052e83ded5d137')
  for lang in ['sq','en','de','it']:
   entry=json.loads((ROOT/'assets/workflow-v2-manifest.json').read_text())[lang]
   self.assertEqual(hashlib.sha256((ROOT/'assets'/entry['file']).read_bytes()).hexdigest(),entry['sha256'])
   d=html.fromstring((ROOT/lang/'index.html').read_text());video=d.get_element_by_id('workflow-video')
   self.assertEqual(video.get('data-src'),f'/assets/prej-workflow-v2-{lang}-48s.mp4');self.assertIsNone(video.get('src'))
   self.assertEqual(video.get('poster'),f'/assets/prej-workflow-v2-{lang}-poster.webp')
   self.assertEqual((video.get('width'),video.get('height')),('1280','720'))
   film=d.get_element_by_id('workflow-film');self.assertNotIn('60',film.text_content());self.assertNotIn('01:00',film.text_content())
   self.assertIn('00:48',film.text_content());self.assertNotIn('60',d.xpath('//button[@class="workflow-play js-only"]/@aria-label')[0])
   self.assertTrue((ROOT/f'assets/prej-workflow-v2-{lang}-poster.webp').is_file())
if __name__=='__main__':unittest.main()
