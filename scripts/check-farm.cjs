const {chromium}=require('/Users/den/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs=require('node:fs');const assert=require('node:assert/strict');
const base='/Users/den/Documents/ChatGPT/Garliboost/output/review-2026-09-15';
(async()=>{
const browser=await chromium.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
const page=await browser.newPage({viewport:{width:1440,height:1000}});const errors=[];const requests=[];
page.on('pageerror',e=>errors.push(e.message));page.on('console',m=>{if(m.type()==='error')errors.push(m.text())});page.on('request',r=>requests.push({method:r.method(),url:r.url()}));
await page.goto('http://127.0.0.1:8765/concept-03.html?review=20260915',{waitUntil:'networkidle'});
await page.addStyleTag({content:'html{scroll-behavior:auto!important}'});
assert.equal(await page.locator('h1').count(),1);
const badAnchors=await page.evaluate(()=>[...document.querySelectorAll('a[href^="#"]')].filter(a=>a.hash&&!document.getElementById(a.hash.slice(1))).map(a=>a.hash));assert.deepEqual(badAnchors,[]);
const report={viewports:[],calculator:[],tabs:'',form:'',videos:[],consoleErrors:errors};
for(const width of [1440,1280,768,390]){
 await page.setViewportSize({width,height:1000});await page.evaluate(()=>scrollTo(0,0));
 assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false,`overflow ${width}`);
 await page.screenshot({path:`${base}/full-${width}.png`,fullPage:true});
 // Tiled captures for reviewing every section at readable size.
 const height=await page.evaluate(()=>document.documentElement.scrollHeight);
 if(width===1440||width===390){for(let y=0,index=0;y<height;y+=950,index++){await page.evaluate(y=>scrollTo(0,y),y);await page.screenshot({path:`${base}/tile-${width}-${index}.png`});}}
 report.viewports.push({width,height,overflow:false});
}
await page.setViewportSize({width:1440,height:1000});
for(const [input,expected] of [['500',['500','≈71,4','≈35,7']],['70',['70','10','5']],['0,1',['0,1','<0,1','<0,1']],['123.4',['123,4','≈17,6','≈8,8']],['2000',['2 000','≈285,7','≈142,9']]]){
 await page.locator('#weight').fill(input);const vals=await page.locator('.dose-results output').allTextContents();assert.deepEqual(vals,expected);report.calculator.push({input,values:vals});
}
for(const input of ['','-1','0','2000.1','abc','1.25','1e3']){await page.locator('#weight').fill(input);assert.equal(await page.locator('#weight').getAttribute('aria-invalid'),'true');assert.deepEqual(await page.locator('.dose-results output').allTextContents(),['—','—','—']);}
await page.locator('#weight').fill('500');
await page.locator('#tab-cows').focus();await page.keyboard.press('ArrowRight');assert.equal(await page.locator('#tab-calves').getAttribute('aria-selected'),'true');assert.equal(await page.locator('#panel-calves').isVisible(),true);await page.keyboard.press('End');assert.equal(await page.locator('#tab-sheep').getAttribute('aria-selected'),'true');await page.keyboard.press('Home');assert.equal(await page.locator('#tab-cows').getAttribute('aria-selected'),'true');
for(const key of ['calves','pigs','goats','sheep','cows']){await page.locator('#tab-'+key).click();assert.equal(await page.locator('#panel-'+key).isVisible(),true);assert.equal(await page.locator('[role=tabpanel]:visible').count(),1);}
report.tabs='All 5 tabs, ArrowRight, Home, End and visible panel passed';
await page.locator('#materials-link').click();assert.equal(await page.locator('#materials').getAttribute('open'),'');
for(const a of await page.locator('#materials a[href$=".pdf"]').all()){const href=await a.getAttribute('href');const response=await page.request.get('http://127.0.0.1:8765/'+href);assert.equal(response.status(),200);}
await page.evaluate(()=>document.getElementById('materials').open=false);
const form=page.locator('#farm-form');assert.equal(await form.evaluate(f=>f.checkValidity()),false);
for(const [name,val] of Object.entries({name:'Проверка макета',company:'Тестовая форма',phone:'+421900000000',email:'invalid',headcount:'10',task:'Проверка без отправки'}))await form.locator(`[name=${name}]`).fill(val);
await form.locator('[name=animals]').selectOption({label:'Коровы'});assert.equal(await form.evaluate(f=>f.checkValidity()),false);
await form.locator('[name=email]').fill('test@example.com');await form.locator('[name=headcount]').fill('-1');assert.equal(await form.evaluate(f=>f.checkValidity()),false);await form.locator('[name=headcount]').fill('10');assert.equal(await form.evaluate(f=>f.checkValidity()),true);await form.locator('button').click();assert.match(await page.locator('#form-status').innerText(),/данные не отправлены/);assert.equal(requests.filter(r=>r.method==='POST').length,0);report.form='Required fields, email, negative headcount, valid submit and explicit demo status passed; no POST';
await form.evaluate(f=>f.reset());await page.evaluate(()=>document.getElementById('form-status').textContent='');
const videos=page.locator('video');assert.equal(await videos.count(),2);
for(let i=0;i<2;i++){const v=videos.nth(i);await v.scrollIntoViewIfNeeded();await v.evaluate(async v=>{v.muted=true;await v.play()});await page.waitForTimeout(300);assert.equal(await v.evaluate(v=>v.currentTime>0),true);await v.evaluate(v=>{v.pause();v.currentTime=10});await page.waitForTimeout(300);report.videos.push(await v.evaluate(v=>({src:v.getAttribute('src'),width:v.videoWidth,height:v.videoHeight,fit:getComputedStyle(v).objectFit})));await page.screenshot({path:`${base}/video-${i+1}.png`});}
await videos.nth(0).evaluate(async v=>{await v.play()});await videos.nth(1).evaluate(async v=>{await v.play()});assert.equal(await videos.nth(0).evaluate(v=>v.paused),true);await videos.nth(1).evaluate(v=>v.pause());
assert.deepEqual(errors,[]);fs.writeFileSync(`${base}/checks.json`,JSON.stringify(report,null,2));console.log(JSON.stringify(report,null,2));await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
