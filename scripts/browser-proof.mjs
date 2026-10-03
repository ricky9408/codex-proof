import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
import {pathToFileURL} from 'node:url';
if(!process.env.PLAYWRIGHT_MODULE)throw new Error('Set PLAYWRIGHT_MODULE to an existing Playwright index.mjs');
const {chromium}=await import(pathToFileURL(process.env.PLAYWRIGHT_MODULE));
const browser=await chromium.launch({channel:'chrome',headless:true,args:['--no-proxy-server']});
const results={browser:'Installed Google Chrome with Playwright; isolated temporary profile',version:browser.version(),fallbackReason:'Browser plugin/skill unavailable; user authorized local Chrome',viewport:{width:1280,height:800},flows:[]};
await fs.mkdir('evidence/browser-video',{recursive:true});
try{
 for(const phase of ['before','after']){
  const context=await browser.newContext({viewport:results.viewport,recordVideo:{dir:'evidence/browser-video',size:results.viewport}});
  const page=await context.newPage();const errors=[];page.on('pageerror',e=>errors.push(String(e)));page.on('console',m=>{if(m.type()==='error')errors.push(m.text());});
  const url=`http://127.0.0.1:4173/sample/?variant=${phase}`;await page.goto(url);assert.equal(await page.title(),'Codex Proof · Cart regression');await page.getByRole('heading',{name:'Your cart',exact:true}).waitFor();
  await page.waitForTimeout(900);await page.locator('#add-notebook').click();await page.waitForTimeout(550);await page.locator('#add-mug').click();assert.equal(await page.locator('#total').textContent(),'$30.00');await page.waitForTimeout(700);await page.getByRole('button',{name:'Remove Notebook',exact:true}).click();
  const observed=await page.locator('#total').textContent();assert.equal(observed,phase==='before'?'$0.00':'$18.00');assert.equal(await page.locator('.item').count(),1);assert.match(await page.locator('#items').textContent(),/Ceramic mug/);await page.screenshot({path:`evidence/${phase}.png`});await page.waitForTimeout(2400);assert.deepEqual(errors,[]);
  results.flows.push({phase,url,actions:['Add Notebook','Add Ceramic mug','Remove Notebook'],expected:'$18.00',observed,itemCount:1,consoleErrors:errors});const video=page.video();await context.close();await video.saveAs(`evidence/${phase}.webm`);
 }
 const context=await browser.newContext({viewport:{width:390,height:844}});const page=await context.newPage();await page.goto('http://127.0.0.1:4173/sample/?variant=after');await page.locator('#add-notebook').click();await page.locator('#add-mug').click();await page.getByRole('button',{name:'Remove Notebook',exact:true}).click();assert.equal(await page.locator('#total').textContent(),'$18.00');assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);await page.screenshot({path:'evidence/mobile-after.png',fullPage:true});results.mobile={viewport:{width:390,height:844},observed:'$18.00',horizontalOverflow:false};await context.close();await fs.writeFile('evidence/browser.json',JSON.stringify(results,null,2)+'\n');console.log(JSON.stringify(results,null,2));
}finally{await browser.close();}
