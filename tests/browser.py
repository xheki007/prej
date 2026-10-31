from playwright.sync_api import sync_playwright
from pathlib import Path
import json,os,shutil
out=Path('../prej-seo-review');out.mkdir(exist_ok=True)
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path=os.environ.get('CHROMIUM_PATH') or shutil.which('chromium'),args=['--no-sandbox'])
 for size in [(1440,1000),(390,844),(320,700)]:
  page=browser.new_page(viewport={'width':size[0],'height':size[1]},reduced_motion='reduce')
  errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  for lang in ('sq','en','de','it'):
   page.goto(f'http://localhost:4174/{lang}/');page.wait_for_load_state('networkidle')
   assert page.locator('html').get_attribute('lang')==lang
   assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'),f'Overflow {size} {lang}'
   page.locator('header .language-picker summary').click();assert page.locator('header .language-options a').count()==4
   page.screenshot(path=str(out/f'{lang}-{size[0]}.png'))
   page.keyboard.press('Escape');assert page.locator('header .language-picker').get_attribute('open') is None
   if size[0]<860:
    page.locator('.menu-toggle').click();assert page.locator('.menu-toggle').get_attribute('aria-expanded')=='true'
    page.keyboard.press('Escape');assert page.locator('.menu-toggle').get_attribute('aria-expanded')=='false'
   page.locator('[data-filter="business"]').click();assert page.locator('.portfolio-card:visible').count()>0
   page.locator('[data-filter="all"]').click();assert page.locator('.portfolio-card:visible').count()==7
   page.locator('.project-details').first.locator('summary').click();assert page.locator('.project-details').first.get_attribute('open') is not None
   page.locator('[data-open-brief]').click();assert page.locator('dialog').is_visible()
   page.locator('[name=name]').fill('Test');page.locator('[name=email]').fill('test@example.com');page.locator('[name=message]').fill('A sample software project.')
   # Force clipboard fallback to verify usable manual-copy flow, without external sends.
   page.evaluate("Object.defineProperty(navigator,'clipboard',{value:{writeText:()=>Promise.reject(new Error('test denial'))},configurable:true})")
   page.locator('#copy-brief').click();assert page.locator('#manual-copy').is_visible();assert 'Test' in page.locator('#manual-brief').input_value()
   page.locator('.close-dialog').click();assert not page.locator('dialog').is_visible()
   page.locator('[data-open-brief]').click();page.keyboard.press('Escape');assert not page.locator('dialog').is_visible()
   assert not errors,errors
  page.goto('http://localhost:4174/?lang=sq#work');page.wait_for_url('**/sq/#work')
  page.goto('http://localhost:4174/de/?lang=it&utm_source=test#contact');page.wait_for_url('**/it/?utm_source=test#contact')
  page.close()
 # Fully visible and navigable without JavaScript.
 page=browser.new_page(java_script_enabled=False)
 for lang in ('sq','en','de','it'):
  page.goto(f'http://localhost:4174/{lang}/');assert page.locator('.portfolio-card:visible').count()==7
  page.locator('header .language-picker summary').click();page.locator('header a[hreflang=en]').click();assert page.url.endswith('/en/')
 browser.close()
print('PASS: 12 locale/viewport journeys, no JS errors or horizontal overflow; filters, cards, picker, modal, copy fallback, legacy URLs, no-JS.')
