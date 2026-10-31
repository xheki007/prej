"""Render substantial service pages using the localized site's existing chrome."""
from copy import deepcopy
from lxml import html,etree
import json
SLUGS=('mobile-app-development','web-platform-development','api-integrations')

def node(parent,tag,text=None,**attrs):
 el=etree.SubElement(parent,tag,{k.rstrip('_').replace('_','-'):v for k,v in attrs.items()})
 el.text=text
 return el

def build_services(root,langs):
 for lang in langs:
  content=json.loads((root/f'i18n/services-{lang}.json').read_text());ui=content['ui']
  home=html.fromstring((root/lang/'index.html').read_text())
  for index,slug in enumerate(SLUGS,1):
   service=content['services'][slug];doc=deepcopy(home);head=doc.find('head');body=doc.find('body')
   url=f'https://prej-tech.com/{lang}/services/{slug}/'
   doc.find('head/title').text=service['title']
   for query,value in [('//meta[@name="description"]',service['description']),('//meta[@property="og:title"]',service['title']),('//meta[@property="og:description"]',service['description']),('//meta[@property="og:url"]',url)]:doc.xpath(query)[0].set('content',value)
   doc.xpath('//link[@rel="canonical"]')[0].set('href',url)
   for el in doc.xpath('//link[@hreflang]'):
    code=el.get('hreflang');el.set('href',f'https://prej-tech.com/{"en" if code=="x-default" else code}/services/{slug}/')
   for el in head.xpath('./script[@src or @id="locale-messages"]'):head.remove(el)
   for el in head.xpath('./link[contains(@href,"hero-motion.css")]'):head.remove(el)
   node(head,'link',rel='stylesheet',href='/service.css?v=2')
   node(head,'script',src='/service.js?v=1',defer='defer')
   node(head,'script',json.dumps({'openMenu':ui['openMenu'],'closeMenu':ui['closeMenu']},ensure_ascii=False),id='service-messages',type='application/json')
   for el in list(body):
    if el.tag=='main' or el.tag=='dialog':body.remove(el)
   for el in body.xpath('.//a[starts-with(@href,"#")]'):
    if el.get('href')=='#top' and 'text-link' in el.get('class',''):continue
    if 'skip-link' not in el.get('class',''):el.set('href',f'/{lang}/'+el.get('href'))
   for el in body.xpath('.//div[@class="language-options"]/a'):
    el.set('href',f'/{el.get("hreflang")}/services/{slug}/')
   main=etree.Element('main',id='main',attrib={'class':'service-main'})
   body.insert(list(body).index(body.find('footer')),main)
   hero=node(main,'section',class_='service-hero',id='top')
   wrap=node(hero,'div',class_='container')
   breadcrumbs=node(wrap,'nav',class_='service-breadcrumbs',aria_label=ui['home']+' / '+ui['services'])
   node(breadcrumbs,'a',ui['home'],href=f'/{lang}/');node(breadcrumbs,'span','/',aria_hidden='true');node(breadcrumbs,'a',ui['services'],href=f'/{lang}/#capabilities');node(breadcrumbs,'span','/',aria_hidden='true');node(breadcrumbs,'span',service['name'],aria_current='page')
   grid=node(wrap,'div',class_='service-hero-grid')
   copy=node(grid,'div');node(copy,'p',ui['eyebrow'],class_='eyebrow');node(copy,'h1',service['name']);node(copy,'p',service['intro'],class_='service-lead')
   node(copy,'a',ui['cta']+' ↗',class_='button primary',href=f'/{lang}/#contact')
   art=node(grid,'div',class_='service-diagram service-diagram-'+str(index),aria_hidden='true')
   node(art,'span',f'0{index}',class_='service-diagram-number')
   for glyph in ['◇','↔','▦']:node(art,'span',glyph,class_='service-diagram-node')
   node(art,'span','PREJ / 0'+str(index),class_='service-diagram-caption')
   contentWrap=node(main,'div',class_='container service-content')
   overview=node(contentWrap,'section',class_='service-overview',aria_label=ui['overview'])
   node(overview,'p',ui['overview'],class_='eyebrow')
   for i,section in enumerate(service['sections'],1):
    article=node(overview,'article',class_='service-feature');node(article,'span',f'0{i}',class_='service-index',aria_hidden='true');box=node(article,'div');node(box,'h2',section['title']);node(box,'p',section['text'])
   delivery=node(contentWrap,'section',class_='service-delivery');node(delivery,'h2',ui['deliverables']);ul=node(delivery,'ul')
   for text in service['deliverables']:node(ul,'li',text)
   node(delivery,'h3',ui['process']);node(delivery,'p',service['processText'])
   proof=node(contentWrap,'section',class_='service-proof');node(proof,'p',ui['evidence'],class_='eyebrow');node(proof,'h2',service['projectName']);node(proof,'p',service['projectText']);node(proof,'a',ui['projectLink']+' ↗',class_='text-link',href=f'/{lang}/#{service["projectId"]}')
   if slug=='web-platform-development':
    case=json.loads((root/f'i18n/case-home-of-dance-{lang}.json').read_text())
    node(proof,'a',case['readCase']+' →',class_='text-link case-proof-link',href=f'/{lang}/projects/home-of-dance/')
   faq=node(contentWrap,'section',class_='service-faq');node(faq,'h2',ui['questions'])
   for item in service['faq']:
    details=node(faq,'details');node(details,'summary',item['q']);node(details,'p',item['a'])
   related=node(contentWrap,'section',class_='service-related');node(related,'h2',ui['related']);links=node(related,'div',class_='service-related-grid')
   for other in SLUGS:
    if other!=slug:
     a=node(links,'a',class_='service-related-card',href=f'/{lang}/services/{other}/');node(a,'h3',content['services'][other]['name']);node(a,'span',ui['readService']+' →')
   cta=node(main,'section',class_='service-cta');w=node(cta,'div',class_='container');node(w,'h2',ui['ctaTitle']);node(w,'p',ui['ctaText']);node(w,'a',ui['cta']+' ↗',class_='button primary',href=f'/{lang}/#contact')
   path=root/lang/'services'/slug;path.mkdir(parents=True,exist_ok=True);(path/'index.html').write_text('<!doctype html>\n'+html.tostring(doc,encoding='unicode',method='html')+'\n')
