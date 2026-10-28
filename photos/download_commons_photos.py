#!/usr/bin/env python3
"""Fetch freely licensed photo candidates for every station listed in the Tokaido route."""
import json, re, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets" / "stations"
ASSETS.mkdir(parents=True, exist_ok=True)
STATIONS = [
  {
    "n": 1,
    "ja": "日本橋",
    "en": "Nihonbashi"
  },
  {
    "n": 2,
    "ja": "品川",
    "en": "Shinagawa"
  },
  {
    "n": 3,
    "ja": "川崎",
    "en": "Kawasaki"
  },
  {
    "n": 4,
    "ja": "神奈川",
    "en": "Kanagawa"
  },
  {
    "n": 5,
    "ja": "程ヶ谷",
    "en": "Hodogaya"
  },
  {
    "n": 6,
    "ja": "戸塚",
    "en": "Totsuka"
  },
  {
    "n": 7,
    "ja": "藤沢",
    "en": "Fujisawa"
  },
  {
    "n": 8,
    "ja": "平塚",
    "en": "Hiratsuka"
  },
  {
    "n": 9,
    "ja": "大磯",
    "en": "Oiso"
  },
  {
    "n": 10,
    "ja": "小田原",
    "en": "Odawara"
  },
  {
    "n": 11,
    "ja": "箱根",
    "en": "Hakone"
  },
  {
    "n": 12,
    "ja": "三島",
    "en": "Mishima"
  },
  {
    "n": 13,
    "ja": "沼津",
    "en": "Numazu"
  },
  {
    "n": 14,
    "ja": "原",
    "en": "Hara"
  },
  {
    "n": 15,
    "ja": "吉原",
    "en": "Yoshiwara"
  },
  {
    "n": 16,
    "ja": "蒲原",
    "en": "Kambara"
  },
  {
    "n": 17,
    "ja": "由比",
    "en": "Yui"
  },
  {
    "n": 18,
    "ja": "興津",
    "en": "Okitsu"
  },
  {
    "n": 19,
    "ja": "江尻",
    "en": "Ejiri"
  },
  {
    "n": 20,
    "ja": "府中",
    "en": "Fuchu"
  },
  {
    "n": 21,
    "ja": "鞠子",
    "en": "Mariko"
  },
  {
    "n": 22,
    "ja": "岡部",
    "en": "Okabe"
  },
  {
    "n": 23,
    "ja": "藤枝",
    "en": "Fujieda"
  },
  {
    "n": 24,
    "ja": "島田",
    "en": "Shimada"
  },
  {
    "n": 25,
    "ja": "金谷",
    "en": "Kanaya"
  },
  {
    "n": 26,
    "ja": "日坂",
    "en": "Nissaka"
  },
  {
    "n": 27,
    "ja": "掛川",
    "en": "Kakegawa"
  },
  {
    "n": 28,
    "ja": "袋井",
    "en": "Fukuroi"
  },
  {
    "n": 29,
    "ja": "見附",
    "en": "Mitsuke"
  },
  {
    "n": 30,
    "ja": "浜松",
    "en": "Hamamatsu"
  },
  {
    "n": 31,
    "ja": "舞坂",
    "en": "Maisaka"
  },
  {
    "n": 32,
    "ja": "新居",
    "en": "Arai"
  },
  {
    "n": 33,
    "ja": "白須賀",
    "en": "Shirasuka"
  },
  {
    "n": 34,
    "ja": "二川",
    "en": "Futagawa"
  },
  {
    "n": 35,
    "ja": "吉田",
    "en": "Yoshida"
  },
  {
    "n": 36,
    "ja": "御油",
    "en": "Goyu"
  },
  {
    "n": 37,
    "ja": "赤坂",
    "en": "Akasaka"
  },
  {
    "n": 38,
    "ja": "藤川",
    "en": "Fujikawa"
  },
  {
    "n": 39,
    "ja": "岡崎",
    "en": "Okazaki"
  },
  {
    "n": 40,
    "ja": "池鯉鮒",
    "en": "Chiryu"
  },
  {
    "n": 41,
    "ja": "鳴海",
    "en": "Narumi"
  },
  {
    "n": 42,
    "ja": "宮",
    "en": "Miya"
  },
  {
    "n": 43,
    "ja": "桑名",
    "en": "Kuwana"
  },
  {
    "n": 44,
    "ja": "四日市",
    "en": "Yokkaichi"
  },
  {
    "n": 45,
    "ja": "石薬師",
    "en": "Ishiyakushi"
  },
  {
    "n": 46,
    "ja": "庄野",
    "en": "Shono"
  },
  {
    "n": 47,
    "ja": "亀山",
    "en": "Kameyama"
  },
  {
    "n": 48,
    "ja": "関",
    "en": "Seki"
  },
  {
    "n": 49,
    "ja": "坂下",
    "en": "Sakanoshita"
  },
  {
    "n": 50,
    "ja": "土山",
    "en": "Tsuchiyama"
  },
  {
    "n": 51,
    "ja": "水口",
    "en": "Minakuchi"
  },
  {
    "n": 52,
    "ja": "石部",
    "en": "Ishibe"
  },
  {
    "n": 53,
    "ja": "草津",
    "en": "Kusatsu"
  },
  {
    "n": 54,
    "ja": "大津",
    "en": "Otsu"
  },
  {
    "n": 55,
    "ja": "京師",
    "en": "Kyoto"
  }
]
API = "https://commons.wikimedia.org/w/api.php"
UA = "TokaidoWalkPhotoResearch/1.0 (https://github.com/belugic80/tokaido-walk; licensed asset collection)"
ALLOWED = ("CC BY-SA", "CC BY ", "CC0", "Public domain", "PD-old", "PD-Japan")

def get_json(params):
    req = Request(API + "?" + urlencode(params), headers={"User-Agent": UA})
    with urlopen(req, timeout=15) as response:
        return json.loads(response.read().decode("utf-8"))

def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

def val(meta, key):
    return (meta.get(key) or {}).get("value", "").strip()

ARTWORK_RE = re.compile(r"(illustration|illustrated|drawing|painting|woodcut|woodblock|ukiyo[- ]?e|lithograph|engraving|etching|cartoon|sketch|printmaking|poster|artwork|絵画|挿絵|イラスト|浮世絵|版画|木版画|絵図)", re.I)

def is_artwork(title, description="", author=""):
    # Reject clearly non-photographic artwork using Commons title and metadata.
    text = " ".join(str(x or "") for x in (title, description, author))
    return bool(ARTWORK_RE.search(text)) or "Abstract/medium" in text and any(x in text.lower() for x in ("woodcut", "print :", "painting", "drawing"))

def eligible(info):
    meta = info.get("extmetadata", {})
    license_name = val(meta, "LicenseShortName")
    if not any(x.lower() in license_name.lower() for x in ALLOWED):
        return False
    if not info.get("mime", "").startswith("image/"):
        return False
    if is_artwork(info.get("canonicaltitle", ""), val(meta, "ImageDescription"), val(meta, "Artist")):
        return False
    return max(info.get("width", 0), info.get("height", 0)) >= 1200 and min(info.get("width", 0), info.get("height", 0)) >= 600

def search_station(station):
    # Collect several distinct candidates so the site editor can choose the best fit.
    queries = [
        f'{station["en"]} Tokaido Japan',
        f'{station["en"]} historical site Japan',
        f'{station["ja"]} 東海道',
        f'{station["ja"]} 観光',
        f'{station["en"]} Japan',
        f'{station["en"]} landmark',
    ]
    found = {}
    for query in queries:
        try:
            data = None
            for attempt in range(3):
                try:
                    data = get_json({"action":"query","format":"json","generator":"search","gsrsearch":query,"gsrnamespace":6,"gsrlimit":30,"prop":"imageinfo","iiprop":"url|size|mime|extmetadata","iiurlwidth":1800})
                    break
                except Exception:
                    if attempt == 2:
                        raise
                    time.sleep(1.5 * (attempt + 1))
            pages = list((data.get("query", {}).get("pages", {}) or {}).values())
            candidates = []
            for page in pages:
                ii = (page.get("imageinfo") or [{}])[0]
                title = page.get("title", "").lower()
                if eligible(ii) and not is_artwork(page.get("title", ""), val(ii.get("extmetadata", {}), "ImageDescription"), val(ii.get("extmetadata", {}), "Artist")) and not any(bad in title for bad in ("map", "logo", "flag", "diagram", "coat of arms")):
                    key = page.get("title", "").lower()
                    if key not in found:
                        candidates.append((page, ii))
            candidates.sort(key=lambda pair: (pair[1].get("width",0)*pair[1].get("height",0), int(pair[1].get("width",0)>=pair[1].get("height",0))), reverse=True)
            for pair in candidates:
                found[pair[0].get("title", "").lower()] = pair
                if len(found) >= 4:
                    break
            if len(found) >= 4:
                break
        except Exception as exc:
            print(f'WARN search failed for {station["en"]} / {query}: {exc}', flush=True)
        time.sleep(0.4)
    return list(found.values())[:4]

def process_station(station):
    stem = f'{station["n"]:02d}-{slug(station["en"])}'
    try:
        existing = []
        for meta_path in sorted(ASSETS.glob(stem + "-*.json")):
            try:
                record = json.loads(meta_path.read_text(encoding="utf-8"))
                img_path = ASSETS / (meta_path.stem + ".jpg")
                if is_artwork(record.get("commons_title"), record.get("description"), record.get("author")):
                    if img_path.exists(): img_path.unlink()
                    meta_path.unlink()
                    print(f"REMOVED non-photo artwork: {meta_path.name}", flush=True)
                    continue
                if img_path.exists() and img_path.stat().st_size >= 15000:
                    existing.append((img_path.name, record))
            except Exception:
                pass
        if len(existing) >= 3:
            return station, existing, None

        results = search_station(station)
        saved = list(existing)
        seen = {rec.get("commons_title", "").lower() for _, rec in saved}
        for page, ii in results:
            if len(saved) >= 4:
                break
            title = page.get("title", "")
            if title.lower() in seen:
                continue
            # Stable candidate number based on currently saved files.
            used = {int(Path(name).stem.rsplit("-", 1)[-1]) for name, _ in saved}
            slot = next((i for i in range(1, 5) if i not in used), None)
            if slot is None:
                break
            candidate_stem = f"{stem}-{slot:02d}"
            filename = candidate_stem + ".jpg"
            destination = ASSETS / filename
            metadata_path = ASSETS / (candidate_stem + ".json")
            url = ii.get("thumburl") or ii.get("url")
            req = Request(url, headers={"User-Agent": UA})
            with urlopen(req, timeout=30) as response:
                data, mime = response.read(), response.headers.get("Content-Type", "")
            if not mime.startswith("image/") or len(data) < 15000:
                print(f'WARN skipped {title}: unexpected payload {mime}, {len(data)} bytes', flush=True)
                continue
            destination.write_bytes(data)
            meta = ii.get("extmetadata", {})
            record = {"route_number":station["n"],"station_ja":station["ja"],"station_en":station["en"],"candidate_number":slot,"commons_title":title,"source_page":"https://commons.wikimedia.org/wiki/"+title.replace(" ", "_"),"author":val(meta,"Artist") or "Not stated on file page","license":val(meta,"LicenseShortName") or "See source page","license_url":val(meta,"LicenseUrl"),"description":val(meta,"ImageDescription"),"source_file_url":ii.get("descriptionurl") or ii.get("url"),"width":ii.get("width"),"height":ii.get("height"),"stored_bytes":len(data),"stored_url":url}
            metadata_path.write_text(json.dumps(record,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
            saved.append((filename, record))
            seen.add(title.lower())
            print(f'OK {station["n"]:02d}/{len(STATIONS)} {station["en"]} candidate {slot}: {title} ({len(data):,} bytes; {record["license"]})', flush=True)
        if not saved:
            return station, [], "No eligible licensed images found"
        return station, saved, None
    except Exception as exc:
        print(f'FAILED {station["n"]:02d} {station["en"]}: {exc}', flush=True)
        return station, [], str(exc)

def main():
    manifest = ["# Tokaido station photo assets", "", "Multiple candidate photos per station are collected from Wikimedia Commons. Only explicitly reusable licenses are accepted. Review visual relevance before use on the live site.", "", "| Route no. | Station | Candidate file | Author | License | Dimensions | Source |", "|---:|---|---|---|---|---:|---|"]
    results = []
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = [pool.submit(process_station, station) for station in STATIONS]
        for future in as_completed(futures):
            results.append(future.result())
    results.sort(key=lambda row: row[0]["n"])
    successful_stations, image_count, failures = 0, 0, []
    for station, images, error in results:
        if not images:
            failures.append((station, error or "No eligible licensed images found"))
            continue
        successful_stations += 1
        for filename, record in sorted(images, key=lambda item: item[0]):
            author = re.sub(r"\s+", " ", re.sub("<[^>]+>", "", record.get("author",""))).strip()
            manifest.append(f'| {station["n"]} | {station["ja"]} / {station["en"]} | [{filename}](assets/stations/{filename}) | {author[:120]} | {record.get("license","See source page")} | {record.get("width")} × {record.get("height")} | [Commons source]({record.get("source_page")}) |')
            image_count += 1
    manifest.extend(["", f"**Stations with photos:** {successful_stations}/{len(STATIONS)}.", f"**Total photo candidates:** {image_count}.", ""])
    if failures:
        manifest.extend(["## Stations needing manual review", ""])
        manifest.extend([f'- {s["n"]}. {s["ja"]} ({s["en"]}) — {err}.' for s, err in failures])
    (ROOT / "photos" / "STATION-PHOTO-MANIFEST.md").write_text("\n".join(manifest)+"\n",encoding="utf-8")
    print(f"FINISHED: {successful_stations}/{len(STATIONS)} stations covered; {image_count} photo candidates; {len(failures)} stations need manual review.", flush=True)

if __name__ == "__main__":
    main()
