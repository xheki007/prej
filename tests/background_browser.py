"""CI browser checks for real section-local background behavior, never send forms."""
from pathlib import Path
import os
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'qa-screenshots';OUT.mkdir(exist_ok=True)
BASE='http://localhost:4174'
def motion(page,host,wanted):
 page.wait_for_function('(args)=>document.querySelector(args[0]).dataset.ambientMotion===args[1]',arg=[host,wanted])
def sample(page,selector):return page.locator(selector).evaluate('(e)=>getComputedStyle(e).strokeDashoffset')
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path=os.environ.get('CHROMIUM_PATH'),args=['--no-sandbox'])
 for width,height in [(1440,1000),(390,844),(320,700)]:
  context=browser.new_context(viewport={'width':width,'height':height},is_mobile=width<500,has_touch=width<500)
  page=context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  for lang in ('sq','en','de','it'):
   for suffix,label in [('', 'home'),('services/web-platform-development/','service'),('projects/home-of-dance/','case')]:
    assert page.goto(f'{BASE}/{lang}/{suffix}').status==200
    host='main>.ambient-host:first-child';pulse=host+' .ambient-route-3 .ambient-pulse'
    motion(page,host,'running')
    assert page.locator(host+' > .ambient-layer').count()==1
    assert page.locator(host+' > .ambient-layer').evaluate('(e)=>getComputedStyle(e).pointerEvents')=='none'
    assert page.locator(host+' > .ambient-layer').evaluate('(e)=>getComputedStyle(e).zIndex')=='-1'
    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
    first=sample(page,pulse);page.wait_for_timeout(130);assert sample(page,pulse)!=first
    if width<500:assert page.locator(host+' .ambient-route-1').evaluate('(e)=>getComputedStyle(e).display')=='none'
    # Decoration is not the hit-test target over real text/controls.
    assert page.locator('h1').evaluate('(e)=>{const r=e.getBoundingClientRect();return !document.elementFromPoint(r.x+5,r.y+5).closest(".ambient-layer")}')
    # Reduced motion flips live and hides pulses, leaving a static light grid.
    page.emulate_media(reduced_motion='reduce');motion(page,host,'paused')
    assert page.locator(pulse).evaluate('(e)=>getComputedStyle(e).display')=='none'
    page.emulate_media(reduced_motion='no-preference');motion(page,host,'running')
    # Exercise actual visibility handler without a production test API.
    page.evaluate("Object.defineProperty(document,'hidden',{configurable:true,get:()=>true});document.dispatchEvent(new Event('visibilitychange'))")
    motion(page,host,'paused')
    page.evaluate("delete document.hidden;document.dispatchEvent(new Event('visibilitychange'))")
    motion(page,host,'running')
    page.evaluate("window.dispatchEvent(new PageTransitionEvent('pagehide',{persisted:true}))");motion(page,host,'paused')
    page.evaluate("window.dispatchEvent(new PageTransitionEvent('pageshow',{persisted:true}))");motion(page,host,'running')
    page.screenshot(path=str(OUT/f'background-{label}-{lang}-{width}.png'))
    # All lower sections remain decorated; only visible sections animate.
    page.locator('footer').scroll_into_view_if_needed();motion(page,host,'paused');motion(page,'footer','running')
    if lang=='sq':page.screenshot(path=str(OUT/f'background-footer-{label}-{width}.png'))
    if label=='home':
     page.locator('#capabilities').scroll_into_view_if_needed();motion(page,'#capabilities','running')
     if lang=='sq':page.screenshot(path=str(OUT/f'background-capabilities-{width}.png'))
    elif label=='service':
     page.locator('.service-faq').scroll_into_view_if_needed();motion(page,'.service-content','running')
     page.locator('.service-faq summary').first.click();assert page.locator('.service-faq details').first.get_attribute('open') is not None
     if lang=='sq':page.screenshot(path=str(OUT/f'background-faq-{width}.png'))
    else:
     page.locator('#public-workflow').scroll_into_view_if_needed();motion(page,'.case-content','running')
     if lang=='sq':page.screenshot(path=str(OUT/f'background-case-content-{width}.png'))
    assert not errors,errors
  context.close()
 # Static no-JS layout has decoration but no moving CSS; no content removed.
 context=browser.new_context(java_script_enabled=False,viewport={'width':390,'height':844});page=context.new_page()
 for suffix in ('','services/web-platform-development/','projects/home-of-dance/'):
  page.goto(BASE+'/en/'+suffix)
  assert page.locator('h1').is_visible()
  assert page.locator('.ambient-pulse').first.evaluate('(e)=>getComputedStyle(e).animationPlayState')=='paused'
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
 context.close();browser.close()
print('Background: 36 locale/viewport/page journeys and three no-JS routes passed')
