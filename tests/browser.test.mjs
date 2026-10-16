import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
const {chromium}=await import(process.env.PLAYWRIGHT_MODULE||'playwright');
const browser=await chromium.launch({headless:true,...(process.env.CHROME_PATH?{executablePath:process.env.CHROME_PATH}:{})});
const page=await browser.newPage({viewport:{width:1280,height:1000}});
const errors=[];page.on('pageerror',e=>errors.push(e.message));
await page.goto(process.env.SIMULATOR_URL||'http://127.0.0.1:8765/');
const complete=()=>page.waitForFunction(()=>document.getElementById('status').textContent.includes('模擬完成'),{},{timeout:60000});
await complete();assert.equal(await page.locator('.plot svg').count(),4);
assert.equal(await page.locator('#N').inputValue(),'1000');assert.equal(await page.locator('#fixed').isChecked(),false);
await page.check('#fixed');await complete();const initial=await page.locator('#stats').innerText();await page.uncheck('#fixed');await complete();await page.check('#fixed');await complete();assert.equal(await page.locator('#stats').innerText(),initial);
for(const key of ['uniform','t','beta','normal','poisson','cauchy','chi']){await page.selectOption('#dist',key);await complete();assert.ok(!/NaN|undefined/.test(await page.locator('#stats').innerText()));assert.equal(await page.locator('#stats tr').count(),3);}
await page.selectOption('#preset','1000');await complete();assert.match(await page.locator('#result-title').innerText(),/n=1000/);
await page.click('#play');await page.waitForFunction(()=>document.getElementById('result-title').textContent.includes('n=1,'));await page.click('#play');assert.match(await page.locator('#play').innerText(),/自動播放/);
await page.selectOption('#preset','30');await complete();
await page.click('#save');const svgPromise=page.waitForEvent('download');await page.click('#save-svg');const svg=await svgPromise;assert.match(svg.suggestedFilename(),/\.svg$/);assert.ok((await fs.readFile(await svg.path(),'utf8')).includes('<svg'));
await page.click('#save');const pngPromise=page.waitForEvent('download');await page.click('#save-png');const png=await pngPromise;assert.match(png.suggestedFilename(),/\.png$/);const pngBytes=await fs.readFile(await png.path());assert.equal(pngBytes[0],137);
await page.click('#converge');await page.waitForFunction(()=>document.getElementById('progress').textContent.startsWith('完成'),{},{timeout:120000});assert.equal(await page.locator('#convergence-plot svg').count(),1);await page.click('#close-dialog');
await page.evaluate(()=>window.scrollTo(0,0));if(process.env.QA_DIR){await page.screenshot({path:process.env.QA_DIR+'/desktop.png',fullPage:true});}
await page.setViewportSize({width:390,height:844});assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));if(process.env.QA_DIR){await page.screenshot({path:process.env.QA_DIR+'/mobile.png',fullPage:true});}
assert.deepEqual(errors,[]);console.log('Original-GUI layout: defaults, seven themes, reproducibility, dropdown presets, autoplay, SVG/PNG downloads, convergence, responsive width and JS errors checked.');await browser.close();
