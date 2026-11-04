// 오프라인 지원: 같은 출처는 네트워크 우선(실패 시 캐시), CDN 라이브러리는 캐시 우선
const V = 'tk-sw-1';
self.addEventListener('install', e => { self.skipWaiting(); });
self.addEventListener('activate', e => { e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== V).map(k => caches.delete(k)))).then(() => self.clients.claim())); });
self.addEventListener('fetch', e => {
  const r = e.request; if (r.method !== 'GET') return;
  const u = new URL(r.url);
  const same = u.origin === location.origin;
  const lib = /(^|\.)unpkg\.com$|cdn\.jsdelivr\.net$|cdnjs\.cloudflare\.com$|fonts\.(googleapis|gstatic)\.com$/.test(u.hostname);
  if (!same && !lib) return;
  if (same && u.searchParams.has('v')) return;
  if (lib) {
    e.respondWith(caches.open(V).then(c => c.match(r).then(m => m || fetch(r).then(n => { if (n.ok || n.type === 'opaque') c.put(r, n.clone()); return n; }))));
    return;
  }
  e.respondWith(fetch(r).then(n => { if (n.ok) { const cp = n.clone(); caches.open(V).then(c => c.put(r, cp)); } return n; }).catch(() => caches.match(r).then(m => m || caches.match('/'))));
});
