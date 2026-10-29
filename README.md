# tokaido-walk
## 수정하는 법
- 일정 원본: `data/schedule.xlsx`
- 사이트 다시 만들기: `python3 build/build.py data/schedule.xlsx _` (openpyxl 필요, 두 번째 값은 쓰지 않지만 자리만 채움)
  - `index.html`, `today.html` — 새 디자인 (메인 · 오늘의 여정, 같은 내용)
  - `old_home.html` `old_today.html` `old_plan.html` `old_records.html` `old_itinerary.html` `old_japanese.html` `old_guide.html` — 예전 디자인 그대로, 탭만 다르게 열림
- 커밋해서 main에 올리면 Vercel이 자동 배포합니다. `vercel.json`의 `cleanUrls`로 `/old_records` 처럼 `.html` 없이 주소가 열립니다.
- 새 디자인(메인/오늘)은 `build/template_main.html`에서 고칩니다. 예전 디자인은 지금까지처럼 `build/template.html`.
- `/plan` `/records` `/itinerary` `/map` `/stations` `/japanese` `/guide` 는 아직 새 디자인이 없어 만들지 않았습니다. 그동안은 새 메인 화면 하단 메뉴가 해당 `/old_*` 화면으로 연결됩니다.

## 삼성 헬스 연동 (HC Webhook → Supabase → 사이트)
- 받는 주소: `https://jmfvsusybouibqmdvtmy.supabase.co/functions/v1/hc-webhook` (헤더 `x-api-key`)
- 읽는 주소: `.../functions/v1/hc-read?from=YYYY-MM-DD&to=YYYY-MM-DD` (헤더 `x-read-key`)
- 열쇠 값은 Supabase `hc_config` 표에만 있음(저장소에 없음). 사이트는 `/#k=읽기열쇠`로 한 번 열면 폰에 기억.
- 함수 코드: `supabase/functions/`
