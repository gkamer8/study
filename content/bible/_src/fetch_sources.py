"""Download and cache the two Douay-Rheims sources (plus WEB for modern-numbering checks).

Primary:   eBible.org engDRA USFM (Douay-Rheims American Edition 1899 = Challoner text, public domain)
           https://ebible.org/Scriptures/engDRA_usfm.zip
Secondary: drbo.org chapter pages (Challoner revision), https://www.drbo.org/chapter/BBCCC.htm
Modern check: eBible.org eng-web USFM (World English Bible, public domain), only used to confirm
           which modern verse number holds the same text; its wording is never used.

Writes sources/primary_engDRA.json, sources/secondary_drbo.json, sources/modern_web.json
(only the verses this subject uses), so build.py runs offline.
"""
import io, json, os, re, sys, time, zipfile, html, urllib.request
from usfm import load
from books import BOOK
from items import ITEMS
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "sources")
UA = {"User-Agent": "Mozilla/5.0 (study.g0rdon.com content build)"}

def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()

def parse_ref(r):
    b, cv = r.split(" ")
    c, v = cv.split(":")
    v1, _, v2 = v.partition("-")
    return b, int(c), int(v1), int(v2 or v1)

def usfm_zip(url, d):
    if not os.path.isdir(d):
        os.makedirs(d)
        zipfile.ZipFile(io.BytesIO(get(url))).extractall(d)
    return load(d)

def drbo_chapter(bk, ch):
    page = get(f"https://www.drbo.org/chapter/{bk:02d}{ch:03d}.htm").decode("utf-8", "replace")
    out = {}
    for m in re.finditer(r'<a class=vn href="[^"]*l=(\d+)-#x">[^<]*</a>(.*?)(?=<a class=vn|</p>)', page, re.S):
        t = re.sub(r"<[^>]+>", "", m.group(2))
        t = re.sub(r"\s+", " ", html.unescape(t)).strip()
        out[int(m.group(1))] = re.split(r"\s*\[\d+\]", t)[0].strip()  # drop Challoner notes that trail a chapter's last verse
    return out

def main():
    refs = [(r, o) for deck in ITEMS.values() for r, _, o in deck]
    tmp = "/tmp/bible_src"
    dra = usfm_zip("https://ebible.org/Scriptures/engDRA_usfm.zip", tmp + "/engDRA")
    web = usfm_zip("https://ebible.org/Scriptures/eng-web_usfm.zip", tmp + "/engweb")
    prim, sec, mod = {}, {}, {}
    chapters = {}
    for r, o in refs:
        b, c, v1, v2 = parse_ref(r)
        for v in range(v1, v2 + 1):
            prim[f"{b} {c}:{v}"] = dra[(b, c, v)]
            if (b, c) not in chapters:
                chapters[(b, c)] = drbo_chapter(BOOK[b]["drbo"], c)
                time.sleep(0.5)
            sec[f"{b} {c}:{v}"] = chapters[(b, c)][v]
        for mr in [o.get("modern"), o.get("nabre")] + o.get("extra_modern", []):
            if not mr: continue
            mb, mc, m1, m2 = parse_ref(mr)
            for v in range(m1, m2 + 1):
                if (mb, mc, v) in web: mod[f"{mb} {mc}:{v}"] = web[(mb, mc, v)]
        if not o.get("modern"):
            for v in range(v1, v2 + 1):
                if (b, c, v) in web: mod[f"{b} {c}:{v}"] = web[(b, c, v)]
    os.makedirs(SRC, exist_ok=True)
    meta = {"retrieved": time.strftime("%Y-%m-%d")}
    for name, data, src in [("primary_engDRA.json", prim, "https://ebible.org/Scriptures/engDRA_usfm.zip"),
                            ("secondary_drbo.json", sec, "https://www.drbo.org/chapter/BBCCC.htm"),
                            ("modern_web.json", mod, "https://ebible.org/Scriptures/eng-web_usfm.zip")]:
        json.dump({"source": src, **meta, "verses": data}, open(os.path.join(SRC, name), "w"), indent=1, ensure_ascii=False)
        print(name, len(data))

if __name__ == "__main__":
    main()
