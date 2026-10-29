import { cp, mkdir, access } from 'node:fs/promises';

const rootFiles = ['index.html', 'manifest.json', 'icon-180.png', 'icon-192.png', 'icon-512.png'];

await mkdir('www', { recursive: true });
for (const file of rootFiles) {
  await access(file);
  await cp(file, `www/${file}`);
}
console.log('Copied static site files to www/.');
