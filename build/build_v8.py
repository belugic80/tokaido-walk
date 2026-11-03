# 새 디자인(클로드 디자인 v8: design/v8/Tokaido Walk App.dc.html)을 기존 데이터·기능에 연결해 내보냄.
#  - 화면(마크업)은 디자인 파일 그대로. 시안용 요소(가짜 상태바·홈 바·가짜 지도)만 실제 것으로 교체.
#  - 데이터·기능은 기존 앱(build.py 결과 index.html)의 로직을 그대로 가져와 씀:
#    일정(엑셀)·위치/GPS·건강 동기화·날씨·저장/클라우드 백업·당겨서 새로고침 등.
#  - 사용: python3 build/build.py data/schedule.xlsx _  →  python3 build/build_v8.py [출력폴더(기본 new)]
import os, sys, re, shutil, json
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, 'design', 'v8', 'Tokaido Walk App.dc.html')
OUT = os.path.join(ROOT, sys.argv[1] if len(sys.argv) > 1 else 'new')
dc = open(SRC, encoding='utf-8').read()
old = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()


def rep(a, b, cnt=1, src=None):
    global dc
    s = dc if src is None else src
    assert s.count(a) == cnt, (s.count(a), a[:120])
    s = s.replace(a, b)
    if src is None:
        dc = s
    return s


# ───────────────────────── 1. 화면 틀 ─────────────────────────
rep("box-shadow:0 30px 60px rgba(40,40,100,.18),0 0 0 10px #1B1C22", "")
rep("w:'760px', h:'860px', r:'28px'", "w:'100%', h:'100lvh', r:'0'")
rep("w:'390px', h:'844px', r:'44px'", "w:'100%', h:'100lvh', r:'0'")
WIDE = "(typeof window !== 'undefined' && window.innerWidth >= 640)"
rep("const F = !!this.props.fold || this.props.go==='flex'", "const F = " + WIDE)
rep("mapAR:'auto', mapHt:'630px',", "mapAR:'auto', mapHt:'calc(100lvh - env(safe-area-inset-top) - env(safe-area-inset-bottom) - 186px)',")
rep("F ? { areas:'\"a d\" \"b e\" \"c f\"',", "F ? { areas: isT ? '\"a d\" \"b e\" \"c f\"' : '\"a d\" \"a e\" \"c f\"',")
rep("this.props.fold", WIDE, cnt=3)

# 시안용 가짜 상태바(14:20·신호·배터리) 제거 → 실제 폰 상태바 사용, 위쪽은 안전 영역만큼 띄움
i = dc.index('<b style="font-size:15px">14:20</b>')
a0 = dc.rindex('<div style="position:absolute;left:0;right:0;top:0;height:50px;', 0, i)
depth, k = 0, a0
while True:
    o, c = dc.find('<div', k), dc.find('</div>', k)
    if o != -1 and o < c:
        depth += 1; k = o + 4
    else:
        depth -= 1; k = c + 6
        if depth == 0:
            break
dc = dc[:a0] + dc[k:]
rep('padding:58px 20px 14px', 'padding:calc(env(safe-area-inset-top) + 18px) 20px 14px')
rep('height:98px;padding-top:52px;z-index:8;', 'height:calc(env(safe-area-inset-top) + 52px);padding-top:env(safe-area-inset-top);z-index:8;')

# 시안용 홈 바(화면 아래 검은 줄) 제거, 하단 메뉴는 기기 안전 영역 위로
rep('<i style="position:absolute;left:50%;bottom:8px;transform:translateX(-50%);width:134px;height:5px;border-radius:3px;background:#18324F;opacity:.85;z-index:11"></i>', '')
rep('width:{{ fr.navW }};bottom:22px;z-index:10;', 'width:{{ fr.navW }};bottom:calc(env(safe-area-inset-bottom) + 14px);z-index:10;')
# 펼친 화면(2열)에서 좌우 카드 높이 맞춤: 두 열을 같은 높이로 늘리고, 각 열의 마지막 카드가 남는 높이를 채움
rep('<div style="display:grid;grid-template-columns:{{ fr.cols }};gap:12px;padding:0 16px;align-items:stretch;min-height:{{ fr.subMin }}"', '<div class="eq2" style="display:grid;grid-template-columns:{{ fr.cols }};gap:12px;padding:0 16px;align-items:stretch;min-height:{{ fr.subMin }}"', cnt=7)
rep('<div style="display:grid;grid-template-columns:{{ fr.cols }};grid-template-areas:{{ fr.areas }};gap:12px;padding:0 16px;align-items:stretch"', '<div class="eq2" style="display:grid;grid-template-columns:{{ fr.cols }};grid-template-areas:{{ fr.areas }};gap:12px;padding:0 16px;align-items:stretch"')
# 일본어: 왼쪽 문장 목록이 길어도 오른쪽 크게 보기 칸은 화면에 붙어 따라옴
rep('<div style="display:grid;grid-template-columns:{{ fr.cols }};gap:12px;padding:0 16px;align-items:start"', '<div class="jp2" style="display:grid;grid-template-columns:{{ fr.cols }};gap:12px;padding:0 16px;align-items:start"')
# 일본어 크게 보기: 일본어 문장은 글자 단위로 줄바꿈되게 (keep-all 때문에 칸 밖으로 넘치던 것)
rep('<b style="font-size:60px;font-weight:800;line-height:1.25;letter-spacing:-.01em;color:#18324F;text-wrap:balance">{{ jpSel.jp }}', '<b style="font-size:60px;font-weight:800;line-height:1.25;letter-spacing:-.01em;color:#18324F;text-wrap:balance;word-break:normal;overflow-wrap:anywhere;max-width:100%">{{ jpSel.jp }}')
rep('<b style="font-size:40px;font-weight:800;line-height:1.3;letter-spacing:-.01em;color:#18324F;text-wrap:balance">{{ ph.jp }}', '<b style="font-size:40px;font-weight:800;line-height:1.3;letter-spacing:-.01em;color:#18324F;text-wrap:balance;word-break:normal;overflow-wrap:anywhere;max-width:100%">{{ ph.jp }}')
# 아이콘 글꼴: 실제 데이터에서 쓰는 아이콘 이름 추가 (이름 목록은 알파벳 순이어야 함)
_fi = dc.index('icon_names='); _fe = dc.index('&amp;display=block', _fi)
_names = sorted(set(dc[_fi + len('icon_names='):_fe].split(',')) | {'temple_buddhist', 'storefront', 'thermostat', 'pin_drop'})
dc = dc[:_fi] + 'icon_names=' + ','.join(_names) + dc[_fe:]
# 오늘 지나는 곳 제목 앞 아이콘 (디자인의 아이콘 칸 규칙: 그라데이션 둥근 사각형 + 흰 아이콘)
rep('<span style="display:flex;align-items:baseline;justify-content:space-between;padding:{{ fr.spPad }}"><b style="font-size:20px;font-weight:800;letter-spacing:-.03em">오늘 지나는 곳</b>',
    '<span style="display:flex;align-items:center;justify-content:space-between;padding:{{ fr.spPad }}"><span style="display:flex;align-items:center;gap:8px"><span style="flex:none;width:30px;height:30px;border-radius:10px;background:linear-gradient(135deg,#7048E8,#9775FA);box-shadow:0 4px 10px rgba(112,72,232,.3);display:grid;place-items:center"><span style="font-family:\'Material Symbols Rounded\';font-weight:normal;font-style:normal;line-height:1;letter-spacing:normal;text-transform:none;white-space:nowrap;direction:ltr;-webkit-font-smoothing:antialiased;font-feature-settings:\'liga\';font-variation-settings:\'FILL\' 1,\'wght\' 500;font-size:18px;color:#fff;">pin_drop</span></span><b style="font-size:20px;font-weight:800;letter-spacing:-.03em">오늘 지나는 곳</b></span>')
# 더보기 메뉴 카드: 빈 공간에 그 메뉴의 주요 내용 미리보기
rep('<span style="display:flex;flex-direction:column;gap:2px"><b style="font-size:16px">{{ m.label }}</b><span style="font-size:13px;color:#4A5D78;white-space:nowrap">{{ m.sub }}</span></span>\n</button>',
    '<span style="display:flex;flex-direction:column;gap:2px"><b style="font-size:16px">{{ m.label }}</b><span style="font-size:13px;color:#4A5D78;white-space:nowrap">{{ m.sub }}</span></span>\n'
    '<span style="margin-top:auto;display:flex;flex-direction:column;gap:6px;width:100%;min-width:0"><b style="font-size:22px;font-weight:800;letter-spacing:-.03em;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{{ m.big }}</b>'
    '<span style="height:6px;border-radius:99px;background:rgba(91,111,212,.15);overflow:hidden;display:{{ m.barD }}"><i style="display:block;height:100%;width:{{ m.pct }};background:{{ m.grad }};border-radius:99px"></i></span>'
    '<span style="font-size:12px;color:#4A5D78;line-height:1.4;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden">{{ m.line }}</span></span>\n</button>')
# 팝업(시트)·하위 화면: 열릴 때 올라오고/밀려 들어오고, 닫힐 때 내려가며 사라짐 + 뒤로 가기는 오른쪽 아래 둥근 버튼
rep('display:flex;align-items:flex-end;justify-content:center;animation:fadeIn .2s">', 'display:flex;align-items:flex-end;justify-content:center;animation:{{ anim.bg }}">')
rep('animation:sheetIn .26s ease-out', 'animation:{{ anim.sh }}')
rep('z-index:12;background:linear-gradient(165deg,#DCE2FF 0%,#EEF0FF 45%,#F9EEF7 100%);animation:fadeIn .2s"', 'z-index:12;background:linear-gradient(165deg,#DCE2FF 0%,#EEF0FF 45%,#F9EEF7 100%);animation:{{ anim.sub }}"')
rep('<button onClick="{{ back }}" style="flex:none;width:44px;height:44px;', '<button onClick="{{ back }}" style="visibility:hidden;flex:none;width:44px;height:44px;')
_si = dc.index('animation:{{ anim.sub }}"'); _si = dc.index('>', _si) + 1
dc = dc[:_si] + ('<button onClick="{{ back }}" aria-label="뒤로 가기" style="position:absolute;right:16px;bottom:calc(env(safe-area-inset-bottom) + 22px);z-index:14;width:60px;height:60px;border-radius:50%;border:1px solid rgba(255,255,255,.95);background:linear-gradient(135deg,#3B5BDB,#6C8CF5);box-shadow:0 10px 24px rgba(59,91,219,.35);display:grid;place-items:center;cursor:pointer">'
                 '<span style="font-family:\'Material Symbols Rounded\';font-weight:normal;font-style:normal;line-height:1;letter-spacing:normal;text-transform:none;white-space:nowrap;direction:ltr;-webkit-font-smoothing:antialiased;font-feature-settings:\'liga\';font-variation-settings:\'FILL\' 1,\'wght\' 500;font-size:28px;color:#fff;">arrow_back</span></button>') + dc[_si:]
rep('@keyframes fadeIn{from{opacity:0}to{opacity:1}}', '@keyframes fadeIn{from{opacity:0}to{opacity:1}}@keyframes fadeOut{from{opacity:1}to{opacity:0}}@keyframes sheetOut{from{transform:none;opacity:1}to{transform:translateY(60px);opacity:0}}@keyframes subIn{from{transform:translateX(40px);opacity:0}to{transform:none;opacity:1}}@keyframes subOut{from{transform:none;opacity:1}to{transform:translateX(40px);opacity:0}}')
rep('overflow-y:auto;scrollbar-width:none;padding-bottom:40px">', 'overflow-y:auto;scrollbar-width:none;padding-bottom:calc(env(safe-area-inset-bottom) + 100px)">')
rep('<div style="display:flex;align-items:center;gap:10px;padding:56px 16px 14px">', '<div style="display:flex;align-items:center;gap:10px;padding:calc(env(safe-area-inset-top) + 14px) 16px 14px">')
rep('<div style="position:absolute;inset:0;z-index:12;background:linear-gradient(165deg,#DCE2FF 0%,#EEF0FF 45%,#F9EEF7 100%);animation:{{ anim.sub }}"', '<div class="subwrap" style="position:absolute;inset:0;z-index:12;background:linear-gradient(165deg,#DCE2FF 0%,#EEF0FF 45%,#F9EEF7 100%);animation:{{ anim.sub }}"')
# ───── 오늘 탭: 날짜 이동을 머리글 오른쪽으로, 그 자리에는 오늘 날씨 카드 ─────
_db0 = dc.index('<div style="display:flex;align-items:center;gap:6px;padding:6px;border-radius:24px;background:rgba(255,255,255,.55);')
_db1 = dc.index('</div>', dc.index('{{ next }}', _db0)) + len('</div>')
_DATEBAR = dc[_db0:_db1]
MSW = lambda px, col: "<span style=\"font-family:'Material Symbols Rounded';font-weight:normal;font-style:normal;line-height:1;letter-spacing:normal;text-transform:none;white-space:nowrap;direction:ltr;-webkit-font-smoothing:antialiased;font-feature-settings:'liga';font-variation-settings:'FILL' 1,'wght' 500;font-size:" + px + "px;color:" + col + ";\">"
_WXCARD = ('<div onClick="{{ wxHome.open }}" style="cursor:pointer;display:flex;align-items:center;gap:14px;padding:12px 14px 12px 12px;border-radius:24px;background:rgba(255,255,255,.55);border:1px solid rgba(255,255,255,.85);backdrop-filter:blur(22px) saturate(1.4);-webkit-backdrop-filter:blur(22px) saturate(1.4);box-shadow:0 8px 24px rgba(40,50,140,.08);min-width:0">'
  '<span style="flex:none;width:52px;height:52px;border-radius:16px;background:linear-gradient(135deg,#1C7ED6,#4DABF7);box-shadow:0 6px 14px rgba(28,126,214,.3);display:grid;place-items:center">' + MSW('30', '#fff') + '{{ wxNow.icon }}</span></span>'
  '<span style="flex:1;display:flex;flex-direction:column;line-height:1.2;min-width:0"><span style="display:flex;align-items:baseline;gap:8px;min-width:0"><b style="font-size:32px;font-weight:800;letter-spacing:-.04em">{{ wxNow.t }}</b><span style="font-size:15px;font-weight:700;color:#3A4D68;white-space:nowrap">{{ wxHome.desc }}</span></span><span style="font-size:13px;color:#4A5D78;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{{ wxHome.place }}</span></span>'
  '<span style="flex:none;display:flex;gap:6px"><sc-for list="{{ wxHome.chips }}" as="c" hint-placeholder-count="3"><span style="display:flex;flex-direction:column;align-items:center;gap:2px;min-width:52px;padding:7px 8px;border-radius:14px;background:rgba(255,255,255,.75)"><span style="font-size:11px;color:#6B7A90;white-space:nowrap">{{ c.k }}</span><b style="font-size:14px;white-space:nowrap;color:{{ c.c }}">{{ c.v }}</b></span></sc-for></span>'
  '</div>')
dc = dc[:_db0] + _WXCARD + dc[_db1:]
_hd = _DATEBAR.replace('<div style="display:flex;align-items:center;gap:6px;padding:6px;border-radius:24px;', '<div style="flex:none;display:flex;align-items:center;gap:4px;padding:4px;border-radius:24px;max-width:60%;', 1)
_wc0 = dc.index('<span style="flex:none;white-space:nowrap;height:36px;padding:0 12px;border-radius:99px;')
_wc1 = dc.index('18°</span>', _wc0) + len('18°</span>')
dc = dc[:_wc0] + '<sc-if value="{{ isHome }}" hint-placeholder-val="{{ true }}">' + _hd + '</sc-if><sc-if value="{{ notHome }}" hint-placeholder-val="{{ false }}">' + dc[_wc0:_wc1] + '</sc-if>' + dc[_wc1:]
# ───── 펼친 화면: 메뉴 바로 위까지 채우기 (스크롤 없이 딱 맞게) ─────
rep('<div onScroll="{{ onScroll }}" style="position:absolute;inset:0;overflow-y:auto;scrollbar-width:none;padding-bottom:130px"', '<div onScroll="{{ onScroll }}" style="position:absolute;inset:0;overflow-y:auto;scrollbar-width:none;padding-bottom:calc(env(safe-area-inset-bottom) + 100px)"')
rep('<div style="display:grid;grid-template-columns:{{ fr.mapCols }};gap:12px;padding:0 16px;align-items:stretch"', '<div class="eq2" style="display:grid;grid-template-columns:{{ fr.mapCols }};gap:12px;padding:0 16px;align-items:stretch"')
# 오늘이 아닌 날 카드: 그날 지역 사진 배경 + 글자 잘 보이게 어두운 그라데이션 (디자인 규칙: 위 .35 / 아래 .88)
_v0 = dc.index('<sc-if value="{{ v.notToday }}" hint-placeholder-val="{{ false }}">'); _v1 = dc.index('</sc-if>', _v0)
_vc = dc[_v0:_v1]
for a_, b_ in [('<div style="flex:1;justify-content:center;border-radius:28px;padding:20px;background:rgba(255,255,255,.55);border:1px solid rgba(255,255,255,.85);backdrop-filter:blur(22px) saturate(1.4);-webkit-backdrop-filter:blur(22px) saturate(1.4);box-shadow:0 8px 24px rgba(40,50,140,.08);display:flex;flex-direction:column;gap:6px">',
                '<div style="flex:1;justify-content:flex-end;min-height:280px;border-radius:28px;padding:20px;background:linear-gradient(180deg,rgba(20,20,50,.35) 0%,rgba(20,20,50,.12) 38%,rgba(20,20,50,.88) 100%),url({{ v.photo }}) center/cover no-repeat,linear-gradient(135deg,#8B9CF0,#C9B8F5);border:1px solid rgba(255,255,255,.5);box-shadow:0 14px 30px rgba(40,50,140,.22);display:flex;flex-direction:column;gap:6px;color:#fff;text-shadow:0 1px 3px rgba(0,0,0,.35)">'),
               ('<span style="font-size:14px;font-weight:700;color:#4A5D78">{{ v.kind }}</span>', '<span style="font-size:14px;font-weight:700;color:rgba(255,255,255,.92)">{{ v.kind }}</span>'),
               ('<b style="font-size:24px;font-weight:800;letter-spacing:-.04em;line-height:1.25">{{ v.path }}</b>', '<b style="font-size:28px;font-weight:800;letter-spacing:-.04em;line-height:1.25">{{ v.path }}</b>'),
               ('<span style="font-size:14px;color:#4A5D78">{{ v.jp }}</span>', '<span style="font-size:14px;color:rgba(255,255,255,.88)">{{ v.jp }}</span>'),
               ('<span style="border-radius:16px;background:rgba(255,255,255,.7);padding:10px 12px;display:flex;flex-direction:column;gap:2px">', '<span style="border-radius:16px;background:rgba(255,255,255,.85);padding:10px 12px;display:flex;flex-direction:column;gap:2px;color:#18324F;text-shadow:none">')]:
    assert _vc.count(a_) == 1, a_[:60]
    _vc = _vc.replace(a_, b_)
dc = dc[:_v0] + _vc + dc[_v1:]
# 오늘 탭 경로 카드: 가로 점 목록 → 세로 '오늘의 경유지' 목록(이름·일본어·상태/예정 시각·거리)
_h0 = dc.index('<span style="display:flex;width:100%">\n<sc-for list="{{ stops }}" as="s" hint-placeholder-count="4">')
_h1 = dc.index('</sc-for>\n</span>', _h0) + len('</sc-for>\n</span>')
_s0 = dc.index('<sc-for list="{{ stops }}" as="s" hint-placeholder-count="4">\n<div style="display:grid;grid-template-columns:28px minmax(0,1fr) auto;')
_s1 = dc.index('</sc-for>', _s0) + len('</sc-for>')
_LIST = dc[_s0:_s1]
dc = dc[:_h0] + '<div style="display:flex;flex-direction:column;border-radius:18px;background:rgba(255,255,255,.6);padding:2px 14px"><span style="font-size:14px;font-weight:800;padding:12px 0 2px">오늘의 경유지</span>' + _LIST + '</div>' + dc[_h1:]
# 머리글 문구·날씨를 실제 값으로
rep('<span style="font-size:13px;color:#4A5D78">도카이도 종주 · {{ todayN }}일째</span>', '<span style="font-size:13px;color:#4A5D78">{{ headSub }}</span>')
rep("font-size:18px;color:#E0861A;\">sunny</span>18°</span>", "font-size:18px;color:{{ wxNow.c }};\">{{ wxNow.icon }}</span>{{ wxNow.t }}</span>")

# 가짜 지도(타일 그림 + 그린 선 + 가짜 핀) → 실제 지도(Leaflet) 자리
def swap_maps():
    global dc
    n = 0
    while True:
        t = dc.find('<img src="https://tile.openstreetmap.org/')
        if t < 0:
            break
        a = dc.rindex('<span', 0, t)
        m = dc.index('<sc-for list="{{ mp.mk }}"', t)
        e = dc.index('</sc-for>', m) + len('</sc-for>')
        kind = ['home', 'sheet', 'tab'][n] if n < 3 else 'x'
        dc = dc[:a] + '<div data-v8map="' + kind + '" data-k="{{ mapKey }}" style="position:absolute;inset:0;z-index:0"></div>' + dc[e:]
        n += 1
    return n
print('maps swapped:', swap_maps())

# ───────────────────────── 2. 문서 머리 ─────────────────────────
DEMO = r'''<script>(function(){ if (!/[?&]demo=1/.test(location.search)) return; window.__demo = 1;
  /* 예시 화면: 여행 12일째(12/15 13:00)로 가정하고 예시 숫자를 보여줌. 실제 저장값·백업은 건드리지 않음 */
  var T = new Date('2026-12-15T13:00:00+09:00').getTime(), D = Date, t0 = D.now();
  function F() { var a = arguments; if (!(this instanceof F)) return new D(T + (D.now() - t0)).toString(); return a.length ? new (Function.prototype.bind.apply(D, [null].concat([].slice.call(a))))() : new D(T + (D.now() - t0)); }
  F.prototype = D.prototype; F.now = function () { return T + (D.now() - t0); }; F.parse = D.parse; F.UTC = D.UTC; window.Date = F;
  try { var LS = window.localStorage, gi = LS.getItem.bind(LS), si = LS.setItem.bind(LS), ri = LS.removeItem.bind(LS);
    Storage.prototype.getItem = function (k) { return gi('demo:' + k); }; Storage.prototype.setItem = function (k, v) { return si('demo:' + k, v); }; Storage.prototype.removeItem = function (k) { return ri('demo:' + k); }; } catch (e) {}
  var days = {}, base = [18240, 21530, 19870, 23110, 16420, 24980, 22310, 17650, 25440, 20120, 13870];
  for (var i = 0; i < 11; i++) { var d = new D(2026, 11, 4 + i), k = d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0'); days[k] = { steps: base[i], km: +(base[i] / 1340).toFixed(1), min: Math.round(base[i] / 1340 * 14.5), hr: 104 + i % 9, kcal: 1100 + i * 23, sleep: 380 + i * 7, hourly: { 8: base[i] * .12, 9: base[i] * .18, 10: base[i] * .17, 11: base[i] * .1, 13: base[i] * .16, 14: base[i] * .15, 15: base[i] * .12 } }; }
  days['2026-12-15'] = { steps: 17820, km: 12.4, min: 192, hr: 112, kcal: 1240, sleep: 412, weight: 76.4, hourly: { 7: 1820, 8: 2950, 9: 3100, 10: 2400, 11: 1200, 12: 3200, 13: 3150 } };
  var of = window.fetch; window.fetch = function (u, o) { if (typeof u === 'string' && /hc-read/.test(u)) return Promise.resolve(new Response(JSON.stringify({ days: days, last: null, snaps: [], dist: {}, locs: {} }), { status: 200, headers: { 'Content-Type': 'application/json' } })); if (typeof u === 'string' && /tk-sync/.test(u)) return Promise.reject(new Error('demo')); return of.apply(this, arguments); };
  try { si('demo:tk-v15-data', JSON.stringify({ stage: 3, bodyLog: { '2026-12-15': { '발바닥': 2, '무릎': 1, '종아리': 3, '어깨': 0, '피로': 2 } }, expLog: { '2026-12-15': [{ cat: '식비', note: '식비', v: 1980, c: 'jpy' }, { cat: '숙박', note: '숙박', v: 7800, c: 'jpy' }, { cat: '기타', note: '기타', v: 300, c: 'jpy' }] }, noteLog: { '2026-12-14': '사타 고개에서 후지산이 끝까지 보였다.', '2026-12-13': '요시와라 지나며 비. 신발 말리기가 일.' } })); ri('demo:tk-hc3'); } catch (e) {}
  document.addEventListener('DOMContentLoaded', function () { var b = document.createElement('div'); b.textContent = '예시 화면 · 숫자는 예시예요'; b.style.cssText = 'position:fixed;left:50%;top:calc(env(safe-area-inset-top) + 6px);transform:translateX(-50%);z-index:9999;padding:5px 12px;border-radius:99px;background:#E0861A;color:#fff;font:800 12px Pretendard,sans-serif;pointer-events:none;box-shadow:0 4px 10px rgba(0,0,0,.2)'; document.body.appendChild(b); });
})();</script>'''
head_shim = old[old.index('<script>(function(){var F=\'.image-slots.state.json\''):]
head_shim = head_shim[:head_shim.index('</script>') + 9]
rep('<meta name="viewport" content="width=device-width, initial-scale=1">',
    '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">' + DEMO + '<title>도카이도 53의 쉼표</title>'
    '<meta name="theme-color" content="#DCE2FF"><meta name="mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-capable" content="yes">'
    '<meta name="apple-mobile-web-app-status-bar-style" content="default">'
    '<link rel="manifest" href="/manifest.json"><link rel="icon" href="/icon-192.png"><link rel="apple-touch-icon" href="/icon-180.png">'
    '<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"><script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>'
    '<script src="./image-slot.js"></script><style>image-slot.ro{pointer-events:none}image-slot.ro::part(empty){display:none!important}html,body{overscroll-behavior:none;-webkit-text-size-adjust:100%;overflow-x:hidden;touch-action:pan-y}[data-v8map] .leaflet-control-attribution{display:none}@media (min-width:640px){.eq2{min-height:calc(100lvh - env(safe-area-inset-top) - env(safe-area-inset-bottom) - 186px)!important}.subwrap .eq2{min-height:calc(100lvh - env(safe-area-inset-top) - env(safe-area-inset-bottom) - 72px - 104px)!important}.eq2>div{display:flex;flex-direction:column}.eq2>div>:last-child{flex:1 1 auto}.jp2>:last-child{position:sticky;top:calc(env(safe-area-inset-top) + 64px)}}</style>'
    + head_shim)

# ───────────────────────── 3. 로직: 기존 앱 로직 + 새 화면 값 ─────────────────────────
oa = old.index('<script type="text/x-dc"'); ob = old.index('>', oa) + 1; oe = old.index('</script>', ob)
OLD = old[ob:oe]
# 기존 화면값 계산은 oldVals 로 이름만 바꿔 그대로 쓰고, 필요한 중간값을 밖으로 꺼냄
OLD = rep('  renderVals() {', '  oldVals() {', src=OLD)
OLD = rep('\n    return {\n      morePlaces:', '\n    return { _x: { dd, n, stage, reached, done, isToday, isPast, walked, remain, steps, mins, hcT, stationsDone, posKmF, eta, today, view, places },\n      morePlaces:', src=OLD)

na = dc.index('<script type="text/x-dc"'); nb = dc.index('>', na) + 1; ne = dc.index('</script>', nb)
NEW = dc[nb:ne]
ci = NEW.index('class Component extends DCLogic {')
NEWC = NEW[ci + len('class Component extends DCLogic {'):NEW.rindex('}')]

# 새 화면 상태: 기존 상태와 이름이 겹치는 것은 n 접두로 분리 (기존 저장값을 덮지 않도록)
s0 = NEWC.index('  state = (() => {'); s1 = NEWC.index('})();', s0) + len('})();')
st = NEWC[s0:s1]
st = st.replace('  state = (() => {', '  nInit() {', 1)[:-len('})();')] + '}'
for a, b in [("amt:'', cat:'식비'", "amt:'', ncat:'식비'"), ("exp:[{cat:'식비'", "nexp:[{cat:'식비'"), ("note:'', noteSaved", "nnote:'', noteSaved"),
             ("fxDir:'jk'", "nfxDir:'jk'"), ("view:11, ", ""), ("...(g==='past'?{view:8}:{}), ...(g==='future'?{view:13}:{}), ", ""), ("arr:2, ", ""), ("...(g==='done'?{arr:4}:{}), ", "")]:
    st = rep(a, b, src=st)
rv = NEWC[NEWC.index('  renderVals() {'):]
rv = rv.replace('  renderVals() {', '  renderVals() {\n    const O = this.oldVals(), X = O._x;', 1)

R = [
    # 역참 이름·거리: 기존 데이터(ST)
    (re.search(r"    const KO = \[.*?\];\n    const JP = \[.*?\];\n    const KM = \[.*?\];\n", rv, re.S).group(0),
     "    const KO = ST.map(t => t.ko.replace(/\\(.*\\)/, '')), JP = ST.map(t => t.jp), KM = ST.map(t => t.km);\n"),
    (re.search(r"    const E = \[.*?\];\n", rv).group(0), ""),
    ("const WD = ['일','월','화','수','목','금','토'], TODAY = 11, TR = {17:5.7, 24:27.3};",
     "const WD = ['일','월','화','수','목','금','토'], TODAY = X.today - 1, VW = X.view - 1, DIST = X.dd.dist, HT = window.TK_HOTELS || {};"),
    # 날짜별 구간: 기존 일정(PLAN·dayData)
    (re.search(r"    const day = i => \{.*?\n.*?\n", rv).group(0),
     "    const day = i => { const P = PLAN[i+1], s = P[0]+1, e = P[1]+1, d = new Date(2026,11,4+i), q = dayData(i+1), dist = q.dist, rest = s===e;\n"
     "      return { i, n:i+1, s, e, dist, rest, tr:q.trKm||0, date:(d.getMonth()+1)+'.'+d.getDate()+' ('+WD[d.getDay()]+')', path: rest ? KO[s-1]+' · 휴식' : KO[s-1]+' → '+KO[e-1], jp: rest ? JP[s-1] : JP[s-1]+' → '+JP[e-1] }; };\n"),
    ("const D = day(S.view), isT = S.view === TODAY;", "const D = day(VW), _df = this.dayInfo().diff, isT = VW === TODAY && X.isToday && _df >= 0 && _df <= 30;"),
    # 오늘 구간의 지점과 진행: 기존 단계(stage)·걸은 거리
    ("const STOPS = [19,20,21,22].map(n => ({ n, ko:KO[n-1], jp:JP[n-1], rel:+(KM[n-1]-KM[18]).toFixed(1) }));",
     "const STOPS = X.dd.stops.map((t,k) => ({ n:k, ko:t.ko.replace(/\\(.*\\)/, ''), jp:t.jp, rel:t.rel }));"),
    ("const arr = S.arr, done = arr >= 4, nxt = done ? null : STOPS[arr], pos = Math.max(12.4, STOPS[Math.min(arr,4)-1].rel), walked = done ? 20.2 : pos;",
     "const arr = Math.max(0, X.stage), done = X.done && X.stage > 0, nxt = done ? null : STOPS[Math.min(arr, STOPS.length-1)], walked = X.walked;"),
]
for a, b in R:
    rv = rep(a, b, src=rv)
# 20.2km(시안 숫자) → 실제 오늘 거리
rv = rep("name:'후지에다', jp:'藤枝', sub:'도착 · 20.2km 걸었어요'", "name:STOPS[STOPS.length-1].ko, jp:STOPS[STOPS.length-1].jp, sub:'도착 · '+DIST+'km 걸었어요'", src=rv)
rv = rep("walked:'20.2km'", "walked:DIST+'km'", src=rv)
rv = rv.replace('20.2', 'DIST')
R2 = [
    ("const past = k < arr, cur = k === arr, last = k === 3;", "const past = k < arr, cur = k === arr && !done, last = k === STOPS.length-1;"),
    ("note: past ? (k===0?'08:02 출발':k===1?'09:31 도착':k===2?'11:40 도착':'도착') : cur",
     "note: past ? (k===0?'출발':'지나옴'+(((S.passed||{})[X.iso]||{})[s.ko] ? ' · '+((S.passed||{})[X.iso]||{})[s.ko] : '')) : cur"),
    ("const past = S.view < TODAY, ids = [];", "const past = X.isPast, ids = [];"),
    ("const N = S.view < 30 ? day(S.view+1) : null;", "const N = VW < 30 ? day(VW+1) : null;"),
    ("const past = S.view < TODAY;", "const past = X.isPast;"),
]
R2 += [("const v = { ...D, isToday:isT, notToday:!isT,", "const v = { ...D, isToday:isT, notToday:!isT, photo: '/assets/dayhero/'+(VW+1)+'.jpg',")]
R2 += [("cur ? '다음 · '+(s.rel-walked).toFixed(1)+'km 남음' : last ? '오늘 숙소' : '예정' }", "cur ? '다음 · '+(s.rel-walked).toFixed(1)+'km 남음 · '+hhmm(START_MIN + s.rel*MIN_PER_KM)+' 도착 예정' : last ? '오늘 숙소 · '+hhmm(START_MIN + s.rel*MIN_PER_KM)+' 도착 예정' : '예정 · '+hhmm(START_MIN + s.rel*MIN_PER_KM) }")]
for a, b in R2:
    rv = rep(a, b, src=rv)
# 지나는 곳: 기존 명소 데이터
SPm = re.search(r"    const SP = \[\n.*?\n    \];\n", rv, re.S).group(0)
rv = rep(SPm, "    const CI = { '역사유적':'museum', '신사·사찰':'temple_buddhist', '명물 음식':'restaurant', '자연·전망':'landscape', '공예·특산':'storefront' };\n"
         "    const SP = (X.places || []).map(p => { const c = (p.desc || '').split(' · ')[0]; return { ko:p.name, jp:p.q || '', at:p.km, icon: CI[c] || 'location_on', short:(p.desc || '').split(' · ').slice(1).join(' · ') || p.desc, desc:(p.long || p.desc || ''), ll:p.ll }; });\n", src=rv)
rv = rep("map: 'https://www.google.com/maps/dir/?api=1&travelmode=walking&destination='+encodeURIComponent(p.jp), open:",
         "map: 'https://www.google.com/maps/dir/?api=1&travelmode=walking&destination='+(p.ll ? p.ll[0]+','+p.ll[1] : encodeURIComponent(p.jp || p.ko)), open:", src=rv)
rv = rep("const spots = SP.map(spotOf), sp = S.sheet && S.sheet.type==='spot' ? spots[S.sheet.i] : {};", "const spotsAll = SP.map(spotOf), sp = S.sheet && S.sheet.type==='spot' ? (spotsAll[S.sheet.i] || {}) : {}, _fu = SP.findIndex(p => !(X.isPast || (isT && p.at <= walked))), _st = Math.max(0, Math.min(SP.length-4, (_fu < 0 ? SP.length : _fu) - 1)), spots = " + WIDE + " ? spotsAll.slice(_st, _st+4) : spotsAll;", src=rv)
rv = rep("const passed = p.at <= walked, d = Math.abs(p.at - walked);", "const passed = X.isPast || (isT && p.at <= walked), d = Math.abs(p.at - (isT ? walked : 0));", src=rv)
rv = rep("const spI = S.sheet && S.sheet.type==='spot' ? S.sheet.i : 0, spN = SP.length;", "const spI = S.sheet && S.sheet.type==='spot' ? S.sheet.i : 0, spN = Math.max(1, SP.length);", src=rv)
rv = rep("const passedN = SP.filter(p => p.at <= walked).length;", "const passedN = SP.filter(p => X.isPast || (isT && p.at <= walked)).length;", src=rv)
# 숙소: 기존 숙소 목록(HOTELS)
LOm = re.search(r"    const lodgeOf = d => \{.*?\};\n", rv, re.S).group(0)
rv = rep(LOm, "    const lodgeOf = d => { const h = HT[d.n] || HT[String(d.n)] || null, conf = !!(h && h.ko), q = h && h.ll && !/^35\\.0,138\\.5$/.test(h.ll) ? h.ll : (h && (h.ja || h.en || h.ko)) || (JP[d.e-1]+'駅 ホテル');\n"
         "      return { when: (d.i===TODAY?'오늘':d.n+'일차')+' 숙소 · '+KO[d.e-1], name: conf ? h.ko : KO[d.e-1]+' · 숙소 미정', chip: conf?'예약 확정':'미정', chipBg: conf?'#E4F8EC':'#FFF3D8', chipFg: conf?'#16804A':'#8A5A0E',\n"
         "      facts:[{k:'도착 지점',v:KO[d.e-1]},{k:'지역',v:(h && h.town) || JP[d.e-1]},{k:'예약',v:conf?'확정':'미정'}], map:'https://www.google.com/maps/dir/?api=1&travelmode=walking&destination='+encodeURIComponent(q) }; };\n", src=rv)
# 지난 날 기록: 실제 건강 기록
rv = rep("facts: past ? [{k:'걸은 거리',v:(D.rest?0:D.dist-D.tr).toFixed(1)+'km'},{k:'걸음',v:D.rest?'—':f1(Math.round((D.dist-D.tr)*1330))},{k:'걸은 시간',v:D.rest?'—':Math.floor((D.dist-D.tr)/4.3)+':'+String(Math.round(((D.dist-D.tr)/4.3%1)*60)).padStart(2,'0')}]",
         "facts: past ? [{k:'걸은 거리',v:X.hcT ? (+X.hcT.km||0).toFixed(1)+'km' : '—'},{k:'걸음',v:X.hcT && X.hcT.steps ? f1(X.hcT.steps) : '—'},{k:'걸은 시간',v:X.hcT && X.hcT.min != null ? Math.floor(X.hcT.min/60)+':'+String(X.hcT.min%60).padStart(2,'0') : '—'}]", src=rv)
# 시간대별 걸음(7시~18시): 실제 기록
rv = rep("const hrs = [0,1820,2950,3100,2400,1200,3200,3150,0,0,0,0], mx = 3200;",
         "const hrs = Array.from({length:12},(x,k) => +((((X.hcT||{}).hourly)||{})[7+k] || 0)), mx = Math.max(1, ...hrs);", src=rv)
# 걸음·걸은 시간·누적
rv = rep("tiles: [{k:'걸음',v:'17,820',u:'걸음',icon:'steps',grad:'linear-gradient(135deg,#1C7ED6,#4DABF7)'},{k:'걸은 시간',v:'3:12',u:'시간',icon:'schedule',grad:'linear-gradient(135deg,#7048E8,#9775FA)'}],",
         "tiles: [{k:'걸음',v:f1(X.steps||0),u:'걸음',icon:'steps',grad:'linear-gradient(135deg,#1C7ED6,#4DABF7)'},{k:'걸은 시간',v:Math.floor((X.mins||0)/60)+':'+String((X.mins||0)%60).padStart(2,'0'),u:'시간',icon:'schedule',grad:'linear-gradient(135deg,#7048E8,#9775FA)'}],", src=rv)
rv = rep("const km = isT ? 167.8+walked : KM[D.e-1]; const stN = KO.slice(0,53).filter((x,k) => KM[k] <= km).length;",
         "const km = isT ? X.posKmF : X.isPast ? KM[D.e-1] : KM[D.s-1]; const stN = KO.slice(0,53).filter((x,k) => KM[k] <= km + .01).length;", src=rv)
rv = rep("const km = isT ? 167.8+walked : 167.8;", "const km = X.posKmF;", src=rv)
rv = rep("health: [{k:'평균 심박',v:'112bpm'},{k:'소모',v:'1,240kcal'},{k:'페이스',v:\"15'28\\\"/km\"}]",
         "health: (() => { const h = X.hcT || {}, pace = h.km > .3 && h.min ? h.min / h.km : 0; return [{k:'평균 심박',v:h.hr ? h.hr+'bpm' : '—'},{k:'소모',v:h.kcal ? f1(h.kcal)+'kcal' : '—'},{k:'페이스',v:pace ? Math.floor(pace)+\"'\"+String(Math.round(pace%1*60)).padStart(2,'0')+'\"/km' : '—'}]; })()", src=rv)
# 날짜 이동·도착 체크: 기존 동작
R3 = [
    ("prevO: S.view === 0 ? '.35' : '1', nextO: S.view === 30 ? '.35' : '1',", "prevO: VW === 0 ? '.35' : '1', nextO: VW === 30 ? '.35' : '1',"),
    ("prev: () => S.view > 0 && set({ view:S.view-1, sheet:null }), next: () => S.view < 30 && set({ view:S.view+1, sheet:null }), goToday: () => set({ view:TODAY, sheet:null }),",
     "prev: () => { O.prevDay(); set({ sheet:null }); }, next: () => { O.nextDayFn(); set({ sheet:null }); }, goToday: () => { O.goToday(); set({ sheet:null }); },"),
    ("check: () => S.arr < 4 && set({ arr:S.arr+1 }), undo: () => S.arr > 2 && set({ arr:S.arr-1 }), undoO: S.arr > 2 ? '1' : '.4',",
     "check: () => { if (isT && !done) O.advance(); }, undo: () => { if (isT && X.stage > 1) this.setState(s => ({ stage: Math.max(1, Math.min(s.stage, STOPS.length) - 1) })); }, undoO: isT && X.stage > 1 ? '1' : '.4',"),
    ("todayN: TODAY+1,", "todayN: TODAY+1, headSub: (() => { const df = this.dayInfo().diff; return df < 0 ? '도카이도 종주 · 출발까지 D-'+(-df) : df > 30 ? '도카이도 종주 · 완주' : '도카이도 종주 · '+(df+1)+'일째'; })(), wxNow: (() => { const w = S.wlive; if (!w || w.now == null) return { icon:'partly_cloudy_day', t:'—', c:'#8C96C2' }; const c = w.code, ic = c <= 1 ? 'sunny' : c <= 3 ? 'partly_cloudy_day' : c >= 51 && c <= 82 ? 'rainy' : 'cloud'; return { icon: ic, t: Math.round(w.now)+'°', c: ic==='sunny' ? '#E0861A' : ic==='rainy' ? '#1C7ED6' : '#8C96C2' }; })(), mapKey: VW+'|'+arr+'|'+((this.routeCache||{})[VW+1] ? 1 : 0),"),
    ("isHome: S.t==='home',", "isHome: S.t==='home', rec, wxHome: (() => { const w = S.wlive, d = (w && w.d) || null, nm = { sunny:'맑음', partly_cloudy_day:'구름 조금', rainy:'비', cloud:'흐림' }; const ic = w && w.code != null ? (w.code <= 1 ? 'sunny' : w.code <= 3 ? 'partly_cloudy_day' : w.code >= 51 && w.code <= 82 ? 'rainy' : 'cloud') : null; const rp = d && d.precipitation_probability_max ? (d.precipitation_probability_max[0] ?? 0) : null; return { desc: ic ? nm[ic] : '날씨 불러오는 중', place: (w && w.name ? w.name+' · ' : '') + '오늘 날씨', open: () => set({ t:'more', sub:'info', sheet:null }), chips: [{k:'최고/최저',v: d && d.temperature_2m_max ? Math.round(d.temperature_2m_max[0])+'°/'+Math.round(d.temperature_2m_min[0])+'°' : '—',c:'#18324F'},{k:'강수',v: rp != null ? rp+'%' : '—',c: rp >= 50 ? '#1C7ED6' : '#18324F'},{k:'일몰',v: d && d.sunset ? String(d.sunset[0]).slice(11,16) : '—',c:'#7048E8'}] }; })(), anim: S.closing==='sheet' ? { bg:'fadeOut .22s ease-in forwards', sh:'sheetOut .22s ease-in forwards', sub:'subIn .26s ease-out' } : S.closing==='sub' ? { bg:'fadeIn .2s', sh:'sheetIn .26s ease-out', sub:'subOut .22s ease-in forwards' } : { bg:'fadeIn .2s', sh:'sheetIn .26s ease-out', sub:'subIn .26s ease-out' }, glHead: (() => { const df = this.dayInfo().diff; return df < 0 ? '시나가와 → 교토 · 출발 전' : '시나가와 → 교토 · '+Math.min(31, df+1)+'일째'; })(), glToday: this.dayInfo().diff < 0 ? '출발 전' : '오늘 '+(TODAY+1)+'일', jnStat: (() => { const df = this.dayInfo().diff, all = Array.from({length:31},(x,k)=>day(k)), w = df < 0 ? 0 : Math.min(31, df), r = all.filter(d => d.rest).length; return { w: w+'일', l: Math.max(0, 31-w-(df >= 0 && df <= 30 ? 1 : 0))+'일', r: r+'일' }; })(), wxCard: (() => { const w = S.wlive; if (!w || w.now == null) return { place:'지금', icon:'partly_cloudy_day', t:'—', desc:'날씨 불러오는 중' }; const c = w.code, ic = c <= 1 ? 'sunny' : c <= 3 ? 'partly_cloudy_day' : c >= 51 && c <= 82 ? 'rainy' : 'cloud', nm = { sunny:'맑음', partly_cloudy_day:'구름 조금', rainy:'비', cloud:'흐림' }[ic], d = w.d || {}; return { place: '지금 · '+(w.name || (w.src === 'gps' ? '내 위치' : '구간 날씨')), icon: ic, t: Math.round(w.now)+'°', desc: nm + (d.temperature_2m_max ? ' · 최고 '+Math.round(d.temperature_2m_max[0])+'° / 최저 '+Math.round(d.temperature_2m_min[0])+'°' : '') }; })(), fxLabel: '100엔 = '+Math.round(rate*100)+'원 · '+(S.fxAuto ? '자동 '+S.fxAuto.t : '기본값'),"),
    ("onScroll: e => { const c = e.currentTarget.scrollTop > 60;", "onScroll: e => { const c = e.currentTarget.scrollTop > 56;"),
]
R3 += [("close: () => set({ sheet:null }),", "close: () => this.closeSheet(),"),
       ("back: () => set({ sub:null }),", "back: () => this.closeSub(),")]
for a, b in R3:
    rv = rep(a, b, src=rv)
rv = rep("    const F = " + WIDE, """    try { const q = dayData(VW+1), rc = (this.routeCache||{})[VW+1], iso = X.iso, tk = isT ? (((S.track||{})[iso])||[]).concat((((S.hc||{}).locs||{})[iso])||[]).sort((a,b) => a[2]-b[2]) : [];
      window.__v8 = { route: rc && rc.pts ? rc.pts : q.route, stops: q.stops.map((t,k) => ({ ll:t.ll, past: X.isPast || (isT && k < arr) })), trk: tk, me: isT && tk.length ? [tk[tk.length-1][0], tk[tk.length-1][1]] : null, amen: amenOn.map(a => ({ ll:a.ll, lt:a.lt, c:a.c })), logTrk: String((O.hov||{}).trk||'').split(';').filter(Boolean).map(q => q.split(',').map(Number)) }; } catch (e) {}
    const F = """ + WIDE, src=rv)
rv = rep("q: QS[S.view % 3]", "q: QS[(VW+3) % 3]", src=rv)
rv = rep("when:(S.view+1===TODAY+1?'내일'", "when:(VW+1===TODAY+1?'내일'", src=rv)
assert 'S.view' not in rv, rv[rv.index('S.view') - 200:rv.index('S.view') + 100]
assert 'S.arr' not in rv, rv[rv.index('S.arr') - 200:rv.index('S.arr') + 100]
# 이름이 겹치는 상태(지출·메모·환율·카테고리)는 새 화면 전용 이름으로 (다음 단계에서 실제 기록과 연결)
for a, b in [("S.cat", "S.ncat"), ("set({ cat:c })", "set({ ncat:c })"), ("S.exp", "S.nexp"), ("exp:[...S.nexp", "nexp:[...S.nexp"),
             ("S.note", "S.nnote"), ("set({ note:e.target.value", "set({ nnote:e.target.value"), ("S.fxDir", "S.nfxDir"), ("set({ fxDir:", "set({ nfxDir:")]:
    rv = rv.replace(a, b)
# ───── 기록 탭: 실제 건강 기록·몸 상태·지출·하루 글·체중 ─────
OLD = rep("synced: v.synced || '' };", "synced: v.synced || '', sleep: v.sleepMin == null ? null : v.sleepMin, weight: v.weight == null ? null : v.weight };", src=OLD)
OLD = rep("'bodyLog', ", "'bodyLog', 'expLog', 'noteLog', ", cnt=1, src=OLD)
LGa = rv.index('    // log\n'); LGb = rv.index('    // jp\n')
rv = rv[:LGa] + r"""    // log (실제 기록)
    const ISO = X.iso, isoOf = d => d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');
    const HCD = (S.hc && S.hc.days) || {}, hT = HCD[ISO] || {};
    const CKS = ['발바닥','무릎','종아리','어깨','피로'];
    const bl = S.bodyLog || {}, b0 = bl[ISO] || {}, condT = Object.fromEntries(CKS.map(k => [k, b0[k] != null ? b0[k] : 0]));
    const rate = ((S.fxAuto && S.fxAuto.r) || (S.fxRate && +S.fxRate) || 905) / 100, toW = e => e.c==='jpy' ? e.v*rate : e.v;
    const EL = S.expLog || {}, expT = EL[ISO] || [];
    const totW = expT.reduce((q,e)=>q+toW(e),0);
    const T0 = new Date(2026,11,4), started = new Date() >= T0;
    const cumW = Object.entries(EL).filter(([k]) => !started || k >= '2026-12-04').reduce((q,[k,a]) => q + a.reduce((r,e)=>r+toW(e),0), 0);
    const NL = S.noteLog || {}, prevNotes = Object.keys(NL).filter(k => k < ISO && NL[k]).sort().reverse().slice(0,3).map(k => { const d = new Date(k+'T00:00:00'), df = Math.round((new Date(ISO+'T00:00:00') - d)/864e5); return { d:k, label:(d.getMonth()+1)+'/'+d.getDate()+' · '+(df===1?'어제':df===2?'그제':df+'일 전'), t:NL[k] }; });
    const QS = ['오늘 가장 기억에 남는 순간은?','오늘 고마웠던 사람은?','내일의 나에게 한마디?'];
    const stepsT = +hT.steps || 0, cumSteps = Object.entries(HCD).filter(([k]) => k >= '2026-12-04' && k <= ISO).reduce((q,[k,v]) => q + (+v.steps||0), 0);
    const wNow = S.wToday || hT.weight || (() => { const k = Object.keys(HCD).filter(k => HCD[k].weight).sort().pop(); return k ? HCD[k].weight : null; })();
    const lgTop = { pct: Math.min(100, Math.round(stepsT/200))+'%', steps: f1(stepsT), cum: started ? (TODAY+1)+'일차까지 '+f1(cumSteps)+'걸음' : '출발 전 · 오늘 기록', hr: hT.hr ? hT.hr+'bpm' : '—', sleep: hT.sleep ? (hT.sleep/60).toFixed(1)+'시간' : '—', w: wNow ? (+wNow).toFixed(1)+'kg' : '—' };
    const np = Math.min(S.np || 0, Math.max(0, prevNotes.length-1));
    const HV = (X.hcH && X.hcH.map) || {}, hrsL = Array.from({length:18},(x,k) => Math.round(+HV[6+k] || 0)), hmx = Math.max(1, ...hrsL), RR = X.hcR || {}, HO = O.hov || {};
    const rec = { label: X.recLabel, prev: HO.recPrev, next: HO.recNext, pO: String(HO.recPrevOp), nO: String(HO.recNextOp), key: X.recIso+'|'+(HO.trkN||0),
      facts: [{k:'걸은 거리',v: RR.km ? (+RR.km).toFixed(1)+'km' : '—'},{k:'걸음',v: RR.steps ? f1(RR.steps) : '—'},{k:'걸은 시간',v: RR.min != null ? Math.floor(RR.min/60)+':'+String(RR.min%60).padStart(2,'0') : '—'}],
      bars: hrsL.map((v,k) => ({ h: Math.max(3, Math.round(v/hmx*90))+'px', c: v ? 'linear-gradient(180deg,#74C0FC,#1C7ED6)' : 'rgba(24,50,79,.1)', l: String(6+k), v: v >= 1000 ? (v/1000).toFixed(1)+'천' : v ? String(v) : '' })),
      hourNote: (X.hcH && X.hcH.note) || '', mapNote: HO.trkN ? '폰 위치 기록 '+HO.trkN+'점 · 보라 실선 = 걸음 · 주황 점선 = 차량·전철' : '이 날은 기록된 위치가 없어요' };
    const lg = {
      cond: CKS.map(k => ({ label:k, opts:[0,1,2,3,4,5].map(n => { const on = condT[k]===n; return { v:n, bg: on ? (n>=4?'linear-gradient(135deg,#C92A42,#F06A7F)':n>=2?'linear-gradient(135deg,#7048E8,#9775FA)':'linear-gradient(135deg,#3B5BDB,#6C8CF5)') : 'rgba(255,255,255,.75)', fg: on ? '#fff' : '#6B7A90', bd: on ? 'transparent' : '#DCE0F7', pick: () => set({ bodyLog:{...bl,[ISO]:{...condT,[k]:n}}, condSaved:false }) }; }) })),
      condBtn: S.condSaved ? '저장됨 ✓' : '저장', condBtnBg: S.condSaved ? '#E4F8EC' : 'linear-gradient(135deg,#3B5BDB,#6C8CF5)', condBtnFg: S.condSaved ? '#16804A' : '#fff', saveCond: () => set({ condSaved:true, bodyLog:{...bl,[ISO]:{...condT}} }),
      cur: [['jpy','엔'],['krw','원']].map(([k,label]) => { const on = S.cur===k; return { label, bg: on ? '#fff' : 'transparent', fg: on ? '#3B5BDB' : '#6B7A90', sh: on ? '0 2px 6px rgba(40,50,140,.15)' : 'none', pick: () => set({ cur:k }) }; }),
      amt: S.amt, onAmt: e => { const d = dig(e.target.value); set({ amt: d ? Number(d).toLocaleString('ko-KR') : '' }); },
      cats: ['식비','숙박','교통','기타'].map(c => ({ label:c, ...chipOf(S.ncat===c), pick: () => set({ ncat:c }) })),
      add: () => { const v = Number(dig(S.amt)); if (v) set({ expLog:{...EL,[ISO]:[...expT,{cat:S.ncat,note:S.ncat,v,c:S.cur,t:Date.now()}]}, amt:'' }); },
      items: expT.map((e,k) => ({ cat:e.cat, note:e.note, v: e.c==='jpy' ? '¥'+fmt(e.v) : '₩'+fmt(e.v), del: () => set({ expLog:{...EL,[ISO]:expT.filter((x,j)=>j!==k)} }) })),
      total: '₩'+fmt(totW), cum: '₩'+fmt(cumW),
      note: NL[ISO] || '', onNote: e => set({ noteLog:{...NL,[ISO]:e.target.value}, noteSaved:false }), q: QS[(new Date().getDate()) % 3],
      noteBtn: S.noteSaved ? '저장됨 ✓' : '저장', noteBtnBg: S.noteSaved ? '#E4F8EC' : 'linear-gradient(135deg,#3B5BDB,#6C8CF5)', noteBtnFg: S.noteSaved ? '#16804A' : '#fff', saveNote: () => set({ noteSaved:true }),
      past: prevNotes.length ? { label: prevNotes[np].label, text: prevNotes[np].t } : { label:'이전 글', text:'아직 남긴 글이 없어요' },
      prevNote: () => np < prevNotes.length-1 && set({ np:np+1 }), nextNote: () => np > 0 && set({ np:np-1 }), pnO: np < prevNotes.length-1 ? '1' : '.35', nnO: np > 0 ? '1' : '.35',
      cumLabel: started ? (TODAY+1)+'일차까지 누적' : '누적 (출발 전 포함)', top: lgTop, wOpen: !!S.wIn, toggleW: () => set({ wIn: !S.wIn }), wInput: S.wInput ?? '', onW: O.onWInput, saveW: O.saveW
    };
""" + rv[LGb:]
# 기록 탭 위쪽 고정 숫자 → 실제 값
for a_, b_ in [('color:#1C7ED6;text-shadow:none">목표 89%</span>', 'color:#1C7ED6;text-shadow:none">목표 {{ lg.top.pct }}</span>'),
               ('line-height:1.1">17,820<span style="font-size:17px;font-weight:700"> 걸음</span></b>', 'line-height:1.1">{{ lg.top.steps }}<span style="font-size:17px;font-weight:700"> 걸음</span></b>'),
               ('<span style="display:block;height:100%;width:89%;border-radius:99px;background:#fff"></span>', '<span style="display:block;height:100%;width:{{ lg.top.pct }};border-radius:99px;background:#fff"></span>'),
               ('<span>목표 20,000</span><span>12일차까지 214,600걸음</span>', '<span>목표 20,000</span><span>{{ lg.top.cum }}</span>'),
               ('white-space:nowrap">112bpm</b>', 'white-space:nowrap">{{ lg.top.hr }}</b>'),
               ('white-space:nowrap">6.8시간</b>', 'white-space:nowrap">{{ lg.top.sleep }}</b>')]:
    dc = rep(a_, b_, src=dc)
dc = rep('<span>12일차까지 누적</span>', '<span>{{ lg.cumLabel }}</span>', src=dc)
for a_, b_ in [('<span style="font-size:14px;font-weight:700">시나가와 → 교토 · 12일째</span>', '<span style="font-size:14px;font-weight:700">{{ glHead }}</span>'),
               ('<span>1일</span><span>오늘 12일</span><span>31일</span>', '<span>1일</span><span>{{ glToday }}</span><span>31일</span>'),
               ('white-space:nowrap">걸은 날</span></span><b style="font-size:19px;font-weight:800;letter-spacing:-.03em;white-space:nowrap">11일</b>', 'white-space:nowrap">걸은 날</span></span><b style="font-size:19px;font-weight:800;letter-spacing:-.03em;white-space:nowrap">{{ jnStat.w }}</b>'),
               ('white-space:nowrap">남은 날</span></span><b style="font-size:19px;font-weight:800;letter-spacing:-.03em;white-space:nowrap">19일</b>', 'white-space:nowrap">남은 날</span></span><b style="font-size:19px;font-weight:800;letter-spacing:-.03em;white-space:nowrap">{{ jnStat.l }}</b>'),
               ('white-space:nowrap">휴식일</span></span><b style="font-size:19px;font-weight:800;letter-spacing:-.03em;white-space:nowrap">3일</b>', 'white-space:nowrap">휴식일</span></span><b style="font-size:19px;font-weight:800;letter-spacing:-.03em;white-space:nowrap">{{ jnStat.r }}</b>'),
               ('<span style="font-size:14px;font-weight:700">지금 · 오카베</span>', '<span style="font-size:14px;font-weight:700">{{ wxCard.place }}</span>'),
               ('font-size:30px;color:#FFE08A;">sunny</span>', 'font-size:30px;color:#FFE08A;">{{ wxCard.icon }}</span>'),
               ('line-height:1">18°</b>', 'line-height:1">{{ wxCard.t }}</b>'), ('<span style="font-size:14px;font-weight:700">맑음 · 체감 17° · 바람 2m/s · 습도 52%</span>', '<span style="font-size:14px;font-weight:700">{{ wxCard.desc }}</span>'),
               ('<span style="font-size:12px;color:#6B7A90">100엔 = 905원 · 예시</span>', '<span style="font-size:12px;color:#6B7A90">{{ fxLabel }}</span>')]:
    dc = rep(a_, b_, src=dc)
# 사진 일기: 기존 사진 칸(day-N-photo-1, 이 기기 저장)을 카드 사진 자리에 표시, 오늘 카드에서는 눌러서 추가
_g = dc.index('aspect-ratio:4/3;background:{{ d.grad }}">'); _ge = dc.index('{{ d.icon }}</span>', _g) + len('{{ d.icon }}</span>')
dc = dc[:_ge] + '<span onClick="{{ d.stopIf }}" style="position:absolute;inset:0;display:block"><image-slot class="{{ d.slotCls }}" id="day-{{ d.n }}-photo-1" shape="rect" placeholder="사진 추가" style="position:absolute;inset:0;width:100%;height:100%"></image-slot></span>' + dc[_ge:]
# 체중: 눌러서 입력 (숫자만 누르면 소수점 자동)
WT = '<span style="border-radius:20px;background:rgba(255,255,255,.55);border:1px solid rgba(255,255,255,.85);backdrop-filter:blur(22px) saturate(1.4);-webkit-backdrop-filter:blur(22px) saturate(1.4);box-shadow:0 8px 24px rgba(40,50,140,.08);padding:12px;display:flex;flex-direction:column;gap:6px;min-width:0"><span style="display:flex;align-items:center;gap:6px"><span style="width:28px;height:28px;border-radius:9px;background:linear-gradient(135deg,#1C7ED6,#4DABF7)'
_wi = dc.index('white-space:nowrap">{{ lg.top.sleep }}</b></span>') ; _wj = dc.index('<span style="border-radius:20px;', _wi)
dc = dc[:_wj] + '<span onClick="{{ lg.toggleW }}" style="cursor:pointer;border-radius:20px;' + dc[_wj + len('<span style="border-radius:20px;'):]
W2 = 'white-space:nowrap">76.2kg</b></span>\n</div>'
dc = rep(W2, 'white-space:nowrap">{{ lg.top.w }}</b></span>\n</div>\n<sc-if value="{{ lg.wOpen }}" hint-placeholder-val="{{ false }}"><div style="display:flex;gap:8px"><input type="text" inputmode="numeric" pattern="[0-9]*" value="{{ lg.wInput }}" onChange="{{ lg.onW }}" placeholder="예: 762 → 76.2kg" style="flex:1;min-width:0;height:48px;border-radius:16px;border:1px solid rgba(255,255,255,.95);background:rgba(255,255,255,.8);padding:0 16px;font:700 17px Pretendard,sans-serif;outline:none"><button onClick="{{ lg.saveW }}" style="flex:none;height:48px;padding:0 18px;border-radius:99px;border:0;background:linear-gradient(135deg,#3B5BDB,#6C8CF5);color:#fff;font:800 15px Pretendard,sans-serif">저장</button></div></sc-if><div style="border-radius:24px;padding:16px;background:rgba(255,255,255,.55);border:1px solid rgba(255,255,255,.85);backdrop-filter:blur(22px) saturate(1.4);-webkit-backdrop-filter:blur(22px) saturate(1.4);box-shadow:0 8px 24px rgba(40,50,140,.08);display:flex;flex-direction:column;gap:12px;min-width:0"><span style="display:flex;align-items:center;justify-content:space-between;gap:8px"><b style="font-size:18px;font-weight:800;letter-spacing:-.03em;white-space:nowrap">하루 기록</b><span style="display:flex;align-items:center;gap:6px"><button onClick="{{ rec.prev }}" style="width:40px;height:40px;border-radius:50%;border:1px solid rgba(255,255,255,.95);background:rgba(255,255,255,.8);display:grid;place-items:center;opacity:{{ rec.pO }}"><span style=\"font-family:\'Material Symbols Rounded\';font-weight:normal;font-style:normal;line-height:1;letter-spacing:normal;text-transform:none;white-space:nowrap;direction:ltr;-webkit-font-smoothing:antialiased;font-feature-settings:\'liga\';font-variation-settings:\'FILL\' 1,\'wght\' 500;font-size:20px;color:#3B5BDB;\">chevron_left</span></button><b style="font-size:14px;white-space:nowrap">{{ rec.label }}</b><button onClick="{{ rec.next }}" style="width:40px;height:40px;border-radius:50%;border:1px solid rgba(255,255,255,.95);background:rgba(255,255,255,.8);display:grid;place-items:center;opacity:{{ rec.nO }}"><span style=\"font-family:\'Material Symbols Rounded\';font-weight:normal;font-style:normal;line-height:1;letter-spacing:normal;text-transform:none;white-space:nowrap;direction:ltr;-webkit-font-smoothing:antialiased;font-feature-settings:\'liga\';font-variation-settings:\'FILL\' 1,\'wght\' 500;font-size:20px;color:#3B5BDB;\">chevron_right</span></button></span></span><div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px"><sc-for list="{{ rec.facts }}" as="x" hint-placeholder-count="3"><span style="border-radius:16px;background:rgba(255,255,255,.65);padding:10px 12px;display:flex;flex-direction:column;gap:4px;min-width:0"><span style="font-size:12px;color:#4A5D78;white-space:nowrap">{{ x.k }}</span><b style="font-size:18px;font-weight:800;letter-spacing:-.03em;white-space:nowrap">{{ x.v }}</b></span></sc-for></div><span style="font-size:14px;font-weight:800">걸은 길</span><div style="position:relative;height:240px;border-radius:16px;overflow:hidden;background:#E8EBF7"><div data-v8map="log" data-k="{{ rec.key }}" style="position:absolute;inset:0;z-index:0"></div></div><span style="font-size:12px;color:#6B7A90">{{ rec.mapNote }}</span><span style="display:flex;justify-content:space-between;align-items:baseline"><span style="font-size:14px;font-weight:800">시간대별 걸음</span><span style="font-size:12px;color:#6B7A90">{{ rec.hourNote }}</span></span><div data-hscroll="1" style="overflow-x:auto;scrollbar-width:none;margin:0 -4px"><div style="display:flex;align-items:flex-end;gap:6px;height:130px;min-width:640px;padding:0 4px"><sc-for list="{{ rec.bars }}" as="b" hint-placeholder-count="18"><span style="flex:1;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;gap:3px;height:100%"><span style="font-size:11px;font-weight:700;color:#1C7ED6;white-space:nowrap">{{ b.v }}</span><i style="width:100%;height:{{ b.h }};border-radius:6px 6px 2px 2px;background:{{ b.c }}"></i><span style="font-size:11px;color:#6B7A90">{{ b.l }}</span></span></sc-for></div></div></div>', src=dc)
# ───── 지도·일본어·더보기(한눈에·사진 일기·전체 여정·일정 관리·역참 스탬프·여행 정보) ─────
def cut(a, b):
    global rv
    i = rv.index(a); j = rv.index(b, i)
    return i, j
# 일본어: 엑셀 문장(★필수 먼저)
i, j = cut('    const PH = ', '    const plist')
rv = rv[:i] + "    const PHD = { '필수': PH.filter(p => p[4]).map(p => [p[3], p[1], p[2]]) }; PH.forEach(p => (PHD[p[0]] = PHD[p[0]] || []).push([p[3], p[1], p[2]]));\n" + rv[j:]
rv = rep("const plist = PH[S.jc],", "const JC = PHD[S.jc] ? S.jc : '필수', plist = PHD[JC],", src=rv)
rv = rep("cats: Object.keys(PH).map(c => ({ label:c, ...chipOf(S.jc===c),", "cats: Object.keys(PHD).map(c => ({ label: c==='필수' ? '★ 필수' : c, ...chipOf(JC===c),", src=rv)
# 지도: 실제 편의시설(경로 주변 400m, 기존 수집 로직)
i, j = cut('    const mf = S.mf;', '    // log')
rv = rv[:i] + r"""    const mf = S.mf;
    const AM = (this.amenCache || {})[VW+1] || null, AK = { cvs:'conv', wc:'wc', st:'sta', ph:'ph' };
    const FC = [['cvs','편','편의점','#3B5BDB'],['wc','화','화장실','#1C7ED6'],['st','역','역','#7048E8'],['ph','약','약국','#C2255C']];
    const meLL = (window.__v8 && window.__v8.me) || (X.dd.stops[0] && X.dd.stops[0].ll), dk = ll => hav(meLL, ll);
    const amenOn = FC.filter(f => mf[f[0]]).flatMap(([k,lt,label,c]) => ((AM && AM[AK[k]]) || []).map(a => ({ k, lt, label, c, ll:a.ll, name:a.name, d: dk(a.ll) })));
    const mp = { mk: [], facPins: [], routeO: mf.route ? '1' : '.35', count: AM ? String(amenOn.length) : '—',
      chips: [['route','경','경로','#3B5BDB'], ...FC].map(([k,lt,label,c]) => { const on = !!mf[k]; return { lt, label, n: k==='route' ? '' : (AM ? String(((AM[AK[k]])||[]).length) : '—'), bg: on ? 'rgba(255,255,255,.95)' : 'rgba(255,255,255,.6)', bd: on ? c : 'rgba(255,255,255,.95)', fg: on ? '#18324F' : '#6B7A90', lb: on ? c : 'rgba(24,50,79,.12)', lf: on ? '#fff' : '#6B7A90', nf: on ? c : '#8C96C2', pick: () => set({ mf:{...mf,[k]:!mf[k]} }) }; }),
      list: amenOn.sort((a,b) => a.d - b.d).slice(0, 8).map((a,i) => ({ name: a.name, kind: a.label, km: a.d < 1 ? Math.round(a.d*1000)+'m' : a.d.toFixed(1)+'km', icon: a.k==='cvs'?'local_convenience_store':a.k==='wc'?'wc':a.k==='st'?'train':'local_pharmacy', bg:a.c, top: i ? '1px solid rgba(24,50,79,.08)' : '0', map:'https://www.google.com/maps/dir/?api=1&travelmode=walking&destination='+a.ll[0]+','+a.ll[1] })),
      dir: 'https://www.google.com/maps/dir/?api=1&travelmode=walking&destination='+encodeURIComponent(JP[D.e-1]) };
""" + rv[j:]
# 더보기 메뉴 설명 문구: 실제 값
rv = rep("'31일 · 37% 완주'", "'31일 · '+Math.round(Math.min(100, X.posKmF/487.7*100))+'% 완주'", src=rv)
rv = rep("'숙소 확정 17 / 31'", "'숙소 확정 '+Object.values(HT).filter(h => h && h.ko).length+' / 31'", src=rv)
rv = rep("'20 / 53 역참'", "STN+' / 53 역참'", src=rv)
rv = rep("{icon:'watch',label:'Galaxy Watch9',v:'연결됨',bg:'#E4F8EC',fg:'#16804A',pick:()=>{}},{icon:'my_location',label:'위치 기록 (OwnTracks)',v:'켜짐',bg:'#E4F8EC',fg:'#16804A',pick:()=>{}}",
         "{icon:'watch',label:'Galaxy Watch9',v:(S.hc && S.hc.at && !S.hc.err) ? '동기화됨' : '확인 중',bg:(S.hc && !S.hc.err) ? '#E4F8EC' : '#FFF3D8',fg:(S.hc && !S.hc.err) ? '#16804A' : '#8A5A0E',pick:()=>this.loadHc()},{icon:'my_location',label:'위치 기록 (OwnTracks)',v:(() => { const L = (S.hc && S.hc.locs) || {}, ks = Object.keys(L).sort(), a = ks.length ? L[ks[ks.length-1]] : null, t = a && a.length ? a[a.length-1][2] : 0; if (!t) return '기록 없음'; const d = new Date(t*1000); return '마지막 '+(d.getMonth()+1)+'/'+d.getDate()+' '+String(d.getHours()).padStart(2,'0')+':'+String(d.getMinutes()).padStart(2,'0'); })(),bg:'rgba(24,50,79,.06)',fg:'#4A5D78',pick:()=>{}}", src=rv)
# 전체 여정·사진 일기에서 날짜 누르면 그 날의 오늘 화면으로
rv = rep("open: () => set({ sub:null, t:'home', view:d.i, sheet:null }) }; }) };", "open: () => { this.goView(d.i+1); set({ sub:null, t:'home', sheet:null }); } }; }) };", src=rv)
rv = rep("open: () => has ? set({ sub:null, t:'home', view:d.i, sheet:null }) : set({ sub:null })", "open: () => { if (has) { this.goView(d.i+1); set({ sub:null, t:'home', sheet:null }); } else set({ sub:null, t:'log' }); }", src=rv)
# 일정 관리: 기존 일정 변경값(mg)에 저장
i, j = cut('    const pd = day(S.pd),', '    const pl = {')
rv = rv[:i] + "    const MG = S.mg || {}, PDi = S.pd != null ? S.pd : VW, pd = day(PDi), PE = Object.fromEntries(Object.entries(MG.ends || {}).map(([d,b]) => [+d-1, b+1])), LF = MG.lf || {}, pEnd = PE[PDi] ?? pd.e, pkm = +(KM[pEnd-1]-KM[pd.s-1]).toFixed(1), lfd = LF[PDi] || {};\n    const hcf = HT[pd.n] || HT[String(pd.n)], conf = !!(hcf && hcf.ko);\n" + rv[j:]
for a_, b_ in [("const on = d.i === S.pd, ch = S.pe[d.i] != null && S.pe[d.i] !== d.e;", "const on = d.i === PDi, ch = PE[d.i] != null && PE[d.i] !== day(d.i).e && false;"),
               ("pick: () => set({ pd:d.i, planSaved:false }) }; }),", "pick: () => set({ pd:d.i, planSaved:false }) }; }),"),
               ("pick: () => set({ pe:{...S.pe,[S.pd]:n}, planSaved:false }) }; }),", "pick: () => set({ mg:{...MG, ends:{...(MG.ends||{}), [PDi+1]: n-1}}, planSaved:false }) }; }),"),
               ("fields: [['name','숙소 이름',conf?KO[pEnd-1]+' 역 앞 비즈니스호텔':'','숙소 이름'],['price','1박 요금 (엔)',conf?'7,800':'','0'],['in','체크인',conf?'15:00':'','15:00']].map(([k,label,def,ph]) => ({ k:label, ph, v: lfd[k] ?? def, on: e => set({ lf:{...S.lf,[S.pd]:{...lfd,[k]:",
                "fields: [['name','숙소 이름',conf?hcf.ko:'','숙소 이름'],['price','1박 요금 (엔)','','0'],['in','체크인','','15:00']].map(([k,label,def,ph]) => ({ k:label, ph, v: lfd[k] ?? def, on: e => set({ mg:{...MG, lf:{...LF,[PDi]:{...lfd,[k]:"),
               ("search: qmap(JP[pEnd-1]+' ホテル'), sumKm:'488km', over: allDays.filter(d => d.dist - d.tr > 30).length+'일', conf:'17 / 31',",
                "search: qmap(JP[pEnd-1]+' ホテル'), sumKm: Math.round(KM[53])+'km', over: allDays.filter(d => d.dist - d.tr > 30).length+'일', conf: Object.values(HT).filter(h => h && h.ko).length+' / 31',"),
               ("reset: () => set({ pe:{}, lf:{}, planSaved:false }) };", "reset: () => set({ mg:{}, planSaved:false }) };")]:
    rv = rep(a_, b_, src=rv)
rv = rv.replace("e.target.value}}, planSaved:false }) })),", "e.target.value}}}, planSaved:false }) })),", 1)
# 역참 스탬프: 기존 방문 기록(smode: 걸어서/교통/해제)
i, j = cut('    const sts = S.stamps,', '    const stp = {')
rv = rv[:i] + "    const SM = S.smode || {}, tStart = this.dayInfo().diff >= 0 ? dayData(X.today).startKm : -1, MOD = k => SM[k] ?? (KM[k] <= tStart + .01 ? 'w' : 'n'), sts = Array.from({length:53},(x,k) => ({w:1,t:2,n:0})[MOD(k)]), walkN = sts.filter(x=>x===1).length, trN = sts.filter(x=>x===2).length;\n    const BGS = (O.badges || []);\n" + rv[j:]
rv = rep("badgeN: '5 / 15',", "badgeN: BGS.filter(x => x.c === '#8A5A12').length+' / '+BGS.length,", src=rv)
rv = rep("pick: () => { const n = sts.slice(); n[k] = (n[k]+1)%3; set({ stamps:n }); } })),", "pick: () => { const cur = MOD(k); set({ smode:{...SM,[k]: cur==='n' ? 'w' : cur==='w' ? 't' : 'n'} }); } })),", src=rv)
i, j = cut("      badges: BD.map(", "\n")
rv = rv[:i] + "      badges: BGS.map(g => { const ok = g.c === '#8A5A12', hide = g.t === '???'; return { icon: hide ? 'lock' : ok ? 'military_tech' : 'flag', t: g.t, s: ok ? g.s : hide ? '시크릿' : '도전 중', o: ok ? '1' : '.6', bg: ok ? 'rgba(255,255,255,.85)' : 'rgba(255,255,255,.45)', bd: ok ? '#E0D7FB' : 'rgba(255,255,255,.9)', ib: ok ? 'linear-gradient(135deg,#7048E8,#9775FA)' : 'rgba(24,50,79,.08)', if: ok ? '#fff' : '#8C96C2' }; }) };" + rv[j:]
# 여행 정보: 실제 날씨(7일)·환율
i, j = cut("    const wx = [['화',", "\n")
rv = rv[:i] + "    const WL = S.wlive && S.wlive.d, WIC = c => c <= 1 ? 'sunny' : c <= 3 ? 'partly_cloudy_day' : c >= 51 && c <= 82 ? 'rainy' : 'cloud';\n    const wx = WL ? WL.time.slice(0,7).map((t,k) => { const icon = WIC(WL.weather_code[k]), rain = (WL.precipitation_probability_max[k] ?? 0)+'%'; return { name: k===0 ? '오늘' : WD[new Date(t+'T00:00:00').getDay()], icon, hi: Math.round(WL.temperature_2m_max[k]), lo: Math.round(WL.temperature_2m_min[k]), rain, bg: k===0 ? 'rgba(91,111,212,.12)' : 'transparent', ic: icon==='sunny' ? '#E0861A' : icon==='rainy' ? '#1C7ED6' : '#8C96C2', rc: parseInt(rain) >= 50 ? '#1C7ED6' : '#6B7A90' }; }) : [];" + rv[j:]
rv = rep("const fv = Number(dig(S.fxv)) || 0, jk = S.nfxDir === 'jk';", "const fv = Number(dig(S.fxv)) || 0, jk = (S.nfxDir || 'jk') === 'jk';", src=rv)
i, j = cut("    const wxd = [", "\n")
rv = rv[:i] + "    const hm = t => t ? t.slice(11,16) : '—';\n    const wxd = [{icon:'wb_twilight',k:'일출',v:WL ? hm(WL.sunrise[0]) : '—',c:'#E0861A'},{icon:'bedtime',k:'일몰',v:WL ? hm(WL.sunset[0]) : '—',c:'#7048E8'},{icon:'thermostat',k:'지금',v:S.wlive && S.wlive.now != null ? Math.round(S.wlive.now)+'°' : '—',c:'#E0861A'},{icon:'umbrella',k:'오늘 강수',v:WL ? (WL.precipitation_probability_max[0] ?? 0)+'%' : '—',c:'#1C7ED6'}];" + rv[j:]
# 사진 일기: 실제 하루 글
rv = rep("note: has ? '“'+DN[d.i]+'”' : '오늘 사진과 한 줄을 남겨 보세요'", "note: (S.noteLog||{})[isoOf(new Date(2026,11,4+d.i))] ? '“'+(S.noteLog||{})[isoOf(new Date(2026,11,4+d.i))]+'”' : has ? '남긴 글 없음' : '오늘 사진과 한 줄을 남겨 보세요'", src=rv)
rv = rep("cnt: has ? ((d.i%3)+1)+'장' : '', cntD: has ? 'block' : 'none'", "cnt: '', cntD: 'none', slotCls: d.i === TODAY && this.dayInfo().diff >= 0 ? '' : 'ro', stopIf: d.i === TODAY && this.dayInfo().diff >= 0 ? (e => e.stopPropagation()) : null", src=rv)
rv = rep("const diary = Array.from({length:TODAY+1},(x,k)=>day(TODAY-k))", "const diary = Array.from({length:Math.max(1, Math.min(31, this.dayInfo().diff+1))},(x,k)=>day(Math.max(0, Math.min(30, this.dayInfo().diff))-k))", src=rv)
# 한눈에: 실제 누적
i, j = cut("        return { stats:[{k:'걸음',v:'214,600'", "\n")
rv = rv[:i] + "        const sd = Object.entries((S.hc && S.hc.days) || {}).filter(([k]) => k >= '2026-12-04'), stp_ = sd.reduce((q,[k,v]) => q+(+v.steps||0), 0), mn_ = sd.reduce((q,[k,v]) => q+(+v.min||0), 0), nd = Math.max(1, sd.length), EL2 = S.expLog || {}, ew = Object.entries(EL2).filter(([k]) => k >= '2026-12-04').reduce((q,[k,a]) => q + a.reduce((r,e) => r + (e.c==='jpy' ? e.v*(((S.fxAuto && S.fxAuto.r) || 905)/100) : e.v), 0), 0), bOk = (O.badges||[]).filter(x => x.c === '#8A5A12').length;\n        return { stats:[{k:'걸음',v:f1(stp_),s:'하루 평균 '+f1(Math.round(stp_/nd))},{k:'걸은 시간',v:Math.floor(mn_/60)+':'+String(mn_%60).padStart(2,'0'),s:'하루 평균 '+Math.floor(mn_/nd/60)+':'+String(Math.round(mn_/nd%60)).padStart(2,'0')},{k:'지출',v:'₩'+fmt(ew),s:'하루 평균 ₩'+fmt(ew/nd)},{k:'배지',v:bOk+' / '+(O.badges||[]).length,s:''}]," + rv[j:]
rv = rep("photos: [10,9,8,7,6,5].map((n,k) => ({ n,", "photos: [].map((n,k) => ({ n,", src=rv)
# 표지(커버 화면)·남은 거리
rv = rep("const STN_ = 0;", "", src=rv) if "const STN_ = 0;" in rv else rv
rv = rep("    // more\n", "    // more\n    const STN = X.stationsDone;\n", src=rv)
rv = rep(".map(([k,icon,label,sub,grad,glow]) => ({ icon,label,sub,grad,glow, open: () => set({ sub:k }) })),", ".map(([k,icon,label,sub,grad,glow]) => ({ icon,label,sub,grad,glow, ...(PV[k] || {}), open: () => set({ sub:k }) })),", src=rv)
rv = rep("    const STN = X.stationsDone;\n", """    const STN = X.stationsDone;
    const _kmT = X.posKmF, _pc = Math.min(100, _kmT/487.7*100), _NL = S.noteLog || {}, _nk = Object.keys(_NL).filter(k => _NL[k]).sort(), _hd = HCD, _sd = Object.keys(_hd).filter(k => k >= '2026-12-04'), _stp = _sd.reduce((q,k) => q+(+_hd[k].steps||0), 0);
    const _nx = day(Math.min(30, Math.max(0, TODAY + (_df < 0 ? 0 : 1)))), _w = S.wlive, _r100 = Math.round((((S.fxAuto && S.fxAuto.r) || 905)));
    const PV = {
      glance: { big: _kmT.toFixed(1)+'km', pct: _pc+'%', barD:'block', line: _df < 0 ? '출발 전 · 31일 488km' : '누적 '+f1(_stp)+'걸음 · '+STN+'/53 역참' },
      diary: { big: _nk.length+'일', pct:'0%', barD:'none', line: _nk.length ? '“'+_NL[_nk[_nk.length-1]]+'”' : '아직 남긴 글이 없어요' },
      journey: { big: Math.round(_pc)+'%', pct: _pc+'%', barD:'block', line: _df < 0 ? '12/4 시나가와 출발 · D-'+(-_df) : (TODAY+1)+'일차 · '+D.path },
      plan: { big: _nx.rest ? '휴식' : _nx.dist+'km', pct:'0%', barD:'none', line: (_df < 0 ? '1일차 · ' : '내일 · ')+_nx.path },
      stamp: { big: STN+' / 53', pct: (STN/53*100)+'%', barD:'block', line: STN ? '다음 역참 · '+(KO[Math.min(52, STN)] || '') : '첫 도장 · 시나가와' },
      info: { big: _w && _w.now != null ? Math.round(_w.now)+'°' : '—', pct:'0%', barD:'none', line: '100엔 = '+_r100+'원' + (_w && _w.d && _w.d.precipitation_probability_max ? ' · 강수 '+_w.d.precipitation_probability_max[0]+'%' : '') }
    };
""", src=rv)
# 마지막으로 보던 화면 전환(t, sheet 등)은 기존 상태와 겹치지 않음. 오늘 날짜(ISO)도 꺼내 줌
OLD = rep("today, view, places },", "today, view, places, hcH, hcR, recLabel, recIso, iso: (() => { const q = new Date(); return q.getFullYear()+'-'+String(q.getMonth()+1).padStart(2,'0')+'-'+String(q.getDate()).padStart(2,'0'); })() },", src=OLD)
OLD = rep("  state = { theme: null,", "  state = { ...this.nInit(), theme: null,", src=OLD)
# 기존 클래스 끝에 새 메서드 추가
ce = OLD.rindex('}')
METH = '''
  closeSheet() { if (this.state.closing || !this.state.sheet) return; this.setState({ closing: 'sheet' }); clearTimeout(this._ct); this._ct = setTimeout(() => this.setState({ sheet: null, closing: null }), 220); }
  closeSub() { if (this.state.closing || !this.state.sub) return; this.setState({ closing: 'sub' }); clearTimeout(this._ct); this._ct = setTimeout(() => this.setState({ sub: null, closing: null }), 220); }
  hwBack() { const s = this.state; if (s.sheet) this.closeSheet(); else if (s.sub) this.closeSub(); else if (s.t && s.t !== 'home') this.setState({ t: 'home' }); }
'''
OLD = OLD[:ce] + '\n' + st + '\n' + METH + rv.rstrip() + '\n' + OLD[ce:]
# 폰 뒤로 가기(제스처·버튼): 팝업 → 하위 화면 → 오늘 탭 순으로 닫음
OLD = rep("  componentDidMount() {", "  componentDidMount() { try { window.addEventListener('popstate', () => this.hwBack()); } catch (e) {}", src=OLD)

# 숙소 목록(HOTELS)을 전역으로
_hi = old.index('var HOTELS = ') + len('var HOTELS = ')
_ho, _hend = json.JSONDecoder().raw_decode(old[_hi:])
HOTELS = json.dumps(_ho, ensure_ascii=False)
na = dc.index('<script type="text/x-dc"'); nb = dc.index('>', na) + 1; ne = dc.index('</script>', nb)
dc = dc[:nb] + '\nwindow.TK_HOTELS = ' + HOTELS + ';\n' + OLD + dc[ne:]

# ───────────────────────── 4. 지도(Leaflet) + 기존 보조 기능 ─────────────────────────
MAP_JS = r"""<script>(function () {
  var TILE = 'https://tile.openstreetmap.org/{z}/{x}/{y}.png';
  function pin(t, bg, fg, bd, s) { return '<div style="transform:translate(-50%,-100%);display:grid;place-items:center;width:' + s + 'px;height:' + s + 'px;border-radius:50% 50% 50% 0;rotate:-45deg;background:' + bg + ';border:2px solid ' + bd + ';box-shadow:0 4px 10px rgba(24,50,79,.3)"><b style="rotate:45deg;font:800 12px Pretendard,sans-serif;color:' + fg + '">' + t + '</b></div>'; }
  setInterval(function () {
    if (!window.L || !window.__v8) return;
    document.querySelectorAll('[data-v8map]').forEach(function (el) {
      var D = window.__v8, k = el.getAttribute('data-k') + '|' + (D.trk || '').length + '|' + (D.amen || '').length + '|' + (D.logTrk || '').length;
      if (!el._map) { try { el._map = L.map(el, { zoomControl: false, attributionControl: false, scrollWheelZoom: false }); L.tileLayer(TILE, { maxZoom: 18 }).addTo(el._map); el._lay = L.layerGroup().addTo(el._map); } catch (e) { return; } }
      if (el._k === k && el._w === el.clientWidth) return; el._k = k; el._w = el.clientWidth; el._lay.clearLayers();
      try { el._map.invalidateSize(); } catch (e) {}
      if (el.getAttribute('data-v8map') === 'log') { var lt = D.logTrk || []; if (lt.length > 1 && window.tkSeg) window.tkSeg(lt).forEach(function (r) { L.polyline(r.pts, r.m === 'v' ? { color: '#F08A24', weight: 6, dashArray: '2 9', lineCap: 'round' } : { color: '#673DE6', weight: 5 }).addTo(el._lay); });
        if (lt.length) { L.circleMarker(lt[0], { radius: 7, color: '#fff', weight: 3, fillColor: '#20A85A', fillOpacity: 1 }).addTo(el._lay); L.circleMarker(lt[lt.length - 1], { radius: 8, color: '#fff', weight: 3, fillColor: '#E8453C', fillOpacity: 1 }).addTo(el._lay); try { el._map.fitBounds(L.latLngBounds(lt.map(function (q) { return [q[0], q[1]]; })), { padding: [24, 24], maxZoom: 16 }); } catch (e) {} } else { try { el._map.setView((D.me || (D.stops && D.stops[0] && D.stops[0].ll) || [35.62, 139.74]), 13); } catch (e) {} }
        return; }
      var pts = D.route || []; if (pts.length > 1) { L.polyline(pts, { color: '#fff', weight: 10, opacity: .9 }).addTo(el._lay); L.polyline(pts, { color: '#3B5BDB', weight: 6, opacity: .95 }).addTo(el._lay); }
      var tr = D.trk || []; if (tr.length > 1 && window.tkSeg) window.tkSeg(tr).forEach(function (r) { L.polyline(r.pts, r.m === 'v' ? { color: '#F08A24', weight: 5, dashArray: '2 9', lineCap: 'round' } : { color: '#7048E8', weight: 5 }).addTo(el._lay); });
      (D.stops || []).forEach(function (s, i, a) { var st = i === 0, en = i === a.length - 1; L.marker(s.ll, { icon: L.divIcon({ className: '', iconSize: [0, 0], html: pin(st ? 'A' : en ? 'B' : String(i), st ? '#18324F' : en ? '#7048E8' : s.past ? '#3B5BDB' : '#fff', st || en || s.past ? '#fff' : '#3B5BDB', st || en ? '#fff' : '#3B5BDB', st || en ? 30 : 24) }), zIndexOffset: st || en ? 300 : 200 }).addTo(el._lay); });
      (D.amen || []).forEach(function (a) { L.marker(a.ll, { icon: L.divIcon({ className: '', iconSize: [0, 0], html: '<div style="transform:translate(-50%,-50%);width:22px;height:22px;border-radius:50%;background:' + a.c + ';border:2px solid #fff;display:grid;place-items:center;font:800 11px Pretendard,sans-serif;color:#fff;box-shadow:0 2px 6px rgba(0,0,0,.25)">' + a.lt + '</div>' }) }).addTo(el._lay); });
      if (D.me) L.circleMarker(D.me, { radius: 8, color: '#fff', weight: 3, fillColor: '#2F7CF6', fillOpacity: 1 }).addTo(el._lay);
      var b = (D.stops || []).map(function (s) { return s.ll; }).concat(pts); if (b.length) try { el._map.fitBounds(L.latLngBounds(b), { padding: [24, 24], maxZoom: 15 }); } catch (e) {}
    });
  }, 600);
})();</script>"""

# 기존 보조 스크립트 중 데이터·기능에 해당하는 것만 가져옴
def old_script(marker):
    i = old.index(marker); a = old.rindex('<script>', 0, i); e = old.index('</script>', i) + 9
    return old[a:e]
KEEP = [
    old_script("var URL_ = 'https://jmfvsusybouibqmdvtmy.supabase.co/functions/v1/tk-sync'"),  # 저장값 클라우드 백업/복원
    old_script('/* 위에서 아래로 당기면 새로고침'),                                             # 당겨서 새로고침
    old_script('window.tkSeg = function (pts)'),                                                   # 걸음/차량 구간 나누기
]
# 전체 화면 자동·뒤로가기 보호·가로 흔들림 잠금 (새 화면의 가로 넘기기 목록은 허용)
FS = old_script("var fsBtn = document.getElementById('fsBtn')")
FS = FS.replace("  fsBtn.addEventListener('click',", "  fsBtn && fsBtn.addEventListener('click',", 1)
_c = "if (dx > dy && !(e.target.closest && e.target.closest('.leaflet-container,input,textarea,[data-hscroll]'))) e.preventDefault();"
assert FS.count(_c) == 1
FS = FS.replace(_c, "if (dx > dy && !(e.target.closest && e.target.closest('.leaflet-container,input,textarea,[data-hscroll]')) && !(function (n) { for (; n && n !== document.body; n = n.parentElement) { if (n.scrollWidth > n.clientWidth + 2) { var o = getComputedStyle(n).overflowX; if (o === 'auto' || o === 'scroll') return true; } } return false; })(e.target)) e.preventDefault();")
KEEP.append(FS)
dc = dc.replace('</body>', MAP_JS + ''.join(KEEP) + '</body>', 1)

os.makedirs(OUT, exist_ok=True)
open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(dc)
for f in ('support.js',):
    shutil.copy(os.path.join(ROOT, 'design', 'v8', f), os.path.join(OUT, f))
shutil.copy(os.path.join(ROOT, 'image-slot.js'), os.path.join(OUT, 'image-slot.js'))
print('wrote', os.path.relpath(OUT, ROOT) + '/index.html', len(dc))
