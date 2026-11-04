const { chromium } = require('playwright'); const fs=require('fs');
const src=fs.readFileSync('/tmp/s/erx4.js','utf8');const NM='/tmp/s/node_modules/';const M=eval('('+src.match(/const M=(\{[^;]*\});/)[1]+')');
(async()=>{const b=await chromium.launch();const pg=await (await b.newContext({viewport:{width:1237,height:1100}})).newPage();
await pg.route('https://unpkg.com/**',r=>{const u=r.request().url();const k=Object.keys(M).find(k=>u.includes(k));if(k)return r.fulfill({body:fs.readFileSync(M[k]),contentType:'text/javascript'});r.abort();});
await pg.route(/fonts\.|tile\.openstreet|supabase|open-meteo|er-api|nominatim|jsdelivr|routing\.|maps\.google|gsi/, r=>r.abort());
await pg.goto('http://localhost:8960/new9/index.html?demo=1');await pg.waitForTimeout(3000);
await pg.mouse.move(600,600);await pg.mouse.wheel(0,900);await pg.waitForTimeout(500);
await pg.locator('div',{hasText:'가나야 돌길'}).last().click({force:true});await pg.waitForTimeout(700);
const before=await pg.evaluate(()=>!!document.querySelector('[data-screen-label="명물 팝업"]'));
for (const [x,y] of [[150,300],[150,700],[1100,700],[150,1000]]) { await pg.mouse.click(x,y); await pg.waitForTimeout(500);
 const st=await pg.evaluate(()=>({pop:!!document.querySelector('[data-screen-label="명물 팝업"]'),full:!!document.querySelector('[data-screen-label="지도 전체 화면"]')&&document.querySelector('[data-screen-label="지도 전체 화면"]').offsetParent!==null}));
 console.log(x,y,JSON.stringify(st)); if(!st.pop){ await pg.locator('div',{hasText:'가나야 돌길'}).last().click({force:true}).catch(()=>{}); await pg.waitForTimeout(600);} }
console.log('opened',before);await b.close();})();
