const { chromium } = require('playwright'); const fs=require('fs');
const NM='/tmp/s/node_modules/';
const M={'react@18.3.1/umd/react.production.min.js':NM+'react/umd/react.production.min.js','react-dom@18.3.1/umd/react-dom.production.min.js':NM+'react-dom/umd/react-dom.production.min.js','leaflet@1.9.4/dist/leaflet.js':NM+'leaflet/dist/leaflet.js','leaflet@1.9.4/dist/leaflet.css':NM+'leaflet/dist/leaflet.css'};
(async()=>{const [w,h,out,...acts]=process.argv.slice(2);const b=await chromium.launch();const ctx=await b.newContext({viewport:{width:+w,height:+h}});const pg=await ctx.newPage();
pg.on('console',m=>{if(m.type()==='error'&&!/Failed to load|Expected/.test(m.text()))console.log('CE',m.text().slice(0,500))});
await pg.route('https://unpkg.com/**',r=>{const u=r.request().url();const k=Object.keys(M).find(k=>u.includes(k));if(k)return r.fulfill({body:fs.readFileSync(M[k]),contentType:k.endsWith('css')?'text/css':'application/javascript',headers:{'access-control-allow-origin':'*'}});r.abort()});
await pg.route(/fonts\.|tile\.openstreet|supabase|open-meteo|er-api|nominatim|jsdelivr|routing\.|maps\.google/, r=>r.abort());
await pg.goto(''+''+(process.env.U||'http://localhost:8960/new9/index.html?demo=1')+'');await pg.waitForTimeout(3500);
for(const a of acts){const [k,v]=[a.slice(0,a.indexOf(':')),a.slice(a.indexOf(':')+1)];
 if(k==='t'){await pg.locator('button,[role=button],div',{hasText:v}).last().click({timeout:3000,force:true}).catch(e=>console.log('noclick',v));}
 if(k==='g'){await pg.evaluate(t=>{const b=[...document.querySelectorAll('button')].filter(x=>x.textContent.trim()===t&&x.offsetParent&&x.getBoundingClientRect().width<80&&x.parentElement.style.position==='absolute');if(b[0])b[0].click();},v);}
 if(k==='a'){await pg.locator('[aria-label="'+v+'"]').first().click({force:true});}
 if(k==='s'){await pg.mouse.move(+w/3,+h/2);await pg.mouse.wheel(0,+v);}
 if(k==='p'){await pg.screenshot({path:'/tmp/s/'+out+'_'+v+'.png'});}
 await pg.waitForTimeout(700);}
const rep=await pg.evaluate(()=>{const out=[];document.querySelectorAll('div').forEach(g=>{const cs=getComputedStyle(g);if(!(cs.display==='grid'||(cs.display==='flex'&&cs.flexDirection==='row')))return;const k=[...g.children].filter(c=>{const r=c.getBoundingClientRect();const b=parseFloat(getComputedStyle(c).borderTopLeftRadius);return r.width>120&&r.height>40&&b>=16});if(k.length<2)return;const tops=k.map(c=>Math.round(c.getBoundingClientRect().top));const bots=k.map(c=>Math.round(c.getBoundingClientRect().bottom));if(new Set(tops).size>1)return;if(Math.max(...bots)-Math.min(...bots)>3)out.push({bots,txt:k.map(c=>c.textContent.trim().slice(0,10))})});return out});console.log(JSON.stringify(rep));await b.close();})();
