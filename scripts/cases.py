"""Build a factual, privacy-safe Home of Dance project case study in each locale."""
from copy import deepcopy
from lxml import html
import json
from background import add_background
from services import node
CASE_SUFFIX='projects/home-of-dance/'

def build_cases(root,langs):
 for lang in langs:
  copy=json.loads((root/f'i18n/case-home-of-dance-{lang}.json').read_text())
  doc=html.fromstring((root/lang/'services/web-platform-development/index.html').read_text())
  head=doc.find('head');body=doc.find('body');old=body.find('main');position=list(body).index(old);body.remove(old)
  for el in head.xpath('./script[@id="service-schema" or @id="service-breadcrumb-schema"]'):head.remove(el)
  main=html.Element('main',id='main',attrib={'class':'case-main'});body.insert(position,main)
  url=f'https://prej-tech.com/{lang}/{CASE_SUFFIX}'
  head.find('title').text=copy['title']
  for query,value in [('//meta[@name="description"]',copy['description']),('//meta[@property="og:title"]',copy['title']),('//meta[@property="og:description"]',copy['description']),('//meta[@property="og:url"]',url),('//meta[@property="og:image"]','https://prej-tech.com/assets/home-of-dance-booking.webp')]:doc.xpath(query)[0].set('content',value)
  doc.xpath('//link[@rel="canonical"]')[0].set('href',url)
  for link in doc.xpath('//link[@hreflang]'):
   code=link.get('hreflang');link.set('href',f'https://prej-tech.com/{"en" if code=="x-default" else code}/{CASE_SUFFIX}')
  for link in doc.xpath('//div[@class="language-options"]/a'):link.set('href',f'/{link.get("hreflang")}/{CASE_SUFFIX}')
  node(head,'link',rel='stylesheet',href='/case-study.css?v=1')
  hero=node(main,'section',class_='case-hero',id='top');wrap=node(hero,'div',class_='container')
  crumbs=node(wrap,'nav',class_='service-breadcrumbs',aria_label=copy['home']+' / '+copy['projects'])
  node(crumbs,'a',copy['home'],href=f'/{lang}/');node(crumbs,'span','/',aria_hidden='true');node(crumbs,'a',copy['projects'],href=f'/{lang}/#work');node(crumbs,'span','/',aria_hidden='true');node(crumbs,'span',copy['name'],aria_current='page')
  node(wrap,'p',copy['eyebrow'],class_='eyebrow');node(wrap,'h1',copy['h1']);node(wrap,'p',copy['intro'],class_='case-intro')
  scope=node(wrap,'div',class_='case-scope');node(scope,'h2',copy['scopeTitle']);ul=node(scope,'ul')
  for item in copy['scope']:node(ul,'li',item)
  content=node(main,'div',class_='container case-content')
  workflow=node(content,'section',class_='case-section',id='public-workflow');node(workflow,'h2',copy['workflowTitle']);node(workflow,'p',copy['workflowIntro'])
  figure=node(workflow,'figure',class_='case-screenshot');node(figure,'img',src='/assets/home-of-dance-booking.webp',alt=copy['bookingAlt'],width='1165',height='747',loading='lazy',decoding='async');node(figure,'figcaption',copy['bookingCaption'])
  node(workflow,'a',copy['publicLink']+' ↗',class_='text-link',href='https://backoffice.homeofdance.de/buchen')
  request=node(content,'section',class_='case-section',id='registration-review');node(request,'h2',copy['requestTitle']);node(request,'p',copy['requestText'])
  boundary=node(request,'aside',class_='case-boundary');node(boundary,'h3',copy['boundaryTitle']);node(boundary,'p',copy['boundaryText'])
  figure=node(request,'figure',class_='case-screenshot');node(figure,'img',src='/assets/home-of-dance-request.webp',alt=copy['requestAlt'],width='1165',height='747',loading='lazy',decoding='async');node(figure,'figcaption',copy['requestCaption'])
  admin=node(content,'section',class_='case-section',id='backoffice');node(admin,'h2',copy['backofficeTitle']);node(admin,'p',copy['backofficeIntro']);grid=node(admin,'div',class_='case-module-grid')
  for i,module in enumerate(copy['modules'],1):
   article=node(grid,'article');node(article,'span',f'0{i}',class_='case-module-index',aria_hidden='true');node(article,'h3',module['title']);node(article,'p',module['text'])
  design=node(content,'section',class_='case-section case-design');node(design,'h2',copy['designTitle']);node(design,'p',copy['designText'])
  evidence=node(content,'section',class_='case-section case-evidence');node(evidence,'h2',copy['evidenceTitle']);node(evidence,'p',copy['evidenceText']);links=node(evidence,'div',class_='case-links');node(links,'a',copy['serviceLink']+' →',class_='text-link',href=f'/{lang}/services/web-platform-development/');node(links,'a',copy['portfolioLink']+' →',class_='text-link',href=f'/{lang}/#project-dance')
  cta=node(main,'section',class_='service-cta');wrap=node(cta,'div',class_='container');node(wrap,'h2',copy['relatedTitle']);node(wrap,'p',copy['relatedText']);node(wrap,'a',copy['cta']+' ↗',class_='button primary',href=f'/{lang}/#contact')
  add_background(doc)
  path=root/lang/CASE_SUFFIX;path.mkdir(parents=True,exist_ok=True);(path/'index.html').write_text('<!doctype html>\n'+html.tostring(doc,encoding='unicode',method='html')+'\n')
