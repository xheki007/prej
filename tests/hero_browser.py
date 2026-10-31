"""CI-only actual browser motion/accessibility checks; never launch locally."""
from pathlib import Path
import os
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
for lang in ('sq','en','de','it'):
 assert 'hero-motion-stage' in (ROOT/lang/'index.html').read_text()
out=ROOT/'qa-hero';out.mkdir(exist_ok=True)
base='http://localhost:4174'
def state(page, expected):
 page.wait_for_function("(s) => document.querySelector('.hero-motion-stage').dataset.motion === s",arg=expected)
def offset(page):
 return page.locator('.hero-light-left').evaluate('(e)=>getComputedStyle(e).strokeDashoffset')
def motion_diagnostic(page):
 return page.locator('.hero-light-left').evaluate('(e)=>({motion:e.closest(".hero-motion-stage").dataset.motion,css:getComputedStyle(e).animationPlayState,offset:getComputedStyle(e).strokeDashoffset,animations:e.getAnimations().map(a=>({state:a.playState,time:a.currentTime,pending:a.pending}))})')
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path=os.environ.get('CHROMIUM_PATH'),args=['--no-sandbox'])
 for width,height in [(1440,1000),(390,844),(320,700)]:
  context=browser.new_context(viewport={'width':width,'height':height},has_touch=width<500,is_mobile=width<500)
  page=context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  for lang in ('sq','en','de','it'):
   response=page.goto(base+'/'+lang+'/');assert response.status==200
   stage=page.locator('.hero-motion-stage');stage.scroll_into_view_if_needed();state(page,'running')
   image=stage.locator('img');image.evaluate('(e)=>e.decode()')
   a=image.bounding_box();b=stage.locator('svg').bounding_box()
   for key in ('x','y','width','height'):assert abs(a[key]-b[key])<.1,(lang,width,key,a,b)
   assert abs(a['width']/a['height']-1280/853)<.001
   assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
   # Animation timeline changes; test a known moving interval, not its intentional quiet interval.
   stage.locator('svg').evaluate('(e)=>e.getAnimations({subtree:true}).forEach(a=>{a.currentTime=500})')
   first=offset(page);page.wait_for_timeout(160);assert offset(page)!=first,(lang,width,first,motion_diagnostic(page))
   button=page.locator('.hero-motion-toggle');button.click();state(page,'paused')
   first=offset(page);page.wait_for_timeout(160);assert offset(page)==first,(lang,width,first,motion_diagnostic(page))
   assert button.inner_text()==button.get_attribute('data-resume')
   page.locator('footer').scroll_into_view_if_needed();state(page,'paused')
   stage.scroll_into_view_if_needed();state(page,'paused')
   assert page.locator('.hero-light-left').evaluate('(e)=>getComputedStyle(e).animationPlayState')=='paused'
   button.focus();page.keyboard.press('Enter');stage.scroll_into_view_if_needed();state(page,'running')
   # Native control owns playback. Seek only: WAAPI play()/pause() would override CSS.
   button.click();state(page,'paused')
   stage.locator('svg').evaluate('(e)=>e.getAnimations({subtree:true}).forEach(a=>{a.currentTime=1500})')
   page.locator('.hero').screenshot(path=str(out/f'hero-{lang}-{width}.png'))
   button.click();stage.scroll_into_view_if_needed();state(page,'running')
   page.locator('footer').scroll_into_view_if_needed();state(page,'paused')
   stage.scroll_into_view_if_needed();state(page,'running')
   # Exercise real visibilitychange handler without a production test hook.
   page.evaluate("Object.defineProperty(document,'hidden',{configurable:true,get:()=>true});document.dispatchEvent(new Event('visibilitychange'))")
   state(page,'paused')
   page.evaluate("delete document.hidden;document.dispatchEvent(new Event('visibilitychange'))")
   state(page,'running')
   if width==1440:
    box=page.locator('.hero').bounding_box()
    page.mouse.move(box['x']+box['width']*.9,max(1,box['y']+box['height']*.7));page.wait_for_timeout(400)
    values=stage.evaluate("(e)=>[parseFloat(e.style.getPropertyValue('--hero-x')),parseFloat(e.style.getPropertyValue('--hero-y'))]")
    assert all(abs(v)<=3 for v in values) and any(abs(v)>.1 for v in values),values
    page.mouse.move(0,height-1);page.wait_for_timeout(350)
    assert stage.evaluate("(e)=>parseFloat(e.style.getPropertyValue('--hero-x'))")==0
   else:
    assert stage.locator('svg').evaluate('(e)=>getComputedStyle(e).pointerEvents')=='none'
    assert stage.evaluate("(e)=>parseFloat(e.style.getPropertyValue('--hero-x')) || 0")==0
    page.locator('.hero a.button').tap();page.wait_for_url('**/#contact')
    page.locator('[data-open-brief]').tap();assert page.locator('dialog').is_visible();page.keyboard.press('Escape')
    stage.scroll_into_view_if_needed();state(page,'running')
   page.emulate_media(reduced_motion='reduce');state(page,'paused')
   assert not button.is_visible()
   assert stage.locator('svg').evaluate('(e)=>getComputedStyle(e).display')=='none'
   assert stage.evaluate('(e)=>getComputedStyle(e).transform')=='none'
   page.emulate_media(reduced_motion='no-preference');state(page,'running')
  assert not errors,errors
  context.close()
 # Unsupported observer: later lifecycle changes must not expose an inert control.
 context=browser.new_context()
 page=context.new_page();page.add_init_script('delete window.IntersectionObserver')
 page.goto(base+'/en/')
 page.evaluate("document.dispatchEvent(new Event('visibilitychange'))")
 page.emulate_media(reduced_motion='reduce');page.emulate_media(reduced_motion='no-preference')
 assert not page.locator('.hero-motion-toggle').is_visible()
 assert page.locator('.hero-motion-stage').get_attribute('data-enhanced') is None
 assert page.locator('.hero-motion-overlay').evaluate('(e)=>getComputedStyle(e).display')=='none'
 context.close()
 # No JS: static original photograph, no inert visible control.
 context=browser.new_context(java_script_enabled=False)
 page=context.new_page();page.goto(base+'/en/')
 assert not page.locator('.hero-motion-toggle').is_visible()
 assert page.locator('.hero-motion-overlay').evaluate('(e)=>getComputedStyle(e).display')=='none'
 assert page.locator('.hero-art img').is_visible();context.close()
 # Two brief actual-motion previews, isolated from full-suite screenshots.
 for width,height in [(1280,820),(390,844)]:
  context=browser.new_context(viewport={'width':width,'height':height},record_video_dir=str(out),record_video_size={'width':width,'height':height},has_touch=width<500,is_mobile=width<500)
  page=context.new_page();page.goto(base+'/sq/');page.locator('.hero-motion-stage').scroll_into_view_if_needed();state(page,'running')
  page.wait_for_timeout(7600)
  video=page.video;context.close();video.save_as(str(out/f'hero-motion-{width}.webm'));Path(video.path()).unlink()
 browser.close()
print('PASS 12 localized hero journeys, reduced motion, no-JS, visibility, pointer/touch; 12 PNG + 2 WebM previews')
