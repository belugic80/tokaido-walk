const { chromium } = require('playwright'); const fs=require('fs');
const src=fs.readFileSync('/tmp/s/erx4.js','utf8');const NM='/tmp/s/node_modules/';const M=eval('('+src.match(/const M=(\{[^;]*\});/)[1]+')');
(async()=>{const b=await chromium.launch();const pg=await (await b.newContext({viewport:{width:1000,height:3200}})).newPage();
await pg.route('https://unpkg.com/**',r=>{const u=r.request().url();const k=Object.keys(M).find(k=>u.includes(k));if(k)return r.fulfill({body:fs.readFileSync(M[k]),contentType:'text/javascript'});r.abort();});
await pg.route(/fonts\.|tile\.openstreet|supabase|open-meteo|er-api|nominatim|jsdelivr|routing\.|maps\.google|gsi/, r=>r.abort());
await pg.goto('http://localhost:8960/new9/index.html?demo=1');await pg.waitForTimeout(3000);
await pg.locator('div,button',{hasText:'기록'}).last().click({force:true});await pg.waitForTimeout(900);
const r=await pg.evaluate(()=>{const g=[...document.querySelectorAll('div')].filter(d=>d.style.display==='grid'&&d.children.length===2&&d.textContent.includes('체중 변화'));const o=g.map(x=>[...x.children].map(c=>({b:Math.round(c.getBoundingClientRect().bottom),kids:[...c.children].map(k=>Math.round(k.getBoundingClientRect().top)+'-'+Math.round(k.getBoundingClientRect().bottom)+' '+k.textContent.slice(0,8))})));return o[o.length-1]});
console.log(JSON.stringify(r,null,1));await b.close();})();

