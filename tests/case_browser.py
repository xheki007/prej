"""Privacy-safe case-study regression; no interactions with the client system."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import os
ROOT=Path(__file__).resolve().parents[1]
LANGS=('sq','en','de','it')
SUFFIX='projects/home-of-dance/'
for lang in LANGS:assert (ROOT/lang/SUFFIX/'index.html').is_file(),f'Missing case study {lang}'
out=ROOT/'qa-screenshots';out.mkdir(exist_ok=True)
base='http://localhost:4174'
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path=os.environ.get('CHROMIUM_PATH'),args=['--no-sandbox'])
 for width,height in [(1440,1000),(390,844),(320,700)]:
  page=browser.new_page(viewport={'width':width,'height':height},reduced_motion='reduce')
  errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  for lang in LANGS:
   path=f'/{lang}/{SUFFIX}';response=page.goto(base+path);assert response.status==200
   page.wait_for_load_state('networkidle')
   assert page.locator('html').get_attribute('lang')==lang
   assert page.locator('h1').count()==1
   assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'),(lang,width)
   for img in page.locator('main img').all():
    img.scroll_into_view_if_needed();assert img.evaluate('(el) => el.decode().then(() => el.naturalWidth)')==1165
   page.locator('header .language-picker summary').click()
   assert page.locator('header .language-options a[hreflang]').count()==4
   assert page.locator('header .language-options a[aria-current=page]').get_attribute('hreflang')==lang
   page.keyboard.press('Escape');assert page.locator('header .language-picker').get_attribute('open') is None
   if width<860:
    page.locator('.menu-toggle').click();assert page.locator('.menu-toggle').get_attribute('aria-expanded')=='true'
    page.keyboard.press('Escape');assert page.locator('.menu-toggle').get_attribute('aria-expanded')=='false'
   page.locator('h1').scroll_into_view_if_needed()
   page.screenshot(path=str(out/f'case-home-dance-{lang}-{width}.png'),full_page=True)
   nextlang=LANGS[(LANGS.index(lang)+1)%4]
   page.locator('header .language-picker summary').click();page.locator(f'header .language-options a[hreflang="{nextlang}"]').click()
   page.wait_for_url('**/'+nextlang+'/'+SUFFIX);assert page.locator('html').get_attribute('lang')==nextlang
   page.go_back();page.wait_for_url('**'+path)
   page.locator(f'main a[href="/{lang}/services/web-platform-development/"]').click();page.wait_for_url('**/'+lang+'/services/web-platform-development/')
   page.locator(f'main a[href="/{lang}/{SUFFIX}"]').click();page.wait_for_url('**'+path)
   page.locator(f'main a[href="/{lang}/#contact"]').click();page.wait_for_url('**/'+lang+'/#contact')
   page.locator('[data-open-brief]').click();assert page.locator('dialog').is_visible();page.keyboard.press('Escape');assert not page.locator('dialog').is_visible()
   assert not errors,errors
  page.close()
 page=browser.new_page(java_script_enabled=False)
 for lang in LANGS:
  page.goto(base+f'/{lang}/{SUFFIX}');assert page.locator('main').is_visible()
  page.locator('header .language-picker summary').click();page.locator('header a[hreflang=en]').click();page.wait_for_url('**/en/'+SUFFIX)
 browser.close()
print('PASS: 12 case-study viewport/locale journeys, images, navigation, picker/menu, service/contact handoff, Back and no-JS; no client submissions.')
