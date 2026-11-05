#!/usr/bin/env python3
"""명물(build/spots.json)별 사진을 위키미디어 커먼즈에서 찾아 assets/spots/에 저장.
- 좌표 주변(400m) 사진 우선, 없으면 일본어 이름 검색. 자유 이용 라이선스(CC BY, CC BY-SA, CC0, 퍼블릭 도메인)만 사용.
- 출처·작가·라이선스는 build/spot_photos.json에 기록."""
import json, os, re, sys, time, urllib.parse, urllib.request
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA = {'User-Agent': 'tokaido-walk-photo-fetch/1.0 (https://github.com/belugic80/tokaido-walk; personal project)'}
API = 'https://commons.wikimedia.org/w/api.php'
OKLIC = re.compile(r'^(CC BY(-SA)?( [0-9.]+)?|CC0.*|Public domain|PD.*|Attribution.*|.*public domain.*)$', re.I)
BAD = re.compile(r'logo|map|diagram|chart|flag|\.svg|\.png|\.gif|\.tif|\.pdf|sign|poster|stamp|ticket|menu', re.I)

def get(url, binary=False):
    for i in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
                d = r.read(); return d if binary else json.loads(d)
        except Exception as e:
            time.sleep(1.5 * (i + 1))
    return None

def q(**p):
    p.update(format='json', action='query'); return get(API + '?' + urllib.parse.urlencode(p))

def info(titles):
    r = q(titles='|'.join(titles), prop='imageinfo', iiprop='url|extmetadata|size|mime', iiurlwidth=900)
    out = []
    for pg in (r or {}).get('query', {}).get('pages', {}).values():
        ii = (pg.get('imageinfo') or [None])[0]
        if not ii or ii.get('mime') != 'image/jpeg' or ii.get('width', 0) < 900 or ii.get('width', 0) < ii.get('height', 0) * 0.9: continue
        m = ii.get('extmetadata', {}); lic = (m.get('LicenseShortName', {}).get('value') or '').strip()
        if not OKLIC.match(lic) or BAD.search(pg['title']): continue
        auth = re.sub(r'<[^>]+>', '', m.get('Artist', {}).get('value') or '').strip()[:80] or '작가 미상'
        out.append({'title': pg['title'], 'url': ii.get('thumburl') or ii['url'], 'page': ii['descriptionurl'], 'author': auth, 'license': lic})
    return out

def pick(s):
    ll = s.get('ll')
    if ll:
        r = q(list='geosearch', gscoord=f'{ll[0]}|{ll[1]}', gsradius=400, gsnamespace=6, gslimit=15)
        t = [x['title'] for x in (r or {}).get('query', {}).get('geosearch', []) if not BAD.search(x['title'])]
        c = info(t[:10]) if t else []
        if c: return c[0], 'geo'
    for term in (s.get('jp'), s['ko']):
        if not term: continue
        r = q(list='search', srsearch=term + ' filetype:bitmap', srnamespace=6, srlimit=10)
        t = [x['title'] for x in (r or {}).get('query', {}).get('search', [])]
        c = info(t[:10]) if t else []
        if c: return c[0], 'search'
    return None, None

def main():
    spots = json.load(open(os.path.join(ROOT, 'build/spots.json')))
    outdir = os.path.join(ROOT, 'assets/spots'); os.makedirs(outdir, exist_ok=True)
    meta_p = os.path.join(ROOT, 'build/spot_photos.json')
    meta = json.load(open(meta_p)) if os.path.exists(meta_p) else {}
    for i, s in enumerate(spots):
        k = str(i)
        if k in meta and os.path.exists(os.path.join(ROOT, 'assets/spots', meta[k]['file'])): continue
        c, how = pick(s); time.sleep(0.4)
        if not c: print(i, s['ko'], '-> 사진 없음'); continue
        d = get(c['url'], True)
        if not d or len(d) < 20000: print(i, s['ko'], '-> 내려받기 실패'); continue
        fn = f'{i:03d}.jpg'; open(os.path.join(outdir, fn), 'wb').write(d)
        meta[k] = {'file': fn, 'credit': f"{c['author']} · {c['license']} · Wikimedia Commons", 'page': c['page'], 'how': how, 'title': c['title']}
        print(i, s['ko'], '->', how, c['title'][:60]); time.sleep(0.4)
    json.dump(meta, open(meta_p, 'w'), ensure_ascii=False, indent=1)
    print('총', len(meta), '/', len(spots))
main()
