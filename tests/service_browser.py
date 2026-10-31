"""Service journeys run on authorized GitHub CI, never submit an enquiry."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import os
ROOT=Path(__file__).resolve().parents[1]
LANGS=('sq','en','de','it')
SERVICES=('mobile-app-development','web-platform-development','api-integrations')
for lang in LANGS:
 for service in SERVICES:
  assert (ROOT/lang/'services'/service/'index.html').is_file(),f'Missing service page: {lang}/{service}'
out=ROOT/'qa-screenshots';out.mkdir(exist_ok=True)
base='http://localhost:4174'
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path=os.environ.get('CHROMIUM_PATH'),args=['--no-sandbox'])
 for width,height in [(1440,1000),(390,844),(320,700)]:
  page=browser.new_page(viewport={'width':width,'height':height},reduced_motion='reduce')
  errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  for lang in LANGS:
   for service in SERVICES:
    path=f'/{lang}/services/{service}/'
    response=page.goto(base+path);assert response.status==200,path
    page.wait_for_load_state('networkidle')
    assert page.locator('html').get_attribute('lang')==lang
    assert page.locator('h1').count()==1
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'),f'Overflow {path} {width}'
    assert page.locator('main').inner_text().strip(),path
    assert page.locator('a[href="/'+lang+'/#contact"]').count()>0
    # Shared chrome must remain keyboard-operable and announce current language.
    picker=page.locator('header .language-picker')
    picker.locator('summary').click();assert picker.locator('a[hreflang]').count()==4
    assert picker.locator('a[aria-current="page"]').get_attribute('hreflang')==lang
    page.keyboard.press('Escape');assert picker.get_attribute('open') is None
    if width<860:
     page.locator('.menu-toggle').click();assert page.locator('.menu-toggle').get_attribute('aria-expanded')=='true'
     page.keyboard.press('Escape');assert page.locator('.menu-toggle').get_attribute('aria-expanded')=='false'
    faq=page.locator('.service-faq details').first
    faq.locator('summary').click();assert faq.get_attribute('open') is not None
    faq.locator('summary').click();assert faq.get_attribute('open') is None
    page.evaluate('window.scrollTo(0,0)')
    page.screenshot(path=str(out/f'service-{service}-{lang}-{width}.png'),full_page=width==390)
    # Language switching must keep this service, not silently return to the home page.
    target='en' if lang!='en' else 'sq'
    picker.locator('summary').click();picker.locator(f'a[hreflang="{target}"]').click()
    assert page.url==base+f'/{target}/services/{service}/'
    page.go_back();assert page.url==base+path
    assert not errors,errors
  page.close()
 # Existing-home service discovery and contact handoff maintain locale.
 page=browser.new_page(reduced_motion='reduce')
 for lang in LANGS:
  page.goto(base+f'/{lang}/')
  for service in SERVICES:
   link=page.locator(f'a[href="/{lang}/services/{service}/"]').first
   assert link.count()==1
   link.click();assert page.url==base+f'/{lang}/services/{service}/'
   page.locator(f'a[href="/{lang}/#contact"]').first.click()
   assert page.url==base+f'/{lang}/#contact'
   page.locator('[data-open-brief]').click();assert page.locator('dialog').is_visible()
   page.locator('.close-dialog').click();assert not page.locator('dialog').is_visible()
 page.close()
 # Crawlable content and equivalent links cannot depend on JavaScript.
 page=browser.new_page(java_script_enabled=False)
 for lang in LANGS:
  for service in SERVICES:
   page.goto(base+f'/{lang}/services/{service}/')
   assert page.locator('h1').is_visible()
   page.locator('header .language-picker summary').click()
   page.locator('header a[hreflang="en"]').click()
   assert page.url==base+f'/en/services/{service}/'
 browser.close()
print('PASS: 36 service locale/viewport journeys, home discovery/contact handoff, equivalent-language navigation, no-JS, no JS errors/overflow.')
