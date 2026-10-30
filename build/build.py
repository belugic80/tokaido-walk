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
# 새로고침해도 보던 메뉴(탭)·하위 메뉴·날짜가 유지되도록 저장/복원만 추가
RESTORE = [
    ("lodgeOk: false, tab: 0, mapMode: 'route', view: null,",
     "lodgeOk: false, tab: (() => { try { const v = +localStorage.getItem('tk-v15-tab'); return v >= 0 && v <= 7 ? v : 0; } catch (e) { return 0; } })(), moreSub: (() => { try { return localStorage.getItem('tk-v15-sub') || undefined; } catch (e) { return undefined; } })(), mapMode: 'route', view: (() => { try { const v = +localStorage.getItem('tk-v15-view'); return v >= 1 && v <= 31 ? v : null; } catch (e) { return null; } })(),"),
    ("  componentDidUpdate() { this.loadDay(this.view());",
     "  componentDidUpdate() { try { localStorage.setItem('tk-v15-tab', this.state.tab); localStorage.setItem('tk-v15-sub', this.state.moreSub || ''); localStorage.setItem('tk-v15-view', this.state.view ?? ''); } catch (e) {} this.loadDay(this.view());"),
]
for a_, b_ in RESTORE:
    assert dc.count(a_) == 1, a_
    dc = dc.replace(a_, b_)
# 일본어 탭 글자 키우기 (사용자 요청)
BIGGER = [
    ("font:700 34px/1.4 'Noto Serif JP',serif;word-break:normal;", "font:700 52px/1.4 'Noto Serif JP',serif;word-break:normal;"),
    ("font-size:30px;font-weight:800;line-height:1.35;letter-spacing:-.01em;color:#CDBBFF;", "font-size:44px;font-weight:800;line-height:1.35;letter-spacing:-.01em;color:#BFD8FF;"),
    ("font-size:18px;font-weight:600;padding-top:12px;border-top:1px solid rgba(255,255,255,.18);min-width:60%;", "font-size:30px;font-weight:600;padding-top:12px;border-top:1px solid rgba(255,255,255,.18);min-width:60%;"),
    ("height:44px;padding:0 13px;border-radius:10px;border:0;background:{{ f.bg }};color:{{ f.color }};font-size:12.5px;", "height:48px;padding:0 16px;border-radius:10px;border:0;background:{{ f.bg }};color:{{ f.color }};font-size:16px;"),
    ('<div style="padding:12px 14px;border-radius:14px;cursor:pointer;background:{{ p.bg }};border:1.5px solid {{ p.border }}" style-hover="background:#FFFFFF"><div style="font-size:15px;font-weight:700;line-height:1.45;color:#20202A">{{ p.ko }}</div><div style="font-size:15px;font-weight:700;line-height:1.45;color:#673DE6;margin-top:4px">{{ p.read }}</div></div>'.replace('<div style="padding','<div onClick="{{ p.open }}" style="padding'),
     '<div onClick="{{ p.open }}" style="padding:16px 18px;border-radius:14px;cursor:pointer;background:{{ p.bg }};border:1.5px solid {{ p.border }}" style-hover="background:#FFFFFF"><div style="font-size:20px;font-weight:700;line-height:1.45;color:#20202A">{{ p.ko }}</div><div style="font-size:20px;font-weight:700;line-height:1.45;color:#673DE6;margin-top:4px">{{ p.read }}</div></div>'),
    ("font-size:18px;font-weight:800;white-space:nowrap\">일본어</div>", "font-size:22px;font-weight:800;white-space:nowrap\">일본어</div>"),
]
for a_, b_ in BIGGER:
    assert dc.count(a_) == 1, a_
    dc = dc.replace(a_, b_)
# 여행 정보 탭: 눈이 좋지 않은 사용자를 위해 전체를 크게 (사용자 요청)
INFO_OLD = '<sc-if value="{{ tabInfo }}" hint-placeholder-val="{{ false }}">\n<div style="flex:1;min-height:0;overflow-y:auto;scrollbar-width:none;padding:0 20px 24px 24px;display:flex;flex-direction:column;gap:12px">'
INFO_NEW = '<sc-if value="{{ tabInfo }}" hint-placeholder-val="{{ false }}">\n<div style="flex:1;min-height:0;overflow-y:auto;scrollbar-width:none;padding:0 20px 24px 24px;display:flex;flex-direction:column;gap:12px;zoom:1.4">'
assert dc.count(INFO_OLD) == 1
dc = dc.replace(INFO_OLD, INFO_NEW)
SC_OLD = '<div style="flex:none;height:400px;background:linear-gradient(135deg,rgba(24,43,61,.94),rgba(45,23,111,.86))'
assert dc.count(SC_OLD) == 1
dc = dc.replace(SC_OLD, '<div data-showcard="1" style="cursor:pointer;flex:none;height:max(420px,calc(100dvh - 790px));background:linear-gradient(135deg,rgba(24,43,61,.94),rgba(45,23,111,.86))')
assert dc.count('길에서 바로 보여주세요</span>') == 1
dc = dc.replace('길에서 바로 보여주세요</span>', '눌러서 화면 가득 보여주기</span>')
# ── 일본어 탭: 보여주기 카드 10문장 + 오늘 숙소 카드 (예전 사이트 기능을 v15 일본어 탭으로) ──
import json as _json
def _lines(t): return [x.strip() for x in str(t or '').split('\n') if x.strip()]
def _hotel_day(i):
    hd = i
    while (not days[hd].get('h1') or '위와 같음' in days[hd]['h1']) and hd > 0 and days[hd - 1]['stay'] == days[i]['stay']:
        hd -= 1
    return hd
def _last_ll(i):
    for k in range(i, -1, -1):
        if days[k]['route']: return days[k]['route'][-1]['ll']
    return '35.0,138.5'
HOTELS = {}
for i, dd in enumerate(days):
    hd = days[_hotel_day(i)]
    first = (_lines(hd.get('h1')) or [''])[0]
    m = re.search(r'\(([A-Za-z][^)]*)\)', first)
    en = m.group(1) if m else (first.split(',')[0] if re.match(r'^[A-Za-z]', first) else '')
    ko = re.sub(r'\(.*?\)', '', re.split(r',|·', first)[0]).strip()
    # v15 디자인의 N일차는 엑셀의 (N+1)일차와 같은 구간이라, 숙소는 한 칸 뒤 행을 사용
    HOTELS[max(1, dd['n'] - 1)] = {'ko': ko, 'en': en, 'ja': hd.get('jaName') or '', 'addr': hd.get('jaAddr') or '', 'town': hd.get('stayQ') or '', 'll': _last_ll(i)}
HOTELS[31] = HOTELS.get(31) or HOTELS[30]
SHOW10 = [
  ['hotel', '숙소로 가 주세요', 'このホテルまでお願いします。'],
  ['checkin', '예약했어요, 체크인 부탁해요', '予約しています。チェックインをお願いします。'],
  ['bag', '짐을 맡아 주실 수 있나요?', '荷物を預かってもらえますか？'],
  ['road', '도카이도 옛길은 어느 쪽인가요?', '旧東海道はどちらですか？'],
  ['toilet', '화장실을 써도 될까요?', 'トイレを借りてもいいですか？'],
  ['pharm', '근처에 약국이 있나요?', '近くに薬局はありますか？'],
  ['hurt', '다리가 아파요. 병원에 가고 싶어요', '足が痛いです。病院に行きたいです。'],
  ['one', '한 명이에요', '一人です。'],
  ['pay', '계산 부탁해요', 'お会計をお願いします。'],
  ['photo', '사진 좀 찍어 주실래요?', '写真を撮ってもらえますか？'],
]
SC_BLOCK = ('<div style="grid-column:1/-1;background:linear-gradient(135deg,#E8F1FF 0%,#F4F8FF 100%);border:1px solid #CFE0FB;border-radius:20px;padding:18px 18px 16px;margin-bottom:8px">'
  '<div style="display:flex;justify-content:space-between;align-items:baseline;gap:10px"><div style="font-size:24px;font-weight:800;color:#1F5BD0">보여주기 카드</div><span style="font-size:16px;color:#3B6FD1;font-weight:600">누르면 화면 가득 크게</span></div>'
  '<div style="display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:10px;margin-top:14px">'
  + ''.join('<button type="button" data-show="%s" style="min-height:76px;padding:8px 14px;border-radius:16px;border:0;background:linear-gradient(135deg,#3979E8 0%%,#55A7EA 100%%);color:#fff;font-size:22px;font-weight:800;line-height:1.3;font-family:inherit;cursor:pointer;box-shadow:0 6px 14px rgba(57,121,232,.28)">%s</button>' % (k, ko) for k, ko, _ in SHOW10)
  + '</div></div>')
SC_GRID_OLD = '<div style="flex:1;min-height:0;overflow-y:auto;scrollbar-width:none;padding-bottom:16px;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:8px;align-content:start">\n<sc-for list="{{ phrases }}"'
assert dc.count(SC_GRID_OLD) == 1
dc = dc.replace(SC_GRID_OLD, SC_GRID_OLD.split('\n')[0] + '\n' + SC_BLOCK + '\n<sc-for list="{{ phrases }}"')
SC_JS = """<script>(function () {
  var HOTELS = %s, SHOW = %s;
  var curDay = function () { var m = (document.body.innerText.match(/DAY\\s*(\\d+)\\s*\\/\\s*31/) || [])[1]; return +m || 12; };
  var el = function (tag, css, txt) { var d = document.createElement(tag); if (css) d.style.cssText = css; if (txt != null) d.textContent = txt; return d; };
  document.addEventListener('click', function (e) {
    var b = e.target.closest && e.target.closest('[data-show]'); if (!b) return;
    var it = SHOW.filter(function (x) { return x[0] === b.getAttribute('data-show'); })[0]; if (!it) return;
    var ov = el('div', 'position:fixed;inset:0;z-index:5000;background:#0F2A5C;color:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;gap:24px;padding:40px 32px;box-sizing:border-box;overflow:auto');
    ov.setAttribute('role', 'dialog'); ov.setAttribute('aria-label', it[1]);
    ov.appendChild(el('div', "font:700 clamp(44px,9vw,84px)/1.35 'Noto Serif JP',serif;overflow-wrap:anywhere", it[2]));
    if (it[0] === 'hotel' || it[0] === 'checkin') {
      var h = HOTELS[curDay()] || {};
      var box = el('div', 'display:flex;flex-direction:column;gap:10px;align-items:center;background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.25);border-radius:22px;padding:22px 28px;max-width:100%%');
      if (h.ja) box.appendChild(el('div', "font:700 clamp(30px,6vw,52px)/1.3 'Noto Serif JP',serif", h.ja));
      if (h.en) box.appendChild(el('div', 'font-size:clamp(24px,4.6vw,38px);font-weight:700', h.en));
      if (h.ko) box.appendChild(el('div', 'font-size:clamp(22px,4vw,32px);opacity:.9', h.ko));
      var ad = h.addr || h.town; if (ad) box.appendChild(el('div', "font:500 clamp(20px,3.6vw,28px)/1.4 'Noto Serif JP',serif;opacity:.9", ad));
      var q = encodeURIComponent((h.ja || h.en || h.ko || '') + ' ' + (h.town || ''));
      var a = el('a', 'margin-top:6px;display:inline-flex;align-items:center;height:56px;padding:0 28px;border-radius:999px;background:#3979E8;color:#fff;font-size:22px;font-weight:800;text-decoration:none', '지도로 보여주기');
      a.href = 'https://www.google.com/maps/search/?api=1&query=' + (h.ll || q); a.target = '_blank'; a.rel = 'noopener'; box.appendChild(a);
      ov.appendChild(box);
    }
    ov.appendChild(el('div', 'font-size:clamp(26px,5vw,44px);font-weight:700;opacity:.92', it[1]));
    var close = function () { ov.remove(); try { if (document.fullscreenElement) document.exitFullscreen(); } catch (er) {} };
    var c = el('button', 'margin-top:8px;height:64px;padding:0 48px;border-radius:999px;border:0;background:#fff;color:#0F2A5C;font-size:26px;font-weight:800;font-family:inherit;cursor:pointer', '닫기');
    c.type = 'button'; c.onclick = close; ov.onclick = function (ev) { if (ev.target === ov) close(); };
    ov.appendChild(c); document.body.appendChild(ov);
    try { var r = document.documentElement.requestFullscreen({ navigationUI: 'hide' }); if (r && r.catch) r.catch(function () {}); } catch (er) {}
  });
})();</script>
""" % (_json.dumps(HOTELS, ensure_ascii=False), _json.dumps(SHOW10, ensure_ascii=False))
# 한눈에 탭: 사진 영역을 화면 높이에 맞춰 키워서, 사진·통계·역참 진행이 한 화면에 꽉 차게
G_OLD = 'grid-template-columns:2fr 1fr 1fr;grid-template-rows:96px 96px;gap:8px'
assert dc.count(G_OLD) == 1
dc = dc.replace(G_OLD, 'grid-template-columns:2fr 1fr 1fr;grid-template-rows:repeat(2,max(96px,calc((100dvh - GAPPX)/2)));gap:8px'.replace('GAPPX', '820px'))
M_OLD = '<div style="position:relative;height:430px;border-radius:16px;overflow:hidden;background:#F3F6FA">\n<div ref="{{ mapRef }}"'
assert dc.count(M_OLD) == 1
dc = dc.replace(M_OLD, M_OLD.replace('<div style="position:relative;height:430px', '<div data-h0="430" style="position:relative;height:430px'))
# 기록 탭: 사진과 한 줄 기록의 사진은 3장
P_OLD = 'dayPhotos: [1, 2, 3, 4].map('
assert dc.count(P_OLD) == 1
dc = dc.replace(P_OLD, 'dayPhotos: [1, 2, 3].map(')
P_GRID = '<div style="display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px;margin-top:12px"><sc-for list="{{ dayPhotos }}"'
assert dc.count(P_GRID) == 1
dc = dc.replace(P_GRID, P_GRID.replace('repeat(4,', 'repeat(3,'))
H_OLD = 'box-shadow:0 16px 40px rgba(15,42,74,.18);display:flex;flex-direction:column;min-width:0">'
assert dc.count(H_OLD) == 1
dc = dc.replace(H_OLD, 'box-shadow:0 16px 40px rgba(15,42,74,.18);display:flex;flex-direction:column;min-width:0">')
PI_OLD = '<div onClick="{{ p.open }}" style="padding:16px 18px;'
assert dc.count(PI_OLD) == 1
dc = dc.replace(PI_OLD, '<div data-phrase="1" onClick="{{ p.open }}" style="padding:16px 18px;')
dc = dc.replace('font-size:20px;font-weight:700;line-height:1.45;color:#673DE6;margin-top:4px', 'font-size:20px;font-weight:700;line-height:1.45;color:#2B6AE0;margin-top:4px')
# 오늘 탭: 날짜 이동 버튼(오늘로·‹·날짜·›)을 화면 아래쪽으로 내려 엄지가 닿게 (사용자 요청)
N_OLD = '<div style="display:flex;align-items:center;gap:6px">\n<sc-if value="{{ notToday }}"'
assert dc.count(N_OLD) == 1
dc = dc.replace(N_OLD, '<div style="position:fixed;left:calc(50% - 46px);bottom:2px;transform:translateX(-50%);z-index:1500;display:flex;align-items:center;gap:8px;padding:8px;border-radius:24px;background:rgba(24,43,61,.94);box-shadow:0 10px 28px rgba(15,42,74,.35)">\n<sc-if value="{{ notToday }}"')
# 오늘 탭: 위쪽 사진(히어로)은 고정, 아래 지도부터 스크롤 (사용자 요청)
HS_OLD = 'data-screen-label="Today hero" style="position:relative;flex:none;height:280px;border-radius:28px;overflow:hidden;background:#182B3D url({{ heroImg }}) center 42%/cover;box-shadow:0 16px 40px rgba(15,42,74,.16)"'
assert dc.count(HS_OLD) == 1
dc = dc.replace(HS_OLD, 'data-screen-label="Today hero" style="position:sticky;top:4px;z-index:1100;flex:none;height:330px;border-radius:28px;overflow:hidden;background:#182B3D url({{ heroImg }}) center 42%/cover;box-shadow:0 -14px 0 0 #F7F7FB,0 12px 0 0 #F7F7FB,0 16px 40px rgba(15,42,74,.16)"')
# 비상 연락처: 한 줄 4칸 유지 + 글자 키움
EM_OLD = '<div style="display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;margin-top:12px">\n<sc-for list="{{ calls }}"'
assert dc.count(EM_OLD) == 1
dc = dc.replace(EM_OLD, EM_OLD)
# 번호가 길면 잘리지 않고 줄바꿈되게 (한 줄 4칸 유지)
NUM_OLD = "font:700 20px 'DM Sans',sans-serif;letter-spacing:-.02em;white-space:nowrap;overflow:hidden;text-overflow:ellipsis"
assert dc.count(NUM_OLD) == 1, 'num'
dc = dc.replace(NUM_OLD, "font:700 21px 'DM Sans',sans-serif;letter-spacing:-.03em;white-space:normal;overflow-wrap:break-word;line-height:1.2")
# 전체 화면 버튼 (주소창 숨기기) — 예전 사이트에 있던 기능
FS = """<button id="fsBtn" aria-label="전체 화면" title="전체 화면" style="position:fixed;left:4px;bottom:4px;opacity:.85;z-index:2000;width:38px;height:38px;border-radius:50%;border:1px solid #E8E7EF;background:rgba(255,255,255,.94);box-shadow:0 4px 14px rgba(15,42,74,.18);display:grid;place-items:center;cursor:pointer;padding:0"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#20202A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M8 3H5a2 2 0 0 0-2 2v3M21 8V5a2 2 0 0 0-2-2h-3M3 16v3a2 2 0 0 0 2 2h3M16 21h3a2 2 0 0 0 2-2v-3"></path></svg></button>
<script>(function () {
  var fsBtn = document.getElementById('fsBtn');
  var goFs = function () { try { var r = document.documentElement.requestFullscreen({ navigationUI: 'hide' }); if (r && r.catch) r.catch(function () {}); } catch (e) {} };
  fsBtn.addEventListener('click', function () { try { if (document.fullscreenElement) document.exitFullscreen(); else goFs(); } catch (e) {} });
  /* 전체 화면을 기본으로: 브라우저 규칙상 첫 터치가 있어야 켤 수 있어서, 화면을 처음 누르는 순간 자동으로 켬 (홈 화면 아이콘으로 열면 처음부터 전체 화면) */
  /* 좌우 드래그 잠금: 지도 밖에서 가로로 끌면 화면이 미세하게 흔들리거나 크기가 바뀌지 않게 막음 */
  var sx = 0, sy = 0;
  document.addEventListener('touchstart', function (e) { if (e.touches.length === 1) { sx = e.touches[0].clientX; sy = e.touches[0].clientY; } }, { passive: true });
  document.addEventListener('touchmove', function (e) {
    if (e.touches.length > 1) { e.preventDefault(); return; }
    var dx = Math.abs(e.touches[0].clientX - sx), dy = Math.abs(e.touches[0].clientY - sy);
    if (dx > dy && !(e.target.closest && e.target.closest('.leaflet-container,input,textarea'))) e.preventDefault();
  }, { passive: false });
  window.scrollTo(0, 0); window.addEventListener('scroll', function () { if (window.scrollX) window.scrollTo(0, window.scrollY); }, { passive: true });
  var inApp = window.matchMedia('(display-mode: fullscreen)').matches || window.matchMedia('(display-mode: standalone)').matches || navigator.standalone;
  var auto = function () { document.removeEventListener('pointerup', auto, true); if (!inApp && !document.fullscreenElement) goFs(); };
  document.addEventListener('pointerup', auto, true);
  /* 일본어 탭: 문장 카드를 누르면 화면 가득 크게(보여주기 카드) + 전체 화면 */
  document.addEventListener('click', function (e) {
    var card = e.target.closest && e.target.closest('[data-showcard]');
    if (!card || e.target.closest('button')) return;
    var t = card.querySelectorAll(':scope > div:nth-child(2) > div');
    if (t.length < 3) return;
    var ov = document.createElement('div');
    ov.setAttribute('role', 'dialog'); ov.setAttribute('aria-label', '보여주기 카드');
    ov.style.cssText = 'position:fixed;inset:0;z-index:5000;background:#0F2A5C;color:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;gap:28px;padding:40px 32px;box-sizing:border-box;overflow:auto';
    var mk = function (txt, css) { var d = document.createElement('div'); d.textContent = txt; d.style.cssText = css; ov.appendChild(d); };
    mk(t[0].textContent, "font:700 clamp(44px,9vw,84px)/1.35 'Noto Serif JP',serif;overflow-wrap:anywhere");
    mk(t[1].textContent, 'font-size:clamp(30px,6vw,52px);font-weight:800;line-height:1.35;color:#CDBBFF');
    mk(t[2].textContent, 'font-size:clamp(24px,4.6vw,38px);font-weight:600;opacity:.92;padding-top:24px;border-top:1px solid rgba(255,255,255,.25);min-width:60%');
    var c = document.createElement('button'); c.type = 'button'; c.textContent = '닫기';
    c.style.cssText = 'margin-top:12px;height:64px;padding:0 48px;border-radius:999px;border:0;background:#fff;color:#0F2A5C;font-size:26px;font-weight:800;font-family:inherit;cursor:pointer';
    var close = function () { ov.remove(); try { if (document.fullscreenElement) document.exitFullscreen(); } catch (er) {} };
    c.onclick = close; ov.onclick = function (ev) { if (ev.target === ov) close(); };
    ov.appendChild(c); document.body.appendChild(ov); goFs();
  });
})();</script>
"""
FIT_JS = """<script>(function () {
  /* 오늘 탭: 지도 높이를 늘려서, 첫 화면이 통계 카드 줄(걸은 거리~걸은 시간)에서 딱 끝나게 맞춤 */
  var busy = false;
  function fit() {
    if (busy) return; busy = true;
    try {
      var lc = document.querySelector('.leaflet-container'); if (!lc) return;
      var box = lc.parentElement; if (!box || !/430px/.test(box.getAttribute('data-h0') || box.style.height || '')) { if (!box || !box.getAttribute('data-h0')) return; }
      var row = box.parentElement; while (row && getComputedStyle(row).display !== 'grid' && row.parentElement) row = row.parentElement;
      var stats = row; if (!stats) return;
      var scroller = row.parentElement, frame = document.querySelector('[data-screen-label="Fold8 unfolded"]');
      if (!scroller || !frame || scroller.scrollTop > 1) return;
      var bottom = stats.getBoundingClientRect().bottom, target = frame.getBoundingClientRect().bottom - 86;
      var cur = box.getBoundingClientRect().height, h = Math.max(430, Math.round(cur + (target - bottom)));
      if (Math.abs(h - cur) > 2) { box.style.height = h + 'px'; setTimeout(function () { window.dispatchEvent(new Event('resize')); }, 30); }
    } finally { busy = false; }
  }
  var t; var sched = function () { clearTimeout(t); t = setTimeout(fit, 120); };
  new MutationObserver(sched).observe(document.body, { childList: true, subtree: true });
  window.addEventListener('resize', sched); window.addEventListener('load', sched); setTimeout(fit, 1500);
})();</script>
"""
assert dc.count('</body>') == 1
dc = dc.replace('</body>', FS + SC_JS + FIT_JS + '</body>')
# 가짜 상태 표시줄(9:41·5G·배터리)과 카메라 점 제거
dc, k = re.subn(r'<div style="flex:none;height:32px;display:flex;align-items:center;justify-content:space-between;padding:0 24px 0 50px;font:600 12px system-ui;color:#20202A">\n<span>9:41</span>.*?</div>\n</div>\n<div style="position:absolute;top:10px;left:24px;width:12px;height:12px;border-radius:50%;background:#0b0d0f;z-index:1001"></div>\n', '', dc, count=1, flags=re.S)
assert k == 1
# 휴대폰에서는 디자인 폭(1000px) 그대로 화면에 맞춰 축소해서 보이게 함
assert dc.count('<meta name="viewport" content="width=device-width, initial-scale=1">') == 1
_TP='<sc-if value="{{ tabToday }}" hint-placeholder-val="{{ true }}">\n<div style="flex:1;min-height:0;overflow-y:auto;scrollbar-width:none;padding:4px 20px 20px 24px;'
assert dc.count(_TP)==1
dc = dc.replace(_TP, _TP.replace('padding:4px 20px 20px 24px;','padding:4px 20px 120px 24px;'))
for _o,_n in [("padding:12px 10px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:3px;text-align:center;position:relative;overflow:hidden\">\n<b style=\"font-size:20px;","padding:20px 8px 24px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:5px;text-align:center;position:relative;overflow:hidden\">\n<b style=\"font-size:32px;"),
 ("<span style=\"font-size:13px;font-weight:600;margin-left:3px\">{{ c.unit }}","<span style=\"font-size:19px;font-weight:600;margin-left:3px\">{{ c.unit }}"),
 ("<small style=\"font-size:12px;line-height:1.35;color:#85859A\">{{ c.label }} · {{ c.sub1 }} {{ c.sub2 }}","<small style=\"font-size:16px;line-height:1.3;color:#6B6B80\">{{ c.label }} · {{ c.sub1 }} {{ c.sub2 }}")]:
    assert dc.count(_o)==1,_o[:40]
    dc=dc.replace(_o,_n)
dc=dc.replace('padding:4px 20px 120px 24px;','padding:4px 20px 100px 24px;')
_G='grid-template-columns:minmax(0,1.3fr) repeat(3,minmax(0,1fr));gap:10px'
assert dc.count(_G)==1
dc=dc.replace(_G,'grid-template-columns:minmax(0,2.3fr) repeat(3,minmax(0,.8fr));gap:10px')
_A='color:#B7791F">ACHIEVEMENT · 스탬프</div><div style="font-size:16px;font-weight:700;color:#20202A;margin-top:3px">53역참 중 {{ stCount }}</div>'
assert dc.count(_A)==1
dc=dc.replace(_A,'color:#B7791F;white-space:nowrap">ACHIEVEMENT · 스탬프</div><div style="font-size:16px;font-weight:700;color:#20202A;margin-top:3px;white-space:nowrap">53역참 중 {{ stCount }}</div>')
# ---- 저장(유실 방지): 입력값을 이 기기에 자동 저장, 사진은 IndexedDB ----
PERSIST_KEYS = ['smode','exp','body','wToday','mg','mgSaved','note','memoSaved','dayNotes','dayNoteSaved','expSaved','theme','stage','lodgeOk','amenOn','fxRate','fxAmt','fxDir']
_P = [
 ("heroImg: (this.props.heroImg && !/^assets\\//.test(this.props.heroImg)) ? this.props.heroImg : 'https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?q=80&w=1600&auto=format&fit=crop',", "heroImg: 'assets/dayhero/' + view + '.jpg', heroPos: (Number(view)===31 ? '50% 86%' : '50% 40%'),"),
 ("amenOn: {}, pop: -1 };", "amenOn: {}, pop: -1, ...(() => { try { return JSON.parse(localStorage.getItem('tk-v15-data') || '{}'); } catch (e) { return {}; } })() };"),
 ("componentDidUpdate() { try {", "componentDidUpdate() { try { const _d = {}; " + repr(PERSIST_KEYS) + ".forEach(k => { if (this.state[k] !== undefined) _d[k] = this.state[k]; }); localStorage.setItem('tk-v15-data', JSON.stringify(_d)); } catch (e) {} try {"),
 ("dayNote: this.state.dayNote || '', onDayNote: e => this.setState({ dayNote: e.target.value, dayNoteSaved: false })", "dayNote: (this.state.dayNotes || {})[view] || '', onDayNote: e => { const v_ = e.target.value; this.setState(s_ => ({ dayNotes: Object.assign({}, s_.dayNotes || {}, { [view]: v_ }), dayNoteSaved: false })); }"),
]
for a_, b_ in _P:
    assert dc.count(a_) == 1, a_
    dc = dc.replace(a_, b_)
dc = dc.replace('<meta name="viewport" content="width=device-width, initial-scale=1">', '<meta name="viewport" content="width=1000, user-scalable=no"><style>[data-theme="dark"] [data-screen-label="Today hero"]{box-shadow:0 -14px 0 0 #171522,0 12px 0 0 #171522,0 16px 40px rgba(0,0,0,.4)!important}header{gap:8px!important;padding-left:16px!important;padding-right:12px!important}header>div:nth-child(3)>span:last-child{display:none}header>*{flex-shrink:1;min-width:0}nav[data-screen-label="Action rail"]>div{overflow-y:auto;scrollbar-width:none}@media (max-height:860px){nav[data-screen-label="Action rail"]>div{zoom:.74;padding-top:6px!important;padding-bottom:6px!important}}@media (max-height:700px){nav[data-screen-label="Action rail"]>div{zoom:.6}}:fullscreen header{padding-top:32px!important}@media (display-mode: fullscreen){header{padding-top:32px!important}}html,body{overflow-x:hidden;overscroll-behavior-x:none;max-width:100%}</style>' + open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'slotstore.html'),encoding='utf-8').read() + '<link rel="manifest" href="manifest.json"><link rel="apple-touch-icon" href="icon-180.png"><meta name="theme-color" content="#F7F7FB"><meta name="mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-status-bar-style" content="black-translucent"><meta name="apple-mobile-web-app-title" content="도카이도">')
_T='<span style="display:{{ s.tagDisplay }};height:20px;padding:0 8px;'
assert dc.count(_T)==1
dc=dc.replace(_T,'<span style="display:none;height:20px;padding:0 8px;')
_N='<b style="font-size:14px;font-weight:{{ s.weight }};color:{{ s.nameColor }};white-space:nowrap">{{ s.name }}</b>'
assert dc.count(_N)==1
dc=dc.replace(_N,'<b style="font-size:14px;font-weight:{{ s.weight }};color:{{ s.nameColor }};white-space:nowrap;flex:none">{{ s.name }}</b>')
_L='{{ c.label }} · {{ c.sub1 }} {{ c.sub2 }}</small>'
assert dc.count(_L)==1
dc=dc.replace(_L,'{{ c.sub1 }} {{ c.sub2 }}</small>')
_B='<b style="font-size:32px;font-weight:700;line-height:1.2;letter-spacing:-.025em;color:{{ c.color }}'
assert dc.count(_B)==1
dc=dc.replace(_B,'<small style="font-size:16px;line-height:1.3;font-weight:800;color:#3B3B4E">{{ c.label }}</small>'+_B)
for _o,_n,_c in [('style="height:46px;padding:0 16px;border:0;border-radius:13px;','style="height:68px;padding:0 20px;border:0;border-radius:16px;',1),
 ('style="width:46px;height:46px;border-radius:15px;border:1px solid rgba(255,255,255,.35)','style="width:62px;height:68px;border-radius:16px;border:1px solid rgba(255,255,255,.35)',2),
 ('style="height:46px;padding:0 14px;border-radius:15px;background:rgba(255,255,255,.94)','style="height:68px;padding:0 18px;border-radius:16px;background:rgba(255,255,255,.94)',1)]:
    assert dc.count(_o)==_c,_o
    dc=dc.replace(_o,_n)
_HB='background:#182B3D url({{ heroImg }}) center 42%/cover;box-shadow:0 -14px 0 0 #F7F7FB,0 12px 0 0 #F7F7FB,0 16px 40px rgba(15,42,74,.16)">'
assert dc.count(_HB)==1
dc=dc.replace(_HB,'background:#101A2B;box-shadow:0 -14px 0 0 #F7F7FB,0 12px 0 0 #F7F7FB,0 16px 40px rgba(15,42,74,.16)"><div style="position:absolute;top:0;bottom:0;right:0;width:80%;background:url({{ heroImg }}) {{ heroPos }}/cover no-repeat"></div><div style="position:absolute;inset:0;background:linear-gradient(90deg,#101A2B 0%,#101A2B 18%,rgba(16,26,43,.97) 24%,rgba(16,26,43,.9) 30%,rgba(16,26,43,.78) 36%,rgba(16,26,43,.62) 43%,rgba(16,26,43,.44) 50%,rgba(16,26,43,.27) 58%,rgba(16,26,43,.12) 67%,rgba(16,26,43,0) 78%)"></div>')
# ---- 글자 크기 가이드: 오늘(홈) 탭만 먼저 적용 ----
def _bump(n):
    n = float(n)
    return 16 if n <= 12 else 17 if n <= 13 else 18 if n <= 15 else 19 if n <= 17 else n
_i0 = dc.index('<sc-if value="{{ tabToday }}"'); _i1 = dc.index('</main>')
_sec = dc[_i0:_i1]
_sizes = set()
def _fs(m):
    n = float(m.group(1)); b = _bump(n)
    if b == n: return m.group(0)
    _sizes.add(n); return 'font-size:var(--f%g,%gpx)' % (n, n)
def _fh(m):
    n = float(m.group(2)); b = _bump(n)
    if b == n: return m.group(0)
    _sizes.add(n); return 'font:%s var(--f%g,%gpx)' % (m.group(1), n, n)
_sec = re.sub(r'font-size:(\d+(?:\.\d+)?)px', _fs, _sec)
_sec = re.sub(r'font:(\d+) (\d+(?:\.\d+)?)px', _fh, _sec)
_css = '@media (orientation:portrait){:root{' + ''.join('--f%g:%gpx;' % (n, _bump(n)) for n in sorted(_sizes)) + '}}'
dc = dc[:_i0] + _sec + dc[_i1:]
dc = dc.replace('<link rel="manifest"', '<style>' + _css + '</style><link rel="manifest"', 1)

# ---- 숙소: 후보 버튼 동작 + 아고다 검색(날짜·지역) ----
def _rep(a, b, cnt=1):
    global dc
    assert dc.count(a) == cnt, (a[:60], dc.count(a))
    dc = dc.replace(a, b)
_rep("lodgeLabel: isPast ? '숙박 완료' : lodgeOk && isToday ? '예약 확정' : '후보',\n      lodgeColor: lodgeOk && isToday ? '#fff' : '#555568', lodgeBg: lodgeOk && isToday ? ink : '#EDEDF4',\n      toggleLodge: () => { if (isToday) this.setState(s => ({ lodgeOk: !s.lodgeOk })); },",
 "lodgeLabel: isPast ? '숙박 완료' : ((lodgeOf(view).st === 'ok') || (lodgeOk && isToday)) ? '예약 확정' : '후보',\n      lodgeColor: ((lodgeOf(view).st === 'ok') || (lodgeOk && isToday)) ? '#fff' : '#3E1FA0', lodgeBg: ((lodgeOk && isToday) || lodgeOf(view).st === 'ok') ? ink : '#EDEDF4',\n      toggleLodge: e => { if (e && e.stopPropagation) e.stopPropagation(); if (isPast) return; const wasOk = (lodgeOf(view).st === 'ok') || (lodgeOk && isToday); setM(m => { m.lodge[view] = Object.assign({}, m.lodge[view], { st: wasOk ? 'cand' : 'ok' }); }); if (isToday) this.setState({ lodgeOk: false }); },")
_rep('<div onClick="{{ toggleLodge }}" style="background:#FFFFFF;border:1px solid #E8E7EF;border-radius:24px;box-shadow:0 4px 18px rgba(15,42,74,.025);padding:14px;cursor:pointer;display:flex;gap:14px;align-items:center"',
     '<div style="background:#FFFFFF;border:1px solid #E8E7EF;border-radius:24px;box-shadow:0 4px 18px rgba(15,42,74,.025);padding:14px;display:flex;gap:14px;align-items:center"')
_rep('<span style="font-size:var(--f12,12px);font-weight:700;color:{{ lodgeColor }};background:{{ lodgeBg }};border-radius:999px;padding:5px 10px;white-space:nowrap">{{ lodgeLabel }}</span>',
     '<button onClick="{{ toggleLodge }}" style="font-size:var(--f12,12px);font-weight:700;color:{{ lodgeColor }};background:{{ lodgeBg }};border:0;border-radius:999px;height:36px;padding:0 14px;white-space:nowrap;cursor:pointer;font-family:inherit">{{ lodgeLabel }}</button>')
_AGO = "'&checkIn=' + ymd(dt) + '&los=1&rooms=1&adults=1&locale=ko-kr&currencyCode=KRW'"
_rep("'&checkIn=' + ymd(dt) + '&checkOut=' + ymd(dt2) + '&rooms=1&adults=1'", _AGO)
_rep("'&checkIn=' + ymd(dt) + '&checkOut=' + ymd(new Date(dt.getTime() + 864e5)) + '&rooms=1&adults=1'", _AGO)


# ---- 오늘 통계 숫자 색상: 주요 색 4가지 ----
_rep("value: remain.toFixed(1), unit: 'km', color: '#20202A', sub1: '도착 예정', sub2: hhmm(eta), pct: Math.round(remain / dd.dist * 100), bar: ink, top: ink",
     "value: remain.toFixed(1), unit: 'km', color: '#2F6FE0', sub1: '도착 예정', sub2: hhmm(eta), pct: Math.round(remain / dd.dist * 100), bar: '#2F6FE0', top: '#2F6FE0'")
_rep("unit: '보', color: '#20202A', sub1: '목표 2만 보', sub2: Math.min(100, Math.round(steps / 200)) + '%', pct: Math.min(100, Math.round(steps / 200)), bar: ink, top: ink",
     "unit: '보', color: '#1E9E57', sub1: '목표 2만 보', sub2: Math.min(100, Math.round(steps / 200)) + '%', pct: Math.min(100, Math.round(steps / 200)), bar: '#1E9E57', top: '#1E9E57'")
_i=dc.index("unit: '', color: '#20202A', sub1: '남은 예상'"); _j=dc.index("bar: ink, top: ink", _i)
dc=dc[:_i]+dc[_i:_j].replace("color: '#20202A'","color: '#D9602F'")+"bar: '#D9602F', top: '#D9602F'"+dc[_j+len("bar: ink, top: ink"):]


# ---- 세로 확대 시 좁은 곳 보정 ----
_rep("font-size:var(--f11,11px);color:#85859A;font-family:'DM Sans','Noto Sans KR',sans-serif;font-variant-numeric:tabular-nums\">{{ d.date }}", "font-size:12px;color:#85859A;font-family:'DM Sans','Noto Sans KR',sans-serif;font-variant-numeric:tabular-nums;letter-spacing:-.04em\">{{ d.date }}")
_rep("<div style=\"font:700 var(--f14,14px) 'DM Sans',sans-serif;white-space:nowrap\">{{ d.hi }}°", "<div style=\"font:700 15px 'DM Sans',sans-serif;white-space:nowrap;letter-spacing:-.04em\">{{ d.hi }}°")
_rep("padding:0 14px;font:600 var(--f14,14px) 'Noto Sans KR',sans-serif;color:#20202A;outline:none;min-width:0;box-sizing:border-box;font-family:'DM Sans',sans-serif\"></input></label>\n", "padding:0 8px;font:600 14px 'Noto Sans KR',sans-serif;color:#20202A;outline:none;min-width:0;box-sizing:border-box;font-family:'DM Sans',sans-serif\"></input></label>\n", 0) if False else None

dc = re.sub(r'(type="time" value="\{\{ mg\.lodgeIn \}\}"[^>]*?)padding:0 14px;font:600 var\(--f14,14px\)', r'\1padding:0 6px;font:600 14px', dc)

# ---- 역참 도장: 한 줄 6개, 세로 직사각형 ----
_rep("grid-template-columns:repeat(auto-fill,minmax(104px,1fr));gap:10px;margin-top:14px", "grid-template-columns:repeat(6,minmax(0,1fr));gap:10px;margin-top:14px")
_rep("position:relative;aspect-ratio:1;border-radius:18px;border:1px solid {{ st.cardBorder }}", "position:relative;aspect-ratio:3/4;border-radius:18px;border:1px solid {{ st.cardBorder }}")
_rep('<div style="width:54px;height:54px;border-radius:50%;border:2.5px {{ st.borderStyle }} {{ st.ring }}', '<div style="width:66px;height:66px;flex:none;border-radius:50%;border:3px {{ st.borderStyle }} {{ st.ring }}')



# ---- 여행 정보: 세로에서는 확대(zoom) 없이 홈 규칙만 적용 ----
_rep("gap:12px;zoom:1.4", "gap:12px;zoom:var(--iz,1.4)")
dc = dc.replace('<link rel="manifest"', '<style>@media (orientation:portrait){:root{--iz:1}}</style><link rel="manifest"', 1)
# ---- 일본어: 보여주기 카드(파란 버튼 묶음) 삭제 ----
_m = re.search(r'<div style="grid-column:1/-1;background:linear-gradient\(135deg,#E8F1FF 0%,#F4F8FF 100%\);border:1px solid #CFE0FB[^\n]*\n', dc)
assert _m
dc = dc[:_m.start()] + dc[_m.end():]


# ---- 오늘: 통계 박스를 사진(히어로)과 지도 사이로 이동 ----
_sa = dc.index('<div style="flex:none;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px">\n<sc-for list="{{ stats }}"')
_se = dc.index('</sc-for>\n</div>\n', _sa) + len('</sc-for>\n</div>\n')
_stats = dc[_sa:_se]
dc = dc[:_sa] + dc[_se:]
_row = '<div style="flex:none;display:grid;grid-template-columns:minmax(0,1.5fr) minmax(280px,.9fr);gap:14px">\n<div style="background:#FFFFFF;border:1px solid #E8E7EF;border-radius:24px;box-shadow:0 4px 18px rgba(15,42,74,.025);padding:14px;display:flex;flex-direction:column;min-width:0">\n<div data-h0="430"'
assert dc.count(_row) == 1
dc = dc.replace(_row, _stats.replace('gap:12px">', 'gap:12px;margin-top:8px">', 1) + _row)


# ---- 여행 정보/일본어 상단 제목 삭제 ----
_rep('<sc-if value="{{ tabMore }}" hint-placeholder-val="{{ false }}">\n<div style="flex:none;padding:0 20px 12px 24px;display:flex;align-items:flex-end', '<sc-if value="{{ moreHead }}" hint-placeholder-val="{{ false }}">\n<div style="flex:none;padding:0 20px 12px 24px;display:flex;align-items:flex-end')
_rep("tabMore: tab === 7, tabLang:", "tabMore: tab === 7, moreHead: tab === 7 && ['stamp', 'prog'].indexOf(this.state.moreSub) >= 0, tabLang:")


# ---- 일본어: 참배 카테고리 삭제 ----
_n0 = dc.count('\n["참배",')
dc = re.sub(r'\n\["참배",[^\n]*', '', dc)
assert _n0 > 0 and '["참배"' not in dc


# ---- 일본어: 1980년생 47살 문장을 사교로 이동 ----
_rep('["숫자","私は1980年生まれの47歳です。"', '["사교","私は1980年生まれの47歳です。"')


# ---- 오늘 지나는 곳 사진: 외부(Unsplash) 대신 앱에 들어있는 사진으로 (로딩 실패 방지) ----
_pm = re.search(r"const PHOTOS = \[.*?\];", dc)
assert _pm
dc = dc[:_pm.start()] + "const PHOTOS = ['assets/hero/12.jpg', 'assets/hero/7.jpg', 'assets/hero/16.jpg', 'assets/hero/26.jpg'];" + dc[_pm.end():]
_rep("credit: 'Photo on Unsplash', creditHref: 'https://unsplash.com/photos/' + PHOTOS[i % PHOTOS.length].split('photo-')[1].split('?')[0],", "credit: '', creditHref: '',")


# ---- 전체 여정: 웨이포인트 간격 넓힘 ----
_rep("<div style=\"min-width:0;display:flex;gap:6px;align-items:center;padding:8px 0\"><b style=\"font-size:var(--f14,14px);white-space:nowrap\">{{ s.ko }}</b>", "<div style=\"min-width:0;display:flex;gap:8px;align-items:center;padding:20px 0\"><b style=\"font-size:var(--f14,14px);white-space:nowrap\">{{ s.ko }}</b>")


# ---- 한눈에 날짜별 기록: 사진은 올리는 곳이 아니라 '기록' 탭에 올린 사진을 불러와 보여주기만 ----
for _k in ('p1', 'p2', 'p3'):
    _rep('<image-slot id="{{ d.%s }}"' % _k, '<image-slot class="ro" id="{{ d.%s }}"' % _k)
dc = dc.replace('<link rel="manifest"', '<style>image-slot.ro{pointer-events:none}image-slot.ro::part(empty){display:none!important}</style><link rel="manifest"', 1)


dc = dc.replace('사진 칸에 끌어다 놓으면 저장돼요', '기록 탭에 올린 사진이 여기 나와요')


# ---- 한눈에 날짜별 기록: 카드를 누르면 그날의 사진·글이 팝업으로, 좌우로 다른 날 ----
_rep('<sc-for list="{{ diary }}" as="d" hint-placeholder-count="4"><div style="border:1px solid #E8E7EF;',
     '<sc-for list="{{ diary }}" as="d" hint-placeholder-count="4"><div data-diary="{{ d.n }}" data-date="{{ d.date }}" data-km="{{ d.km }}" data-path="{{ d.path }}" data-note="{{ d.note }}" data-tag="{{ d.tag }}" style="cursor:pointer;border:1px solid #E8E7EF;')
DIARY_JS = r"""<script>(function () {
  var ov = null, list = [], idx = 0, pic = 0;
  function esc(t) { return String(t == null ? '' : t).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function photosOf(card) {
    var out = []; card.querySelectorAll('image-slot').forEach(function (s) {
      var im = s.shadowRoot && s.shadowRoot.querySelector('img');
      if (im && im.src && im.style.display !== 'none') out.push(im.src);
    }); return out;
  }
  function collect() {
    return Array.prototype.map.call(document.querySelectorAll('[data-diary]'), function (c) {
      return { n: c.getAttribute('data-diary'), date: c.getAttribute('data-date'), km: c.getAttribute('data-km'), path: c.getAttribute('data-path'), note: c.getAttribute('data-note'), tag: c.getAttribute('data-tag'), pics: photosOf(c) };
    });
  }
  function close() { if (ov) { ov.remove(); ov = null; document.removeEventListener('keydown', onKey); } }
  function onKey(e) { if (e.key === 'Escape') close(); else if (e.key === 'ArrowLeft') go(1); else if (e.key === 'ArrowRight') go(-1); }
  function go(d) { var k = idx + d; if (k < 0 || k >= list.length) return; idx = k; pic = 0; render(); }
  function render() {
    var it = list[idx], has = it.pics.length > 0;
    var cbtn = '<button data-close="1" aria-label="닫기" style="width:68px;height:68px;border-radius:50%;border:0;background:linear-gradient(135deg,#673DE6 0%,#8B5CF6 100%);color:#fff;font-size:26px;font-weight:700;cursor:pointer;display:flex;align-items:center;justify-content:center;box-shadow:0 8px 20px rgba(103,61,230,.4);flex:none">✕</button>';
    var nb = function (dir, dis, label) { return '<button data-go="' + dir + '" style="height:68px;min-width:104px;padding:0 18px;border-radius:20px;border:1.5px solid #E5DBFF;background:#F1ECFF;color:#3E1FA0;font:700 20px \'Noto Sans KR\',sans-serif;cursor:pointer;opacity:' + (dis ? .3 : 1) + ';white-space:nowrap">' + label + '</button>'; };
    var ph = 'border-radius:16px;background:#F1F1F7;display:grid;place-items:center;color:#85859A;font-size:19px;text-align:center;line-height:1.5';
    var cur = Math.min(pic, Math.max(0, it.pics.length - 1));
    var tl = [0, 1, 2];
    var thumbs = '<div style="display:flex;gap:10px;margin-top:10px">' + tl.map(function (i) { var u = it.pics[i]; return u ? '<img data-pic="' + i + '" src="' + u + '" style="flex:1;min-width:0;height:min(17dvh,200px);object-fit:cover;border-radius:16px;cursor:pointer;border:3px solid ' + (i === cur ? '#673DE6' : 'transparent') + ';box-sizing:border-box">' : '<div style="flex:1;min-width:0;height:min(17dvh,200px);' + ph + '">사진 없음</div>'; }).join('') + '</div>';
    ov.innerHTML = '<div style="position:relative;width:min(900px,calc(100% - 48px));max-height:calc(100% - 40px);overflow:auto;background:#fff;border-radius:28px;padding:22px;box-shadow:0 30px 80px rgba(0,0,0,.45)">' +
      '<div style="display:flex;align-items:center;gap:12px"><b style="font:800 24px \'DM Sans\',sans-serif;letter-spacing:.08em;color:#673DE6">DAY ' + esc(it.n) + '</b><span style="font-size:22px;color:#555568">' + esc(it.date) + ' · ' + esc(it.km) + 'km</span><span style="flex:1"></span><span style="font-size:19px;font-weight:700;padding:4px 14px;border-radius:999px;background:#E4F8EC;color:#15803D">' + esc(it.tag) + '</span></div>' +
      '<div style="font-size:30px;font-weight:800;margin:10px 0">' + esc(it.path) + '</div>' +
      (has ? '<img src="' + it.pics[Math.min(pic, it.pics.length - 1)] + '" style="width:min(100%,46dvh);aspect-ratio:4/3;object-fit:cover;border-radius:20px;display:block;margin:0 auto">'
           : '<div style="width:min(100%,46dvh);aspect-ratio:4/3;margin:0 auto;border-radius:20px;background:#F1F1F7;display:grid;place-items:center;color:#85859A;font-size:21px;text-align:center;line-height:1.5">이 날은 올린 사진이 없어요<br>기록 탭에서 올리면 여기 나와요</div>') + thumbs +
      '<div style="font-size:24px;font-weight:500;line-height:1.5;margin-top:14px;padding:16px 20px;min-height:3.4em;box-sizing:border-box;display:flex;align-items:center;justify-content:center;text-align:center;border-radius:16px;background:linear-gradient(135deg,#EEE9FF 0%,#F8F5FF 100%)">“' + esc(it.note) + '”</div>' +
      '<div style="display:flex;align-items:center;justify-content:space-between;margin-top:16px;padding-top:12px;border-top:1px solid #F1F5F9">' + cbtn +
      '<div style="display:flex;align-items:center;gap:10px">' + nb(1, idx >= list.length - 1, '‹ 이전 날') + '<span style="font:700 20px \'DM Sans\',sans-serif;color:#555568;min-width:64px;text-align:center">' + (list.length - idx) + ' / ' + list.length + '</span>' + nb(-1, idx <= 0, '다음 날 ›') + '</div>' + cbtn + '</div></div>';
  }
  function open(card) {
    list = collect(); idx = Math.max(0, list.findIndex(function (x) { return x.n === card.getAttribute('data-diary'); })); pic = 0;
    ov = document.createElement('div');
    ov.style.cssText = "font-family:'DM Sans','Noto Sans KR',sans-serif;position:fixed;inset:0;z-index:3000;display:flex;align-items:center;justify-content:center;background:rgba(15,23,42,.55);-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px)";
    ov.addEventListener('click', function (e) {
      var t = e.target; if (t === ov || (t.closest && t.closest('[data-close]'))) return close();
      var g = t.closest && t.closest('[data-go]'); if (g) return go(+g.getAttribute('data-go'));
      var pc = t.closest && t.closest('[data-pic]'); if (pc) { pic = +pc.getAttribute('data-pic'); render(); }
    });
    var x0 = null; ov.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; }, { passive: true });
    ov.addEventListener('touchend', function (e) { if (x0 == null) return; var dx = e.changedTouches[0].clientX - x0; x0 = null; if (Math.abs(dx) > 60) go(dx < 0 ? -1 : 1); }, { passive: true });
    document.body.appendChild(ov); document.addEventListener('keydown', onKey); render();
  }
  document.addEventListener('click', function (e) { if (ov) return; var c = e.target.closest && e.target.closest('[data-diary]'); if (c) open(c); });
})();</script>
"""
dc = dc.replace('</body>', DIARY_JS + '</body>')


# ---- 오늘 지나는 곳: 12일차뿐 아니라 모든 날에 (일정표의 명소 목록 사용) ----
_px = {}
for _n in range(1, 32):
    _seen = set(); _lst = []
    for _t in list(PH.get(_n, {}).get('s', [])) + list(XT.get(_n, {}).get('s', [])):
        if _t[0] in _seen: continue
        _seen.add(_t[0]); _lst.append([_t[0], _t[1], _t[2] if len(_t) > 2 else ''])
    if _lst: _px[_n] = _lst
_rep("    places: d === 12 ? PLACES12 : []\n",
"""    places: d === 12 ? PLACES12 : (PLACESX[d] || []).map((sp, i, arr) => {
      const t = (i + 1) / (arr.length + 1), km = +(dist * t).toFixed(1);
      let ll = rel[rel.length - 1].ll;
      for (let k = 1; k < rel.length; k++) { if (km <= rel[k].rel || k === rel.length - 1) { const a0 = rel[k - 1], b0 = rel[k], f = b0.rel === a0.rel ? 0 : Math.min(1, Math.max(0, (km - a0.rel) / (b0.rel - a0.rel))); ll = [a0.ll[0] + (b0.ll[0] - a0.ll[0]) * f, a0.ll[1] + (b0.ll[1] - a0.ll[1]) * f]; break; } }
      if (rel.length === 1) ll = rel[0].ll;
      return { name: sp[0], km, ll, desc: sp[2] || sp[1], q: sp[1], long: sp[2] ? sp[2] + '. 오늘 코스 근처에서 들러볼 만한 곳이에요.' : sp[0] + '(' + sp[1] + ') — 오늘 코스 근처에서 들러볼 만한 곳이에요. 위치는 대략적이니 구글 지도로 정확한 길을 확인하세요.' };
    })
""")
_rep("const PLACES12 = [", "const PLACESX = " + json.dumps(_px, ensure_ascii=False) + ";\nconst PLACES12 = [")


# ---- 기록: 수면/체중 카드 위아래 간격 (고정 높이 때문에 글자가 겹치던 것) ----
_rep("gap:12px;height:62px\"><div style=\"min-width:0\">", "gap:12px;min-height:62px;padding-bottom:6px\"><div style=\"min-width:0\">", 2)
_rep("margin-top:10px;height:36px;flex-wrap:nowrap", "margin-top:14px;min-height:40px;flex-wrap:nowrap", 2)


# ---- 장소 팝업 크게 ----
_pa = dc.index('<div data-screen-label="Spot popup"'); _pb = dc.index('<sc-if value="{{ creaseOn }}"')
_pp = dc[_pa:_pb]
for _o, _n in [
  ('justify-content:flex-end;padding:60px 120px 40px 40px', 'justify-content:flex-end;padding:30px 96px 30px 24px'),
  ('width:440px;max-height:100%', 'width:min(800px,100%);max-height:100%'),
  ('border-radius:28px;padding:20px;box-shadow', 'border-radius:32px;padding:26px;box-shadow'),
  ('position:relative;height:200px;border-radius:20px', 'position:relative;height:min(40dvh,420px);border-radius:24px'),
  ('padding:6px 12px;border-radius:999px;font-size:12px;font-weight:700', 'padding:8px 16px;border-radius:999px;font-size:18px;font-weight:700'),
  ('margin:16px 0 12px;text-align:center', 'margin:22px 0 16px;text-align:center'),
  ('font-size:24px;font-weight:800;letter-spacing:-.02em;color:#0F172A', 'font-size:36px;font-weight:800;letter-spacing:-.02em;color:#0F172A'),
  ("font:500 13px 'Noto Serif JP',serif;color:#64748B;margin-top:4px", "font:500 19px 'Noto Serif JP',serif;color:#64748B;margin-top:6px"),
  ('gap:8px">\n<sc-for list="{{ pop.facts }}"', 'gap:12px">\n<sc-for list="{{ pop.facts }}"'),
  ('border-radius:14px;padding:10px 8px;display:flex', 'border-radius:18px;padding:16px 8px;display:flex'),
  ('<small style="font-size:12px;color:#64748B;font-weight:500">', '<small style="font-size:17px;color:#64748B;font-weight:500">'),
  ("font:800 16px 'DM Sans','Noto Sans KR',sans-serif;letter-spacing:-.02em;color:#0F172A;white-space:nowrap", "font:800 25px 'DM Sans','Noto Sans KR',sans-serif;letter-spacing:-.02em;color:#0F172A;white-space:nowrap"),
  ('font-size:13px;color:#475569;line-height:1.7;margin:12px 0', 'font-size:20px;color:#475569;line-height:1.7;margin:18px 0'),
  ('position:relative;height:150px;border-radius:16px', 'position:relative;height:260px;border-radius:20px'),
  ('padding:5px 10px;border-radius:999px;background:rgba(255,255,255,.94);font-size:12px', 'padding:7px 14px;border-radius:999px;background:rgba(255,255,255,.94);font-size:16px'),
  ('margin-top:14px;padding-top:10px;border-top', 'margin-top:18px;padding-top:12px;border-top'),
  ('gap:6px;font-size:13px;font-weight:700;color:#5B32D6;padding:12px 4px', 'gap:6px;font-size:20px;font-weight:700;color:#5B32D6;padding:14px 6px'),
  ('width:48px;height:48px;border-radius:50%;border:0;background:linear-gradient(135deg,#673DE6 0%,#8B5CF6 100%);color:#fff;font-size:18px', 'width:68px;height:68px;border-radius:50%;border:0;background:linear-gradient(135deg,#673DE6 0%,#8B5CF6 100%);color:#fff;font-size:26px'),
]:
    assert _pp.count(_o) == 1, _o
    _pp = _pp.replace(_o, _n)
dc = dc[:_pa] + _pp + dc[_pb:]


# ---- 일정 관리: 도착지 버튼에서 거리/안내가 겹치던 것 ----
_rep('<span style="display:flex;align-items:baseline;gap:6px"><span style="font-size:var(--f15,15px);font-weight:700;color:{{ e.kmC }}', '<span style="display:flex;align-items:baseline;gap:2px 6px;flex-wrap:wrap"><span style="font-size:var(--f15,15px);font-weight:700;color:{{ e.kmC }}')
_rep('background:rgba(15,23,42,.42);backdrop-filter:blur(2.5px);-webkit-backdrop-filter:blur(2.5px)', 'background:rgba(15,23,42,.30);backdrop-filter:blur(18px);-webkit-backdrop-filter:blur(18px)')


# ---- 장소 팝업: 하단에 이전/다음 버튼 ----
_nb = lambda lab, fn, op: '<button onClick="{{ %s }}" style="height:68px;min-width:104px;padding:0 18px;border-radius:20px;border:1.5px solid #E5DBFF;background:#F1ECFF;color:#3E1FA0;font:700 20px \'Noto Sans KR\',sans-serif;cursor:pointer;opacity:{{ %s }};white-space:nowrap">%s</button>' % (fn, op, lab)
_rep('구글 지도로 길찾기 ›</a>\n<button onClick="{{ closePop }}"',
     '구글 지도로 길찾기 ›</a>\n<div style="display:flex;align-items:center;gap:10px">' + _nb('‹ 이전', 'popPrev', 'popPrevOp') + '<span style="font:700 20px \'DM Sans\',sans-serif;color:#555568;min-width:64px;text-align:center">{{ popPos }}</span>' + _nb('다음 ›', 'popNext', 'popNextOp') + '</div>\n<button onClick="{{ closePop }}"')
_rep("closePop: () => this.setState({ pop: -1 }),", "closePop: () => this.setState({ pop: -1 }), popPrev: () => this.setState(s => ({ pop: Math.max(0, s.pop - 1) })), popNext: () => this.setState(s => ({ pop: Math.min(dd.places.length - 1, s.pop + 1) })), popPrevOp: pi > 0 ? 1 : .3, popNextOp: pi < dd.places.length - 1 ? 1 : .3, popPos: (pi + 1) + ' / ' + dd.places.length,")
_rep("this.popMap = pm; this.popR = L.svg({ padding: 0.5 }).addTo(pm); this.drawPop();", "this._popN = this._pop && this._pop.n; this.popMap = pm; this.popR = L.svg({ padding: 0.5 }).addTo(pm); this.drawPop();")
_rep("} else if (!pel && this.popMap) {", "} else if (pel && this.popMap && this._pop && this._popN !== this._pop.n) { this._popN = this._pop.n; this.drawPop(); } else if (!pel && this.popMap) {")


# ---- 지도: 하단 '구글 지도 길찾기' 글자 삭제 → 지도 버튼 열에 구글 지도 버튼 추가, 지도는 그만큼 커짐 ----
_rep('\n<a href="{{ gmapsDir }}" target="_blank" rel="noopener" style="font-weight:700;white-space:nowrap">구글 지도 길찾기 ›</a>', '')
_gb = '<a href="{{ gmapsDir }}" target="_blank" rel="noopener" title="구글 지도로 길찾기" style="width:46px;height:46px;border:1px solid #DDE5EC;border-radius:15px;background:#fff;box-shadow:0 4px 14px rgba(27,51,69,.13);cursor:pointer;display:flex;align-items:center;justify-content:center;text-decoration:none"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#2F6FE0" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s-7-6.2-7-11a7 7 0 0 1 14 0c0 4.8-7 11-7 11z"></path><circle cx="12" cy="10" r="2.6"></circle></svg></a>\n'
_rep('<div style="position:absolute;right:12px;bottom:12px;z-index:500;display:grid;gap:9px">\n<button onClick="{{ lodgeFly }}"', '<div style="position:absolute;right:12px;bottom:12px;z-index:500;display:grid;gap:9px">\n' + _gb + '<button onClick="{{ lodgeFly }}"')


# ---- 체중 그래프: 값이 범위(72~80)를 벗어나도 그래프 안에 들어오게 눈금 자동 조절 ----
_rep("    const wPts = wv.map((v, i) => ({ x: sx(i, wv.length, 52, 330), y: sc(v, 72, 80, 10, 146),",
     "    const wLo = Math.min(72, Math.floor((Math.min(...wv, 77) - 1) / 2) * 2), wHi = Math.max(80, Math.ceil((Math.max(...wv, 77) + 1) / 2) * 2), wTicks = []; for (let t = wLo; t <= wHi; t += 2) wTicks.push(t);\n    const wPts = wv.map((v, i) => ({ x: sx(i, wv.length, 52, 330), y: sc(v, wLo, wHi, 10, 146),")
_rep("const wBase = 77, wBY = sc(wBase, 72, 80, 10, 146);", "const wBase = 77, wBY = sc(wBase, wLo, wHi, 10, 146);")
_rep("grid: grid([72, 74, 76, 78, 80], 72, 80, 10, 146, v => v + 'kg'), baseY: wBY", "grid: grid(wTicks, wLo, wHi, 10, 146, v => v + 'kg'), baseY: wBY")


# ---- 수면 그래프: 기준 8시간, 그래프 세로로 더 길게 (체중 그래프도 같은 높이) ----
dc = dc.replace('viewBox="0 0 354 170"', 'viewBox="0 0 354 250"')
assert dc.count('y="165" text-anchor="middle"') == 2
dc = dc.replace('y="165" text-anchor="middle"', 'y="245" text-anchor="middle"')
dc = dc.replace('10, 146', '10, 226')
_rep("rline(sleep, 5, 9, [5, 6, 7, 8, 9], v => v + 'h'", "rline(sleep, 4, 10, [4, 6, 8, 10], v => v + 'h'")
_rep("sc(7, 5, 9, 10, 226)", "sc(8, 4, 10, 10, 226)")
_rep("y = sc(v, 5, 9, 10, 226)", "y = sc(v, 4, 10, 10, 226)")
_rep("c: v >= 7 ? '#7951E8' : '#F2C66A'", "c: v >= 8 ? '#7951E8' : '#F2C66A'")
_rep("sleep.filter(v => v >= 7).length", "sleep.filter(v => v >= 8).length")
_rep("'기준 7시간 대비'", "'기준 8시간 대비'")
dc = dc.replace('>기준 7시간 대비 · Galaxy Watch9<', '>기준 8시간 대비 · Galaxy Watch9<')
dc = dc.replace('>기준 7h<', '>기준 8h<').replace('>7h 이상 {{ c.over }}일<', '>8h 이상 {{ c.over }}일<').replace('>7h 미만 {{ c.under }}일<', '>8h 미만 {{ c.under }}일<')


# ---- 여행 정보: 지금 날씨 / 이번 주 날씨를 두 줄로 ----
_rep('<div style="flex:none;display:grid;grid-template-columns:minmax(0,.9fr) minmax(0,1.1fr);gap:12px">\n<div data-screen-label="Weather now"', '<div style="flex:none;display:grid;grid-template-columns:minmax(0,1fr);gap:12px">\n<div data-screen-label="Weather now"')


# ---- 기록 배지: 정사각형 + 설명 요약(잘리지 않게) ----
for _o, _n in [
 ("'이제 감이 좀 잡히는데?'", "'감이 잡히기 시작'"),
 ("['하프 마라톤의 날', '하루에 20km 이상을 걸은 날'", "['하프 마라톤', '하루 20km 이상'"),
 ("'비가 오나 눈이 오나 7일간 멈추지 않은 발걸음'", "'7일 연속 걷기'"),
 ("'휴식일 제외 연속 10일, 습관이 된 걷기'", "'10일 연속 걷기'"),
 ("'바다를 옆에 끼고 걸은 날 (누마즈~유이 해안길 완료)'", "'누마즈~유이 해안길'"),
 ("'하코네·오키쓰·아리마 온천에서 물집 잡힌 발을 녹인 날'", "'온천에서 발 풀기'"),
 ("'길 위에서 맞은 1월 1일'", "'길 위의 1월 1일'"),
 ("'마지막 큰 고개를 넘은 날'", "'마지막 큰 고개'"),
 ("'시크릿 배지 · 달성하면 열려요'", "'달성하면 열려요'"),
]:
    assert dc.count(_o) >= 1, _o
    dc = dc.replace(_o, _n)
_rep('<div title="{{ g.s }}" style="display:flex;flex-direction:column;align-items:center;justify-content:center;gap:3px;text-align:center;border-radius:14px;padding:10px 6px;', '<div title="{{ g.s }}" style="aspect-ratio:1;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:5px;text-align:center;border-radius:16px;padding:8px 6px;')
_rep('<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="{{ g.ic }}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="{{ g.icon }}"></path></svg><div style="font-size:var(--f13,13px);font-weight:700;line-height:1.25;color:{{ g.c }};white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:100%">{{ g.t }}</div><div style="font-size:var(--f11,11px);line-height:1.3;color:{{ g.sc }};white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:100%">{{ g.s }}</div>',
     '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="{{ g.ic }}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="{{ g.icon }}"></path></svg><div style="font-size:var(--f13,13px);font-weight:800;line-height:1.25;color:{{ g.c }};word-break:keep-all;max-width:100%">{{ g.t }}</div><div style="font-size:var(--f12,12px);line-height:1.3;color:{{ g.sc }};word-break:keep-all;max-width:100%">{{ g.s }}</div>')


# ---- 이번 주 날씨: 기온 크게 ----
_rep("<div style=\"font:700 15px 'DM Sans',sans-serif;white-space:nowrap;letter-spacing:-.04em\">{{ d.hi }}°<span style=\"color:#85859A;font-weight:500\"> {{ d.lo }}°</span>", "<div style=\"font:800 25px 'DM Sans',sans-serif;white-space:nowrap;letter-spacing:-.03em\">{{ d.hi }}°<span style=\"color:#85859A;font-weight:500;font-size:19px\"> {{ d.lo }}°</span>")


# ---- 날씨: Open-Meteo(무료·키 없음)로 내 위치 실시간 날씨 자동 불러오기 ----
_rep("componentDidMount() { this.loadFx();", "componentDidMount() { this.loadFx(); this.loadWx();")
_rep("  loadFx() {\n", """  loadWx() {
    try { const c = JSON.parse(localStorage.getItem('tk-wx') || 'null'); if (c && Date.now() - c.ts < 6 * 36e5 && !this.state.wlive) this.setState({ wlive: c }); } catch (e) {}
    const apply = (lat, lon, src) => {
      const u = 'https://api.open-meteo.com/v1/forecast?latitude=' + lat.toFixed(3) + '&longitude=' + lon.toFixed(3) + '&current=temperature_2m,weather_code,is_day&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max,sunrise,sunset&timezone=auto&forecast_days=7';
      fetch(u).then(r => r.json()).then(j => { if (!j || !j.current || !j.daily || !j.daily.time) throw 0; const w = { ts: Date.now(), src, now: j.current.temperature_2m, code: j.current.weather_code, d: j.daily }; this.setState({ wlive: w }); try { localStorage.setItem('tk-wx', JSON.stringify(w)); } catch (e) {} }).catch(() => {});
    };
    const fb = () => { const ll = this._wxLL || [34.97, 138.38]; apply(ll[0], ll[1], 'trip'); };
    try { if (navigator.geolocation) navigator.geolocation.getCurrentPosition(p => apply(p.coords.latitude, p.coords.longitude, 'gps'), fb, { timeout: 6000, maximumAge: 600000 }); else fb(); } catch (e) { fb(); }
    clearTimeout(this._wxT); this._wxT = setTimeout(() => this.loadWx(), 30 * 6e4);
  }
  loadFx() {
""")
_rep("    const wx = view === 12 ?", "    let wx = view === 12 ?")
_rep("    const wxPlace = nm(tdd.stops[Math.max(0, Math.min(tst, tn) - (tst > 0 ? 1 : 0))]);", "    const wxPlace = nm(tdd.stops[Math.max(0, Math.min(tst, tn) - (tst > 0 ? 1 : 0))]);\n    this._wxLL = tdd.stops[Math.max(0, Math.min(tst, tn) - (tst > 0 ? 1 : 0))].ll;")
_rep("const wxw = { place: wxPlace, now: 9,", "const wxw = { badge: '예시 데이터', place: wxPlace, now: 9,")
_rep("{ label: '일몰', t: fmtT(ss), color: accent }] };", """{ label: '일몰', t: fmtT(ss), color: accent }] };
    const WL = this.state.wlive;
    if (WL && WL.d && WL.d.time && WL.d.time.length) {
      const wcat = c => c <= 1 ? 0 : c <= 48 ? 1 : 2;
      const wtxt = c => c === 0 ? '맑음' : c <= 2 ? '구름 조금' : c === 3 ? '흐림' : c <= 48 ? '안개' : c <= 57 ? '이슬비' : c <= 67 ? '비' : c <= 77 ? '눈' : c <= 82 ? '소나기' : c <= 86 ? '눈보라' : '뇌우';
      wxw.days = WL.d.time.map((t, i) => { const [yy, mm, d2] = t.split('-').map(Number), dtx = new Date(yy, mm - 1, d2), kk = WXK[wcat(WL.d.weather_code[i])]; return { name: i === 0 ? '오늘' : i === 1 ? '내일' : '일월화수목금토'[dtx.getDay()], date: mm + '/' + d2, icon: kk[1], ic: kk[2], hi: Math.round(WL.d.temperature_2m_max[i]), lo: Math.round(WL.d.temperature_2m_min[i]), rain: Math.round(WL.d.precipitation_probability_max[i] || 0), bg: i === 0 ? '#F1ECFF' : '#F1F1F7', c: i === 0 ? '#4E27C5' : '#20202A' }; });
      wxw.now = Math.round(WL.now); wxw.cond = wtxt(WL.code); wxw.place = WL.src === 'gps' ? '내 위치' : wxPlace;
      const sr0 = (WL.d.sunrise[0] || '').slice(11, 16), ss0 = (WL.d.sunset[0] || '').slice(11, 16);
      wxw.sun = [{ label: '일출', t: sr0, color: '#20202A' }, { label: '일몰', t: ss0, color: accent }];
      wxw.badge = '실시간 · ' + (WL.src === 'gps' ? '내 위치' : '코스 기준');
      wx = { t: Math.round(WL.d.temperature_2m_min[0]) + '° / ' + Math.round(WL.d.temperature_2m_max[0]) + '°', s: wtxt(WL.code) + ' · 일몰 ' + ss0, sun: WL.code <= 2 };
    }""")
_rep("opacity:.85\">WEATHER · 지금</span><span style=\"height:24px;padding:0 10px;border-radius:999px;background:rgba(255,255,255,.16);border:1px solid rgba(255,255,255,.3);backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);font-size:var(--f12,12px);font-weight:700;display:flex;align-items:center;white-space:nowrap;flex:none\">예시 데이터</span>", "opacity:.85\">WEATHER · 지금</span><span style=\"height:24px;padding:0 10px;border-radius:999px;background:rgba(255,255,255,.16);border:1px solid rgba(255,255,255,.3);backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);font-size:var(--f12,12px);font-weight:700;display:flex;align-items:center;white-space:nowrap;flex:none\">{{ wxw.badge }}</span>")


_cb = '<button onClick="{{ closePop }}" aria-label="팝업 닫기" style="width:68px;height:68px;border-radius:50%;border:0;background:linear-gradient(135deg,#673DE6 0%,#8B5CF6 100%);color:#fff;font-size:26px;font-weight:700;cursor:pointer;display:flex;align-items:center;justify-content:center;box-shadow:0 8px 20px rgba(103,61,230,.4);flex:none">✕</button>'
_rep('<a href="{{ pop.dir }}" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;gap:6px;font-size:20px;font-weight:700;color:#5B32D6;padding:14px 6px">구글 지도로 길찾기 ›</a>\n', _cb + '\n')


_rep("<b style=\"font-size:32px;font-weight:700;line-height:1.2;letter-spacing:-.025em;color:{{ c.color }}", "<b style=\"font-size:26px;font-weight:700;line-height:1.2;letter-spacing:-.025em;color:{{ c.color }}")
_rep("{{ c.value }}<span style=\"font-size:19px;font-weight:600;margin-left:3px\">{{ c.unit }}", "{{ c.value }}<span style=\"font-size:16px;font-weight:600;margin-left:3px\">{{ c.unit }}")

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
