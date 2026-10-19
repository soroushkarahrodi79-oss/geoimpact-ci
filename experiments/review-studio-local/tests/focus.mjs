/* V01 regression: actual Tab focus, not just the tour's highlighted target.
   --baseline runs the retained 32f3ab5 module in this browser context only. */
import { chromium } from 'playwright';
import assert from 'node:assert/strict';
import { readFile, readdir, mkdir, writeFile, mkdtemp, rm } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const root=fileURLToPath(new URL('../',import.meta.url)),web=path.join(root,'web');
const base=new URL(process.env.STUDIO_URL || 'http://127.0.0.1:8765');
assert(['127.0.0.1','localhost'].includes(base.hostname));
const baseline=process.argv.includes('--baseline'),reference='32f3ab50bb8a91d21118610bfc135b33e3fb2f3c';
const old=execFileSync('git',['show',`${reference}:experiments/review-studio-local/web/onboarding.js`],{cwd:root});
const local=path.join(root,'qa/local'),shots=path.join(root,'qa/screenshots/focus-v01');
await mkdir(local,{recursive:true});await mkdir(shots,{recursive:true});
const hash=bytes=>createHash('sha256').update(bytes).digest('hex');
async function inventory(dir=path.join(web,'data')) {
  const values={};
  for(const entry of await readdir(dir,{withFileTypes:true})) {
    const p=path.join(dir,entry.name);
    if(entry.isDirectory())Object.assign(values,await inventory(p));
    else values[path.relative(web,p).replaceAll('\\','/')]=hash(await readFile(p));
  }
  return values;
}
const before=await inventory(),records=[],external=[],errors=[],consoleErrors=[];
let nativeZoom=null;
const browser=await chromium.launch({headless:true,...(process.env.STUDIO_CHROMIUM_EXECUTABLE?{executablePath:process.env.STUDIO_CHROMIUM_EXECUTABLE}:{})});
const settle=page=>page.evaluate(()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve))));
async function state(page) {
  return page.evaluate(()=>{
    const n=document.activeElement,r=n.getBoundingClientRect(),panel=document.getElementById('guide-panel'),d=panel.getBoundingClientRect();
    const control=n.matches('button,input,select,a[href],summary,[tabindex]'),inside=panel.contains(n);
    const point=document.elementFromPoint(r.left+r.width/2,r.top+r.height/2);
    const covered=control&&!inside&&!panel.hidden&&r.left>=d.left&&r.right<=d.right&&r.top>=d.top&&r.bottom<=d.bottom&&Boolean(point?.closest('#guide-panel'));
    const offscreen=control&&(r.bottom<=0||r.top>=innerHeight||r.right<=0||r.left>=innerWidth);
    return {id:n.id||n.dataset.i18nAria||`${n.tagName}:${n.textContent.trim().slice(0,45)}`,control,inside,covered,offscreen,
      rect:{x:r.x,y:r.y,width:r.width,height:r.height},panel:{x:d.x,y:d.y,width:d.width,height:d.height}};
  });
}
async function visibleFocus(page) {
  await settle(page);const s=await state(page);
  if(!baseline){assert(!s.covered,`Focus covered: ${JSON.stringify(s)}`);assert(!s.offscreen,`Focus offscreen: ${JSON.stringify(s)}`);}
  return s;
}
async function start(page) {
  await page.locator('#help-button').click();await page.locator('[data-help-action=tour]').click();
  await page.locator('#guide-panel:not([hidden])[data-step="1"]').waitFor();
}
async function walk(page,stage,key,count,viewport) {
  const failures=[],visited=new Set();let outside=0;
  for(let i=1;i<=count;i++) {
    await page.keyboard.press(key);const s=await visibleFocus(page);visited.add(s.id);
    if(s.control&&!s.inside)outside++;
    if(s.covered||s.offscreen)failures.push({press:i,...s});
    if(stage==='historical-forward'&&((viewport.width===1440&&viewport.height===900&&i===12)||(viewport.width===834&&i===33)||(viewport.width===390&&i===9))) {
      assert.equal(await page.locator('#case').inputValue(),'synthetic-block');
      await page.screenshot({path:path.join(shots,`${baseline?'before':'after'}-${viewport.width}x${viewport.height}.png`)});
    }
  }
  records.push({viewport,stage,key,presses:count,controlsOutsideGuide:outside,visited:[...visited],failures});
  console.log(`${baseline?'BASELINE':'PASS'} ${viewport.width}x${viewport.height} ${stage}: ${failures.length} hidden/offscreen focus events`);
  return {visited,outside};
}
try {
  // Other UI files must remain the reference; no unrelated redesign in this test.
  for(const name of ['index.html','app.js','reader.js','style.css','onboarding-copy.js','onboarding.css']) {
    assert.equal(hash(await readFile(path.join(web,name))),hash(execFileSync('git',['show',`${reference}:experiments/review-studio-local/web/${name}`],{cwd:root})),name);
  }
  for(const [width,height] of [[1440,900],[1440,1000],[834,1112],[375,812],[390,844],[320,812]]) {
    const viewport={width,height},context=await browser.newContext({viewport,reducedMotion:'reduce'});
    await context.addInitScript(()=>localStorage.setItem('geoimpact:review-studio:onboarding:v1','{"status":"dismissed"}'));
    await context.route('**/*',async route=>{
      const u=new URL(route.request().url());
      if(u.origin!==base.origin){external.push(u.origin);await route.abort();return;}
      if(baseline&&u.pathname.endsWith('/onboarding.js')){await route.fulfill({status:200,body:old,contentType:'text/javascript'});return;}
      await route.continue();
    });
    const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));page.on('console',m=>{if(m.type()==='error')consoleErrors.push(m.text());});
    await page.goto(base.href);await page.locator('#completed:not([hidden]),#problem:not([hidden])').waitFor();
    assert(await page.locator('#completed').isVisible(),await page.locator('#problem').innerText());
    await start(page);const forward=await walk(page,'historical-forward','Tab',50,viewport);
    assert(forward.outside>0&&forward.visited.has('case')&&forward.visited.has('search'),'Tour trapped focus');
    await page.keyboard.press('Escape');assert.equal(await page.locator('#help-button').evaluate(n=>n===document.activeElement),true);
    await start(page);await walk(page,'historical-reverse','Shift+Tab',50,viewport);
    if(!baseline) {
      // Manual scrolling stays free; the next Tab/Shift+Tab reveals its new focus.
      await page.mouse.wheel(0,700);await walk(page,'after-manual-scroll','Tab',10,viewport);
      await page.keyboard.press('PageUp');await walk(page,'after-page-up','Shift+Tab',10,viewport);
      await page.keyboard.press('Escape');await start(page);
      for(let i=1;i<4;i++)await page.locator('[data-guide-action=next]').click();
      await walk(page,'map-step-forward','Tab',20,viewport);await walk(page,'map-step-reverse','Shift+Tab',20,viewport);
      await page.locator('#search').focus();await visibleFocus(page);
      await page.setViewportSize(width>700?{width:390,height:844}:{width:834,height:1112});await visibleFocus(page);
      await walk(page,'resized-forward','Tab',10,viewport);await walk(page,'resized-reverse','Shift+Tab',10,viewport);
      await page.setViewportSize(viewport);await page.keyboard.press('Escape');await start(page);
      await page.evaluate(()=>{document.documentElement.style.zoom='2';dispatchEvent(new Event('resize'));});await settle(page);
      await walk(page,'zoom-200-forward','Tab',30,viewport);await walk(page,'zoom-200-reverse','Shift+Tab',30,viewport);
      await page.evaluate(()=>{document.documentElement.style.zoom='1';dispatchEvent(new Event('resize'));});
      await page.keyboard.press('Escape');await page.locator('#language').selectOption('en');await start(page);
      await walk(page,'english-forward','Tab',15,viewport);await walk(page,'english-reverse','Shift+Tab',15,viewport);
      await page.keyboard.press('Escape');await page.locator('#language').selectOption('es');
      await page.locator('#help-button').click();await page.locator('[data-help-action=practice]').click();await page.locator('[data-onboarding-action=practice-start]').click();
      await walk(page,'practice-forward','Tab',15,viewport);await walk(page,'practice-reverse','Shift+Tab',15,viewport);
      await page.keyboard.press('Escape');await page.locator('#onboarding-dialog[open][data-page=practice-exit]').waitFor();await page.keyboard.press('Escape');
      assert.equal(await page.locator('#help-button').evaluate(n=>n===document.activeElement),true);
      assert.equal(await page.locator('dialog[open]').count(),0);assert.equal(await page.locator('[inert]').count(),0);
    }
    await context.close();
  }
  if(!baseline) {
    // Chromium's own page zoom, independent of the CSS-zoom checks above.
    // A disposable profile configures its default storage partition (key x).
    const profile=await mkdtemp(path.join(local,'focus-zoom-'));
    let context;
    try {
      await mkdir(path.join(profile,'Default'));
      await writeFile(path.join(profile,'Default','Preferences'),JSON.stringify({partition:{default_zoom_level:{x:Math.log(2)/Math.log(1.2)}}}));
      context=await chromium.launchPersistentContext(profile,{headless:true,viewport:{width:1440,height:1000},reducedMotion:'reduce',...(process.env.STUDIO_CHROMIUM_EXECUTABLE?{executablePath:process.env.STUDIO_CHROMIUM_EXECUTABLE}:{})});
      await context.addInitScript(()=>localStorage.setItem('geoimpact:review-studio:onboarding:v1','{"status":"dismissed"}'));
      await context.route('**/*',async route=>{if(new URL(route.request().url()).origin!==base.origin){external.push(route.request().url());await route.abort();}else await route.continue();});
      const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));page.on('console',m=>{if(m.type()==='error')consoleErrors.push(m.text());});
      await page.goto(base.href);await page.locator('#completed:not([hidden])').waitFor();
      nativeZoom=await page.evaluate(()=>({innerWidth,innerHeight,devicePixelRatio,cssZoom:getComputedStyle(document.documentElement).zoom}));
      assert.deepEqual(nativeZoom,{innerWidth:720,innerHeight:500,devicePixelRatio:2,cssZoom:'1'});
      await start(page);await walk(page,'native-zoom-200-forward','Tab',50,{width:1440,height:1000});
      await walk(page,'native-zoom-200-reverse','Shift+Tab',50,{width:1440,height:1000});
      await page.screenshot({path:path.join(shots,'after-native-zoom-200.png')});
    } finally {await context?.close();await rm(profile,{recursive:true,force:true});}
  }
  assert.deepEqual(await inventory(),before);assert.equal(external.length,0);assert.equal(errors.length,0);assert.equal(consoleErrors.length,0);
  if(baseline)assert(records.some(r=>r.failures.some(f=>f.covered)),'V01 did not reproduce');
} catch(error) {console.error(error);process.exitCode=1;}
finally {
  const result={baseline,reference_commit:reference,executed_at_utc:new Date().toISOString(),browser:browser.version(),node:process.version,physical_devices:false,screen_reader_tested:false,zoom:'200% CSS zoom at all six sizes; native Chromium 200% at 1440x1000',native_zoom:nativeZoom,module_sha256:hash(baseline?old:await readFile(path.join(web,'onboarding.js'))),records,external_requests:external,uncaught_errors:errors,console_errors:consoleErrors,scientific_bytes_unchanged:JSON.stringify(await inventory())===JSON.stringify(before),success:!process.exitCode};
  await writeFile(path.join(local,`focus-v01-${baseline?'before':'after'}.json`),JSON.stringify(result,null,2)+'\n');await browser.close();
}
