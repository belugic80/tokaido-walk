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

OVR = {0:['Matsumoto Kiyoshi drugstore','ドラッグストア 日本 店舗'],1:['品川宿','Shinagawa-juku'],4:['大磯 松並木','Oiso pine tree road'],7:['かまぼこ 小田原','kamaboko'],16:['源兵衛川'],24:['白隠正宗'],25:['蒲原宿'],33:['清水港 マグロ','Shimizu port'],48:['蓬莱橋','Horai Bridge Shimada'],52:['掛川茶','Kakegawa tea'],54:['浜松 うなぎ','unagi kabayaki'],55:['浜松餃子','Hamamatsu gyoza'],57:['浜松餃子','Hamamatsu gyoza'],59:['舞阪 松並木'],61:['潮見坂'],65:['ちくわ 豊橋','chikuwa'],67:['いなり寿司','inarizushi'],69:['藤川宿'],74:['有松 町並み','Arimatsu'],75:['有松 絞'],76:['有松 絞'],81:['味噌カツ','手羽先','きしめん'],82:['桑名 蛤','Hamaguri clam'],83:['しぐれ蛤'],88:['関の戸'],93:['石部宿'],98:['鮒ずし'],100:['滋賀 日本酒'],101:['三条大橋','Sanjo Ohashi'],103:['ドン・キホーテ','Don Quijote store']}

def cores(s):
    out = []
    for term in (s.get('jp'), s['ko']):
        for p in re.split(r'[\s/／・·,()（）:：]+', term or ''):
            p = p.strip()
            if len(p) >= 2 and p not in out and not re.fullmatch(r'[0-9A-Za-z.]+', p): out.append(p)
    return out

def wiki_img(term):
    # 위키백과(일/영/한) 항목의 대표 사진 → 커먼즈 라이선스 확인. 항목 제목이 이름과 겹칠 때만 사용
    for lang in ('ja', 'en', 'ko'):
        r = get(f'https://{lang}.wikipedia.org/w/api.php?' + urllib.parse.urlencode({'action': 'query', 'format': 'json', 'generator': 'search', 'gsrsearch': term, 'gsrlimit': 3, 'prop': 'pageimages', 'piprop': 'name', 'redirects': 1}))
        for pg in sorted((r or {}).get('query', {}).get('pages', {}).values(), key=lambda x: x.get('index', 9)):
            t = pg.get('title', '')
            if not pg.get('pageimage') or not (term in t or t in term): continue
            c = info(['File:' + pg['pageimage']])
            if c: return c[0]
    return None

def pick(s, idx=None):
    for term in OVR.get(idx, []):
        r = q(list='search', srsearch=term, srnamespace=6, srlimit=12)
        t = [x['title'] for x in (r or {}).get('query', {}).get('search', [])]
        c = info(t[:12]) if t else []
        if c: return c[0], 'query'
    if OVR: return None, None
    for term in cores(s):
        c = wiki_img(term)
        if c: return c, 'wiki'
    for term in cores(s):
        r = q(list='search', srsearch=term, srnamespace=6, srlimit=10)
        t = [x['title'] for x in (r or {}).get('query', {}).get('search', []) if term in x['title']]
        c = info(t[:10]) if t else []
        if c: return c[0], 'name'
    return None, None

def main():
    spots = json.load(open(os.path.join(ROOT, 'build/spots.json')))
    outdir = os.path.join(ROOT, 'assets/spots'); os.makedirs(outdir, exist_ok=True)
    meta_p = os.path.join(ROOT, 'build/spot_photos.json')
    meta = json.load(open(meta_p)) if os.path.exists(meta_p) else {}
    for i, s in enumerate(spots):
        k = str(i)
        if k in meta and os.path.exists(os.path.join(ROOT, 'assets/spots', meta[k]['file'])): continue
        c, how = pick(s, i); time.sleep(0.4)
        if not c: print(i, s['ko'], '-> 사진 없음'); continue
        d = get(c['url'], True)
        if not d or len(d) < 20000: print(i, s['ko'], '-> 내려받기 실패'); continue
        fn = f'{i:03d}.jpg'; open(os.path.join(outdir, fn), 'wb').write(d)
        meta[k] = {'file': fn, 'credit': f"{c['author']} · {c['license']} · Wikimedia Commons", 'page': c['page'], 'how': how, 'title': c['title']}
        print(i, s['ko'], '->', how, c['title'][:60]); time.sleep(0.4)
    json.dump(meta, open(meta_p, 'w'), ensure_ascii=False, indent=1)
    print('총', len(meta), '/', len(spots))
main()
