"""Add the approved, purely decorative ambient data paths to existing sections."""
from lxml import etree
SVG='http://www.w3.org/2000/svg'
ROUTES=(
 'M0 180 H160 L240 80 H510 L600 200 H840 L980 65 H1440',
 'M0 700 H170 L330 810 H730 L900 660 H1200 L1440 820',
 'M1360 0 V280 L1240 390 V600 H1440',
 'M45 100 V400 L130 470 V800 L280 900',
)
def add_background(doc):
 head=doc.find('head')
 if not head.xpath('./link[contains(@href,"background-motion.css")]'):
  etree.SubElement(head,'link',rel='stylesheet',href='/background-motion.css?v=1')
 if not head.xpath('./script[contains(@src,"background-motion.js")]'):
  etree.SubElement(head,'script',src='/background-motion.js?v=1',defer='defer')
 for host in doc.xpath('//main/*[self::section or self::div] | //body/footer'):
  if host.xpath('./div[@class="ambient-layer"]'):continue
  host.set('class',(host.get('class','')+' ambient-host').strip())
  layer=etree.Element('div',{'class':'ambient-layer','aria-hidden':'true'})
  host.insert(0,layer)
  svg=etree.SubElement(layer,'{'+SVG+'}svg',nsmap={None:SVG},viewBox='0 0 1440 900',preserveAspectRatio='none',focusable='false')
  for i,path in enumerate(ROUTES):
   group=etree.SubElement(svg,'{'+SVG+'}g',{'class':f'ambient-route ambient-route-{i+1}'})
   etree.SubElement(group,'{'+SVG+'}path',{'d':path,'class':'ambient-track','vector-effect':'non-scaling-stroke'})
   etree.SubElement(group,'{'+SVG+'}path',{'d':path,'class':'ambient-pulse','pathLength':'1000','vector-effect':'non-scaling-stroke'})
