#!/usr/bin/env python3
"""Download freely licensed Tokaido photo candidates from Wikimedia Commons.

This script only manages files under photos/assets and photos/ATTRIBUTION.md.
It does not edit the website or deploy anything.
"""
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
ASSETS.mkdir(parents=True, exist_ok=True)

PHOTOS = [
    {
        "filename": "hakone-old-tokaido-cedar-avenue.jpg",
        "source": "https://commons.wikimedia.org/wiki/File:Old_Tokaido_-_Hakone.jpg",
        "download": "https://commons.wikimedia.org/wiki/Special:FilePath/Old_Tokaido_-_Hakone.jpg",
        "author": "Quercus acuta",
        "license": "CC BY-SA 4.0",
        "license_url": "https://creativecommons.org/licenses/by-sa/4.0/",
        "description": "Old Tokaido cedar avenue near Hakone Kindergarten, Hakone, Japan.",
    },
    {
        "filename": "miho-no-matsubara-mount-fuji.jpg",
        "source": "https://commons.wikimedia.org/wiki/File:Miho_no_Matsubara_and_Mount_Fuji_s2.JPG",
        "download": "https://commons.wikimedia.org/wiki/Special:FilePath/Miho_no_Matsubara_and_Mount_Fuji_s2.JPG",
        "author": "Alpsdake",
        "license": "CC BY-SA 4.0",
        "license_url": "https://creativecommons.org/licenses/by-sa/4.0/",
        "description": "Mount Fuji seen from Miho no Matsubara, Shizuoka, Japan.",
    },
    {
        "filename": "hakone-old-tokaido-trail.jpg",
        "source": "https://commons.wikimedia.org/wiki/File:Old_Tokaido_Trail_%40_Hakone_%2810621614413%29.jpg",
        "download": "https://commons.wikimedia.org/wiki/Special:FilePath/Old_Tokaido_Trail_%40_Hakone_%2810621614413%29.jpg",
        "author": "Guilhem Vellut",
        "license": "CC BY 2.0",
        "license_url": "https://creativecommons.org/licenses/by/2.0/",
        "description": "Old Tokaido trail in Hakone, Japan.",
    },
]

def main():
    attribution = [
        "# Photo asset attribution",
        "",
        "These files are candidate assets for the Tokaido travel project. Verify suitability before using them in the website.",
        "",
        "| Local file | Description | Author | License | Original source |",
        "|---|---|---|---|---|",
    ]
    for photo in PHOTOS:
        destination = ASSETS / photo["filename"]
        if not destination.exists() or destination.stat().st_size == 0:
            req = Request(photo["download"], headers={"User-Agent": "TokaidoWalkPhotoAssets/1.0 (photo research; contact via GitHub repository)"})
            with urlopen(req, timeout=60) as response:
                data = response.read()
                content_type = response.headers.get("Content-Type", "")
            if not content_type.lower().startswith("image/") or len(data) < 10_000:
                raise RuntimeError(f"Unexpected download for {photo['filename']}: {content_type}, {len(data)} bytes")
            destination.write_bytes(data)
            print(f"Downloaded {photo['filename']} ({len(data):,} bytes)")
        else:
            print(f"Already present: {photo['filename']} ({destination.stat().st_size:,} bytes)")
        attribution.append(
            f"| `assets/{photo['filename']}` | {photo['description']} | {photo['author']} | "
            f"[{photo['license']}]({photo['license_url']}) | [Wikimedia Commons]({photo['source']}) |"
        )
    (ROOT / "ATTRIBUTION.md").write_text("\n".join(attribution) + "\n", encoding="utf-8")

if __name__ == "__main__":
    main()
