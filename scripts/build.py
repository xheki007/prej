"""Build committed, crawlable locale pages: python scripts/build.py (requires lxml)."""
from pathlib import Path
import json
from lxml import html,etree
ROOT=Path(__file__).resolve().parents[1]
LANGS={'sq':('Shqip','🇦🇱'),'en':('English','🇬🇧'),'de':('Deutsch','🇩🇪'),'it':('Italiano','🇮🇹')}
META={
'en':('PREJ — Software development in Kosovo','PREJ builds mobile apps, business platforms, AI-assisted systems and interactive 3D products. Software engineering from Mitrovica, Kosovo.'),
'sq':('PREJ — Zhvillim softuerik në Kosovë','PREJ ndërton aplikacione mobile, platforma biznesi, sisteme të asistuara nga AI dhe produkte interaktive 3D. Inxhinieri softuerike nga Mitrovica, Kosovë.'),
'de':('PREJ — Softwareentwicklung aus Kosovo','PREJ entwickelt mobile Apps, Business-Plattformen, KI-gestützte Systeme und interaktive 3D-Produkte. Softwareentwicklung aus Mitrovica, Kosovo.'),
'it':('PREJ — Sviluppo software dal Kosovo','PREJ sviluppa app mobili, piattaforme aziendali, sistemi assistiti dall’IA e prodotti interattivi 3D. Ingegneria software da Mitrovica, Kosovo.')}

def build(lang):
 doc=html.fromstring((ROOT/'i18n/template.html').read_text())
 translations=json.loads((ROOT/f'i18n/{lang}.json').read_text())
 for el in doc.iter():
  for source,target in [('data-sq',None),('data-sq-aria','aria-label'),('data-sq-alt','alt')]:
   if source not in el.attrib:continue
   original=el.text_content() if target is None else el.get(target)
   translated=translations[original]
   if target:el.set(target,translated)
   else:
    for child in list(el):el.remove(child)
    el.text=translated
   del el.attrib[source]
 # Translate remaining leaf labels (technical/product names remain unchanged).
 for el in doc.iter():
  if len(el)==0 and el.text and el.text.strip() in translations:
   el.text=translations[el.text.strip()]
 doc.set('lang',lang)
 title,description=META[lang];url=f'https://prej-tech.com/{lang}/'
 doc.find('head/title').text=title
 for query,value in [('//meta[@name="description"]',description),('//meta[@property="og:title"]',title),('//meta[@property="og:description"]',description),('//meta[@property="og:url"]',url),('//meta[@property="og:image"]','https://prej-tech.com/assets/connected-systems.png')]:doc.xpath(query)[0].set('content',value)
 doc.xpath('//link[@rel="canonical"]')[0].set('href',url)
 head=doc.find('head')
 for code in [*LANGS,'x-default']:
  etree.SubElement(head,'link',rel='alternate',hreflang=code,href=f'https://prej-tech.com/{code if code!="x-default" else "en"}/')
 etree.SubElement(head,'meta',property='og:locale',content={'en':'en_GB','sq':'sq_AL','de':'de_DE','it':'it_IT'}[lang])
 structured={'@context':'https://schema.org','@type':'Organization','name':'PREJ','legalName':'PREJ SH.P.K.','url':'https://prej-tech.com/','logo':'https://prej-tech.com/assets/prej-logo-dark.webp','email':'ferizixhevdet@gmail.com','telephone':'+38349475027','address':{'@type':'PostalAddress','addressLocality':'Mitrovica','addressCountry':'XK'}}
 etree.SubElement(head,'script',type='application/ld+json').text=json.dumps(structured,ensure_ascii=False)
 etree.SubElement(head,'link',rel='stylesheet',href='/language.css?v=1')
 runtime=json.loads((ROOT/f'i18n/runtime-{lang}.json').read_text())
 etree.SubElement(head,'script',id='locale-messages',type='application/json').text=json.dumps(runtime,ensure_ascii=False)
 for el in doc.xpath('//div[contains(@class,"language-switch")]'):
  el.clear();el.set('class','language-switch')
  picker=etree.SubElement(el,'details',{'class':'language-picker'})
  summary=etree.SubElement(picker,'summary',{'aria-label':translations['Language']+': '+LANGS[lang][0]})
  flag=etree.SubElement(summary,'span',{'aria-hidden':'true'});flag.text=LANGS[lang][1];flag.tail=' '+LANGS[lang][0]
  links=etree.SubElement(picker,'div',{'class':'language-options'})
  for code,(name,flag) in LANGS.items():
   a=etree.SubElement(links,'a',href=f'/{code}/',lang=code,hreflang=code)
   if code==lang:a.set('aria-current','page')
   etree.SubElement(a,'span',{'aria-hidden':'true'}).text=flag
   a[-1].tail=' '+name
 for el in doc.iter():
  for attr in ['href','src','poster','data-src']:
   v=el.get(attr)
   if v and (v.startswith('assets/') or v.split('?')[0] in ['style.css','portfolio.css','workflow-video.css','app.js']):el.set(attr,'/'+v)
 for el in doc.xpath('//img[contains(@src,"prej-logo-dark.png")]'):el.set('src','/assets/prej-logo-dark.webp');el.set('width','624');el.set('height','208')
 doc.xpath('//link[@rel="icon"]')[0].set('href','/assets/favicon.png')
 hero=doc.xpath('//img[contains(@src,"connected-systems.png")]')[0]
 hero.set('src','/assets/connected-systems-1280.webp');hero.set('srcset','/assets/connected-systems-640.webp 640w, /assets/connected-systems-1280.webp 1280w');hero.set('sizes','(max-width: 580px) 100vw, 65vw');hero.set('fetchpriority','high')
 doc.xpath('//noscript/a')[0].text='▶ '+translations['Watch the film']+' · 60s'
 result='<!doctype html>\n'+html.tostring(doc,encoding='unicode',method='html')+'\n'
 (ROOT/lang).mkdir(exist_ok=True);(ROOT/lang/'index.html').write_text(result)
 return result
for lang in LANGS:
 result=build(lang)
 if lang=='en':(ROOT/'index.html').write_text(result)
(ROOT/'robots.txt').write_text('User-agent: *\nAllow: /\nDisallow: /i18n/\nDisallow: /scripts/\nDisallow: /tests/\nDisallow: /docs/\n\nSitemap: https://prej-tech.com/sitemap.xml\n')
ns='http://www.sitemaps.org/schemas/sitemap/0.9';xh='http://www.w3.org/1999/xhtml'
root=etree.Element('{'+ns+'}urlset',nsmap={None:ns,'xhtml':xh})
for lang in LANGS:
 node=etree.SubElement(root,'{'+ns+'}url');etree.SubElement(node,'{'+ns+'}loc').text=f'https://prej-tech.com/{lang}/'
 for alt in [*LANGS,'x-default']:etree.SubElement(node,'{'+xh+'}link',rel='alternate',hreflang=alt,href=f'https://prej-tech.com/{alt if alt!="x-default" else "en"}/')
(ROOT/'sitemap.xml').write_bytes(etree.tostring(root,xml_declaration=True,encoding='UTF-8',pretty_print=True))
