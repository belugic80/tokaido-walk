import openpyxl, json, datetime, re, sys, os

SRC = sys.argv[1]
OUT = sys.argv[2]
wb = openpyxl.load_workbook(SRC, data_only=True)

_HERE0 = os.path.dirname(os.path.abspath(__file__))
HERO_DIR = os.path.join(_HERE0, '..', 'assets', 'hero')
HERO_DAYS = set()
if os.path.isdir(HERO_DIR):
    for f in os.listdir(HERO_DIR):
        m = re.match(r'^(\d+)\.jpg$', f)
        if m:
            HERO_DAYS.add(int(m.group(1)))


def v(x):
    if x is None:
        return None
    if isinstance(x, datetime.time):
        return x.strftime('%H:%M')
    if isinstance(x, datetime.timedelta):
        s = int(x.total_seconds())
        return f"{s // 3600}:{(s % 3600) // 60:02d}"
    if isinstance(x, float):
        return round(x, 2)
    if isinstance(x, str):
        return x.strip()
    return x


def rows(name, hr):
    ws = wb[name]
    out = {}
    for r in ws.iter_rows(min_row=hr + 1, values_only=True):
        if isinstance(r[0], (int, float)):
            out[int(r[0])] = [v(c) for c in r]
    return out


A = rows('전체 일정', 4)
M = rows('이동 상세', 5)
R = rows('경로 좌표', 5)
rate = wb['이동 상세'].cell(3, 2).value or 8.445


def one(s):
    return re.sub(r'\s*\n\s*', ' ', s) if s else s


def steps(s):
    if not s:
        return []
    parts = re.split(r'(?=(?:교통|걷기|관광)\))', s.replace('\n', ' '))
    out = []
    for p in parts:
        p = p.strip().rstrip(',').strip()
        m = re.match(r'(교통|걷기|관광)\)\s*(.*)', p)
        if m:
            out.append({'k': m.group(1), 't': m.group(2).strip()})
    return out


sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from photos import P as PH
from photos_extra import X as XT
from photos_extra2 import X2
for _n, _v in X2.items():
    for _k, _l in _v.items():
        XT.setdefault(_n, {}).setdefault(_k, []).extend(_l)
AG = {}
_ws = wb['이동 상세']
for _r in range(6, _ws.max_row + 1):
    _n = _ws.cell(_r, 1).value
    _h = _ws.cell(_r, 23).hyperlink
    if isinstance(_n, (int, float)) and _h and _h.target:
        AG[int(_n)] = _h.target
import math
def hav(p, q):
    la1, lo1 = map(float, p.split(',')); la2, lo2 = map(float, q.split(','))
    r = math.radians; dla, dlo = r(la2 - la1), r(lo2 - lo1)
    h = math.sin(dla / 2) ** 2 + math.cos(r(la1)) * math.cos(r(la2)) * math.sin(dlo / 2) ** 2
    return 6371 * 2 * math.asin(math.sqrt(h))
def nodes_of(route, km):
    # 경로 지점마다 그날 출발점에서의 거리(km): 직선거리 비율로 그날 걷는 거리에 맞춤
    if len(route) < 2 or not km: return []
    seg = [hav(route[i]['ll'], route[i + 1]['ll']) for i in range(len(route) - 1)]
    tot = sum(seg) or 1; out = [0.0]
    for x in seg: out.append(out[-1] + x / tot * km)
    return [round(v, 1) for v in out]
days = []
for n in sorted(A):
    a, m, r = A[n], M.get(n, [None] * 23), R.get(n)
    route = []
    if r:
        for i in range(2, 12, 2):
            if r[i] and r[i + 1]:
                route.append({'name': r[i], 'll': str(r[i + 1]).replace(' ', '')})
    days.append({
        'n': n, 'date': a[1], 'dow': a[2], 'region': a[3], 'stay': one(a[4]), 'nights': a[5],
        'type': a[6], 'km': a[7] or 0, 'wt': a[8], 'start': m[15] or a[9], 'arrive': m[16] or a[10],
        'spare': a[11], 'sunset': m[17], 'character': (a[12] or '').strip(),
        'stations': [s.strip() for s in (a[13] or '').split('\n') if s.strip()],
        'steps': steps(a[14]),
        'spots': a[20], 'food': a[21], 'crafts': a[22], 'history': a[23], 'now': a[24], 'memo': a[25],
        'walkSeg': m[6] if isinstance(m[6], str) else None,
        'trSeg': m[9], 'trKm': m[10], 'trMin': m[11], 'rides': m[12], 'yen': m[13], 'mdMemo': m[14],
        'h1': m[19], 'h2': m[20], 'route': route, 'mapUrl': r[13] if r else None,
        'agoda': AG.get(n), 'photos': {k: [list(x) + ['', 0] for x in PH.get(n, {}).get(k, [])] + [list(x) + [1] for x in XT.get(n, {}).get(k, [])] for k in ('s', 'f', 'c')},
        'stayQ': PH.get(n, {}).get('stay'),
        'nodes': nodes_of(route, a[7] or 0),
        'hero': n in HERO_DAYS,
    })


def red(cell):
    f = cell.font
    return bool(f and f.b and f.color is not None and f.color.rgb not in (None, 'FF000000'))


tips = []
ws = wb['여행 전 알아둘 것']
for r in range(5, ws.max_row + 1):
    c = [ws.cell(r, i).value for i in range(1, 4)]
    if c[0] and c[2]:
        tips.append({'cat': c[0], 'title': c[1], 'body': c[2], 'must': red(ws.cell(r, 3)) or red(ws.cell(r, 2))})

ja = []
ws = wb['일본어']
for r in range(5, ws.max_row + 1):
    c = [ws.cell(r, i).value for i in range(1, 7)]
    if c[0] and c[2]:
        ja.append({'cat': c[0], 'sit': c[1], 'ko': c[2], 'ja': c[3], 'pr': c[4], 'tip': c[5], 'must': red(ws.cell(r, 3))})

# 화장실 관련 필수 문장 (몸·긴급에 추가)
JA_EXTRA = [
    ('화장실', '화장실은 어디예요?', 'トイレはどこですか？', '토이레와 도코데스카?'),
    ('화장실', '화장실 좀 써도 될까요?', 'トイレを借りてもいいですか？', '토이레오 카리테모 이-데스카?'),
    ('화장실', '근처에 공중화장실이 있나요?', '近くに公衆トイレはありますか？', '치카쿠니 코-슈- 토이레와 아리마스카?'),
    ('화장실', '화장실이 급해요', 'トイレに急いで行きたいです。', '토이레니 이소이데 이키타이데스'),
    ('화장실', '남자 화장실은 어느 쪽이에요?', '男性用トイレはどちらですか？', '단세-요- 토이레와 도치라데스카?'),
    ('화장실', '휴지가 없어요', 'トイレットペーパーがありません。', '토이렛토 페-파-가 아리마셍'),
    ('화장실', '물이 안 내려가요', '水が流れません。', '미즈가 나가레마셍'),
]
ja = [j for j in ja if not (j['ko'] == '화장실은 어디예요?')]
ja = [{'cat': '몸·긴급', 'sit': s, 'ko': k, 'ja': j, 'pr': pr, 'tip': None, 'must': True} for s, k, j, pr in JA_EXTRA] + ja
title_ws = wb['전체 일정']
data = {
    'title': title_ws.cell(1, 1).value, 'sub': title_ws.cell(2, 1).value, 'rate': rate,
    'days': days, 'tips': tips, 'ja': ja,
}
import os
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA_JSON = json.dumps(data, ensure_ascii=False)

# ── 새 디자인 화면 (/, /today, /records, /plan, /map, /japanese, /guide) ──
main_tpl = open(os.path.join(HERE, 'template_main.html'), encoding='utf-8').read()
main_html = main_tpl.replace('/*__DATA__*/null', DATA_JSON)
NEW_TABS = {
    'today': 'today', 'journey': 'journey', 'records': 'record', 'plan': 'schedule',
    'map': 'map', 'more': 'more', 'japanese': 'lang', 'guide': 'info',
}

# ── 홈(/) = 클로드 디자인 v15 파일 그대로 ─────────────────────────────
# design/ 의 원본은 손대지 않고, 폰 테두리 프레임만 걷어내 화면에 꽉 차게 내보냄
DESIGN = os.path.join(ROOT, 'design')
dc = open(os.path.join(DESIGN, 'Tokaido Today v15.dc.html'), encoding='utf-8').read()
FRAME = [
    ('<div style="min-height:100vh;display:flex;flex-direction:column;align-items:safe center;justify-content:safe center;gap:14px;padding:36px 24px;box-sizing:border-box;overflow-x:auto">',
     '<div style="min-height:100vh;display:flex;justify-content:center;box-sizing:border-box">'),
    ('width:1000px;height:960px;flex:none;border-radius:34px;', 'width:100%;max-width:1000px;height:100dvh;flex:none;border-radius:0;'),
    ('box-shadow:0 0 0 9px #15181B,0 0 0 10px #3B4147,0 36px 80px rgba(23,43,61,.3);', ''),
]
for a_, b_ in FRAME:
    assert dc.count(a_) == 1, a_
    dc = dc.replace(a_, b_)
# 가짜 상태 표시줄(9:41·5G·배터리)과 카메라 점 제거
dc, k = re.subn(r'<div style="flex:none;height:32px;display:flex;align-items:center;justify-content:space-between;padding:0 24px 0 50px;font:600 12px system-ui;color:#20202A">\n<span>9:41</span>.*?</div>\n</div>\n<div style="position:absolute;top:10px;left:24px;width:12px;height:12px;border-radius:50%;background:#0b0d0f;z-index:1001"></div>\n', '', dc, count=1, flags=re.S)
assert k == 1
# 휴대폰에서는 디자인 폭(1000px) 그대로 화면에 맞춰 축소해서 보이게 함
assert dc.count('<meta name="viewport" content="width=device-width, initial-scale=1">') == 1
dc = dc.replace('<meta name="viewport" content="width=device-width, initial-scale=1">', '<meta name="viewport" content="width=1000">')
open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8').write(dc)
import shutil as _sh
for f in ('support.js', 'image-slot.js'):
    _sh.copyfile(os.path.join(DESIGN, f), os.path.join(ROOT, f))
os.makedirs(os.path.join(ROOT, 'assets'), exist_ok=True)
for f in os.listdir(os.path.join(DESIGN, 'assets')):
    _sh.copyfile(os.path.join(DESIGN, 'assets', f), os.path.join(ROOT, 'assets', f))


# ── 히어로 사진(실제 폴더 사진): assets/hero/*.jpg → /hero/*.jpg로 그대로 배포 ──
import shutil
if os.path.isdir(HERO_DIR):
    out_hero = os.path.join(ROOT, 'hero')
    os.makedirs(out_hero, exist_ok=True)
    for f in os.listdir(HERO_DIR):
        if re.match(r'^\d+\.jpg$', f):
            shutil.copyfile(os.path.join(HERO_DIR, f), os.path.join(out_hero, f))

# ── 예전 화면 (옛 디자인 그대로, 탭만 다르게 열림) ──────────────────────
old_tpl = open(os.path.join(HERE, 'template.html'), encoding='utf-8').read()
old_html = old_tpl.replace('/*__DATA__*/null', DATA_JSON)
OLD_TABS = {
    'old_home': 'day', 'old_today': 'day', 'old_plan': 'all', 'old_records': 'rec',
    'old_itinerary': 'all', 'old_japanese': 'ja', 'old_guide': 'tips',
}
for name, tab in OLD_TABS.items():
    html = old_html.replace('</body>', f'<script>setTab("{tab}");</script>\n</body>')
    open(os.path.join(ROOT, f'{name}.html'), 'w', encoding='utf-8').write(html)

print('days', len(days), 'tips', len(tips), 'ja', len(ja), 'routes', sum(1 for d in days if d['route']))
print('wrote index.html (v15) +', len(OLD_TABS), 'old_*.html')
