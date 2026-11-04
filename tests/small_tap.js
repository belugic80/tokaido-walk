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
const rep=await pg.evaluate(()=>{const o=[];document.querySelectorAll('button,[role=button],[onclick]').forEach(e=>{const r=e.getBoundingClientRect();if(r.width>0&&r.height>0&&(r.height<44||r.width<44)&&r.width<120)o.push(Math.round(r.width)+'x'+Math.round(r.height)+' '+(e.textContent||'').trim().slice(0,12)+' | '+(e.getAttribute('style')||'').slice(0,60))});return o});console.log(rep.length+'\n'+rep.join('\n'));await b.close();})();
