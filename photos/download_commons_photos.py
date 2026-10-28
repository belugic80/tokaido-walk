#!/usr/bin/env python3
"""Fetch freely licensed photo candidates for every station listed in the Tokaido route."""
import json, re, time
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
    with urlopen(req, timeout=45) as response:
        return json.loads(response.read().decode("utf-8"))

def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

def val(meta, key):
    return (meta.get(key) or {}).get("value", "").strip()

def eligible(info):
    meta = info.get("extmetadata", {})
    license_name = val(meta, "LicenseShortName")
    if not any(x.lower() in license_name.lower() for x in ALLOWED):
        return False
    if not info.get("mime", "").startswith("image/"):
        return False
    return max(info.get("width", 0), info.get("height", 0)) >= 1200 and min(info.get("width", 0), info.get("height", 0)) >= 600

def search_station(station):
    queries = [f'"{station["ja"]}" Japan', f'"{station["en"]}" Japan', f'{station["en"]} Tokaido Japan']
    for query in queries:
        try:
            data = get_json({"action":"query","format":"json","generator":"search","gsrsearch":query,"gsrnamespace":6,"gsrlimit":30,"prop":"imageinfo","iiprop":"url|size|mime|extmetadata","iiurlwidth":1800})
            pages = list((data.get("query", {}).get("pages", {}) or {}).values())
            candidates = []
            for page in pages:
                ii = (page.get("imageinfo") or [{}])[0]
                title = page.get("title", "").lower()
                if eligible(ii) and not any(bad in title for bad in ("map", "logo", "flag", "diagram", "coat of arms")):
                    candidates.append((page, ii))
            if candidates:
                candidates.sort(key=lambda pair: (pair[1].get("width",0)*pair[1].get("height",0), int(pair[1].get("width",0)>=pair[1].get("height",0))), reverse=True)
                return candidates[0]
        except Exception as exc:
            print(f'WARN search failed for {station["en"]} / {query}: {exc}')
        time.sleep(0.2)
    return None

def main():
    manifest = ["# Tokaido station photo assets", "", "Automatically collected from Wikimedia Commons. Only files with an explicit reuse-friendly license were accepted. Please review visual relevance before using on the live site.", "", "| Route no. | Station | File | Author | License | Dimensions | Source |", "|---:|---|---|---|---|---:|---|"]
    successes, failures = 0, []
    for station in STATIONS:
        stem = f'{station["n"]:02d}-{slug(station["en"])}'
        filename = stem + ".jpg"
        destination = ASSETS / filename
        metadata_path = ASSETS / (stem + ".json")
        if destination.exists() and metadata_path.exists():
            record = json.loads(metadata_path.read_text(encoding="utf-8"))
        else:
            result = search_station(station)
            if not result:
                failures.append(station)
                print(f'NO LICENSED IMAGE FOUND: {station["n"]}. {station["en"]} ({station["ja"]})')
                continue
            page, ii = result
            url = ii.get("thumburl") or ii.get("url")
            try:
                req = Request(url, headers={"User-Agent": UA})
                with urlopen(req, timeout=60) as response:
                    data, mime = response.read(), response.headers.get("Content-Type", "")
                if not mime.startswith("image/") or len(data) < 15000:
                    raise RuntimeError(f"unexpected payload: {mime}, {len(data)} bytes")
                destination.write_bytes(data)
            except Exception as exc:
                failures.append(station)
                print(f'DOWNLOAD FAILED: {station["en"]}: {exc}')
                continue
            meta = ii.get("extmetadata", {})
            record = {"route_number":station["n"],"station_ja":station["ja"],"station_en":station["en"],"commons_title":page.get("title",""),"source_page":"https://commons.wikimedia.org/wiki/"+page.get("title","").replace(" ","_"),"author":val(meta,"Artist") or "Not stated on file page","license":val(meta,"LicenseShortName") or "See source page","license_url":val(meta,"LicenseUrl"),"description":val(meta,"ImageDescription"),"source_file_url":ii.get("descriptionurl") or ii.get("url"),"width":ii.get("width"),"height":ii.get("height"),"stored_bytes":len(data),"stored_url":url}
            metadata_path.write_text(json.dumps(record,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
            print(f'OK {station["n"]:02d}/{len(STATIONS)} {station["en"]}: {page.get("title")} ({len(data):,} bytes; {record["license"]})')
        author = re.sub(r"\s+", " ", re.sub("<[^>]+>", "", record.get("author",""))).strip()
        manifest.append(f'| {station["n"]} | {station["ja"]} / {station["en"]} | [{filename}](assets/stations/{filename}) | {author[:120]} | {record.get("license","See source page")} | {record.get("width")} × {record.get("height")} | [Commons source]({record.get("source_page")}) |')
        successes += 1
        time.sleep(0.15)
    manifest.extend(["", f"**Collected:** {successes}/{len(STATIONS)} station images.", ""])
    if failures:
        manifest.extend(["## Stations needing manual review", ""])
        manifest.extend([f'- {s["n"]}. {s["ja"]} ({s["en"]}) — no eligible image found by automated search.' for s in failures])
    (ROOT / "STATION-PHOTO-MANIFEST.md").write_text("\n".join(manifest)+"\n",encoding="utf-8")
    print(f"FINISHED: {successes}/{len(STATIONS)} station images; {len(failures)} need manual review.")

if __name__ == "__main__":
    main()
