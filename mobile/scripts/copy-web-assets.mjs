import { cp, mkdir, access, readFile, writeFile } from 'node:fs/promises';
const rootFiles=['index.html','manifest.json','icon-180.png','icon-192.png','icon-512.png'];
await mkdir('www',{recursive:true});
for(const file of rootFiles){await access('../'+file);await cp('../'+file,'www/'+file)}
const path='www/index.html';let html=await readFile(path,'utf8');
if(!html.includes('src="./tracker.js"')){if(!html.includes('</body>'))throw new Error('index.html does not contain </body>');html=html.replace('</body>','<script src="./tracker.js"></script>\n</body>');await writeFile(path,html)}
console.log('Copied the site and injected the mobile GPS tracker.');
