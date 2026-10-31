"""Homepage-only progressive decorative motion; coordinates match the unchanged photograph."""
from lxml import html,etree
LABELS={
 'en':('Pause animation','Resume animation'),
 'sq':('Ndalo animacionin','Vazhdo animacionin'),
 'de':('Animation pausieren','Animation fortsetzen'),
 'it':('Metti in pausa l’animazione','Riprendi l’animazione'),
}
def add_hero_motion(doc,hero,lang):
 hero.set('width','1280');hero.set('height','853')
 stage=etree.Element('div',{'class':'hero-motion-stage','data-motion':'paused'})
 hero.addprevious(stage);stage.append(hero)
 stage.append(html.fragment_fromstring('''<svg class="hero-motion-overlay" viewBox="0 0 1280 853" aria-hidden="true" focusable="false">
 <defs><radialGradient id="hero-icon-light"><stop offset="0" stop-color="#77fff3" stop-opacity=".34"></stop><stop offset=".5" stop-color="#32e9e0" stop-opacity=".12"></stop><stop offset="1" stop-color="#32e9e0" stop-opacity="0"></stop></radialGradient></defs>
 <g fill="url(#hero-icon-light)" stroke="none"><ellipse class="hero-icon-glow hero-icon-phone" cx="268" cy="406" rx="48" ry="60"></ellipse><ellipse class="hero-icon-glow hero-icon-web" cx="710" cy="178" rx="64" ry="65"></ellipse><ellipse class="hero-icon-glow hero-icon-db" cx="974" cy="504" rx="59" ry="66"></ellipse></g>
 <g fill="none" stroke="#bafff8" stroke-width="3" stroke-linecap="round"><path class="hero-light-pulse hero-light-left" d="M454 459 L584 408 L584 385" pathLength="100"></path><path class="hero-light-pulse hero-light-right" d="M743 500 L828 536" pathLength="100"></path></g>
 </svg>'''))
 pause,resume=LABELS[lang]
 control=etree.SubElement(doc.xpath('//*[contains(concat(" ",normalize-space(@class)," ")," hero-copy ")]')[0],'button',{'class':'hero-motion-toggle','type':'button','hidden':'hidden','data-pause':pause,'data-resume':resume})
 control.text=pause
 head=doc.find('head')
 etree.SubElement(head,'link',rel='stylesheet',href='/hero-motion.css?v=1')
 etree.SubElement(head,'script',src='/hero-motion.js?v=1',defer='defer')
