"""Build the Bible memorization subject from items.py + cached sources.

Run:  cd _src && python3 fetch_sources.py   # only when sources/ needs refreshing (network)
      python3 build.py                      # offline; writes ../index.json and ../NN-<deck>.json
Fails loudly if any verse differs in wording between the two Douay-Rheims sources.
"""
import json, os, re, datetime
from books import BOOK, B
from items import DECKS, ITEMS

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
SRC = os.path.join(HERE, "sources")
load = lambda n: json.load(open(os.path.join(SRC, n), encoding="utf-8"))
PRIM, SEC, MOD = load("primary_engDRA.json"), load("secondary_drbo.json"), load("modern_web.json")

# Known, reviewed differences between the two sources (keyed by DRB ref).
# Only the text outside `recite` may differ; `recite` must match word for word.
REVIEWED = {
    "PSA 118:105": "eBible prints the Hebrew acrostic letter 'NUN.' at the start of the verse; drbo.org shows it as a "
                   "section heading. It is not memorized (recite_prefix).",
}

def parse_ref(r):
    b, cv = r.split(" ")
    c, v = cv.split(":")
    v1, _, v2 = v.partition("-")
    return b, int(c), int(v1), int(v2 or v1)

def fmt(book_name, c, v1, v2):
    if book_name == "Psalms":
        book_name = "Psalm"  # a single psalm is cited 'Psalm 22:1'
    return f"{book_name} {c}:{v1}" + (f"–{v2}" if v2 != v1 else "")

def words(t):
    t = t.lower().replace("’", "'").replace("‘", "'").replace("-", " ")
    return re.sub(r"[^a-z' ]", " ", t).replace("'", "").split()

def tidy(t):
    return re.sub(r"\s+", " ", t).strip()

def item_accept(b, refs, v1s):
    """Accepted reference strings for the text->reference drill.
    refs: list of (chapter, v_start, v_end) numberings that count as correct (DRB first)."""
    bk = BOOK[b]
    names = [bk["drb"]] + ([bk["modern"]] if bk["modern"] != bk["drb"] else [])
    aliases = names + [a for a in bk["drb_aliases"] + bk["modern_aliases"]]
    out = []
    for c, a, z in refs:
        for n in aliases:
            out.append(f"{n} {c}:{a}")
            if z != a:
                out.append(f"{n} {c}:{a}-{z}")
    seen, res = set(), []
    for s in out:
        k = re.sub(r"\s+", "", s.lower())
        if k not in seen:
            seen.add(k); res.append(s)
    return res

def build():
    today = datetime.date.today().isoformat()
    items_all, units = [], []
    crosscheck = {"exact": 0, "punctuation_only": 0, "reviewed": 0}
    for di, (slug, title, summary) in enumerate(DECKS, 1):
        raw = []
        for ref, context, o in ITEMS[slug]:
            b, c, v1, v2 = parse_ref(ref)
            bk = BOOK[b]
            verses, sec_verses = [], []
            for v in range(v1, v2 + 1):
                k = f"{b} {c}:{v}"
                verses.append({"verse": v, "text": tidy(PRIM["verses"][k])})
                sec_verses.append(tidy(SEC["verses"][k]))
            text = " ".join(x["text"] for x in verses)
            sec_text = " ".join(sec_verses)
            prefix = o.get("strip", "")
            if prefix:
                assert text.startswith(prefix + " "), (ref, prefix, text)
                recite = text[len(prefix) + 1:]
            else:
                recite = text
            # Cross-check against the second source.
            sec_recite = sec_text[len(prefix) + 1:] if prefix and sec_text.startswith(prefix + " ") else sec_text
            if words(recite) != words(sec_recite):
                raise SystemExit(f"WORDING MISMATCH {ref}\n  eBible: {recite}\n  drbo:   {sec_recite}")
            if text.replace("’", "'") == sec_text.replace("’", "'"):
                status = "exact"
            elif ref in REVIEWED:
                status = "reviewed"
            elif words(text) == words(sec_text):
                status = "punctuation_only"
            else:
                raise SystemExit(f"UNREVIEWED DIFFERENCE {ref}\n  eBible: {text}\n  drbo:   {sec_text}")
            crosscheck[status] += 1

            ref_drb = fmt(bk["drb"], c, v1, v2)
            if o.get("modern"):
                mb, mc, m1, m2 = parse_ref(o["modern"])
            else:
                mb, mc, m1, m2 = b, c, v1, v2
            ref_modern = fmt(BOOK[mb]["modern"], mc, m1, m2)
            nab = None
            if o.get("nabre"):
                nb, nc, n1, n2 = parse_ref(o["nabre"])
                nab = fmt(BOOK[nb]["modern"], nc, n1, n2)
            numberings = [(c, v1, v2), (mc, m1, m2)]
            if nab: numberings.append((nc, n1, n2))
            for e in o.get("extra_modern", []):
                eb, ec, e1, e2 = parse_ref(e); numberings.append((ec, e1, e2))
            systems = ["drb", "modern"] + (["nabre"] if nab else []) + ["modern"] * len(o.get("extra_modern", []))
            numbering_list = [{"system": s, "chapter": n[0], "verse_start": n[1], "verse_end": n[2]}
                              for s, n in zip(systems, numberings)]
            # dedupe identical numberings, keep first (drb wins)
            _seen = set(); numbering_list = [x for x in numbering_list if not ((k := (x["chapter"], x["verse_start"], x["verse_end"])) in _seen or _seen.add(k))]
            # passages: item_accept emits both the starting verse alone and the full range
            accept = item_accept(b, numberings, None)
            notes = []
            if bk["drb"] != bk["modern"]:
                notes.append(f"{bk['drb']} is the Douay name for {bk['modern']}.")
            if (mc, m1, m2) != (c, v1, v2):
                why = ("Douay-Rheims follows the Vulgate/Greek psalm numbering, usually one lower than modern Bibles"
                       if b == "PSA" else "Douay-Rheims follows the Vulgate verse numbering here")
                notes.append(f"{why}: {ref_drb} in the Douay is {ref_modern} in most modern Bibles"
                             + (f" ({nab} in the NABRE)." if nab else "."))
            elif nab:
                notes.append(f"The NABRE numbers this {nab}.")
            raw.append(dict(
                ref_drb=ref_drb,
                ref_modern=ref_modern if ref_modern != ref_drb else None,
                ref_nabre=nab,
                book=b, book_drb=bk["drb"], book_modern=bk["modern"],
                chapter=c, verse_start=v1, verse_end=v2,
                verses=verses if v2 != v1 else None,
                text=text, recite=recite, recite_prefix=prefix or None,
                word_count=len(words(recite)),
                context=context, deck=slug, group=o.get("group"),
                numberings=numbering_list, accept=accept, note=" ".join(notes) or None,
                source={"primary": "eBible.org engDRA (Douay-Rheims 1899, Challoner text)",
                        "crosscheck": "drbo.org", "crosscheck_status": status,
                        **({"review_note": REVIEWED[ref]} if ref in REVIEWED else {})},
            ))
        # order: short -> long; a group (Beatitudes) stays together, in canonical order,
        # at the position of its average length.
        snapshot = list(raw)
        def key(it):
            if it["group"]:
                g = [x for x in snapshot if x["group"] == it["group"]]
                return (sum(x["word_count"] for x in g) / len(g), 0, it["chapter"], it["verse_start"])
            return (it["word_count"], 1, it["chapter"], it["verse_start"])
        raw.sort(key=key)
        cards = []
        for n, it in enumerate(raw, 1):
            iid = f"bible-{slug}-{n:02d}"
            it = {"id": iid, **{k: v for k, v in it.items() if v is not None}}
            items_all.append(it)
            ref_line = it["ref_drb"] + (f" ({it['ref_modern']} in modern Bibles)" if it.get("ref_modern") else "")
            cards.append({"id": f"{iid}-text", "item": iid, "type": "verse-text", "direction": "ref-to-text",
                          "front": ref_line, "hint": it["context"], "answer_form": "the verse, word for word", "back": it["recite"],
                          "tags": [slug, it["book"].lower()]})
            cards.append({"id": f"{iid}-ref", "item": iid, "type": "verse-ref", "direction": "text-to-ref",
                          "front": it["recite"], "answer_form": "book chapter:verse, e.g. John 3:16", "back": ref_line,
                          "accept": it["accept"], "tags": [slug, it["book"].lower()]})
        fname = f"{di:02d}-{slug}.json"
        unit = {"unit": di, "slug": slug, "title": title, "summary": summary,
                "kind": "verses", "items": [i for i in items_all if i["deck"] == slug],
                "cards": cards, "lesson": "", "glossary": [], "quiz": []}
        json.dump(unit, open(os.path.join(OUT, fname), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        units.append({"unit": di, "slug": slug, "title": title, "summary": summary, "file": fname,
                      "item_count": len(raw), "card_count": len(cards), "quiz_count": 0,
                      "glossary_count": 0, "lesson_words": 0, "prerequisites": [], "figure_count": 0})
    books = [{"usfm": b[0], "drb": b[2], "modern": b[3], "drb_aliases": b[4], "modern_aliases": b[5]} for b in B]
    spec = json.load(open(os.path.join(HERE, "scoring_spec.json"), encoding="utf-8"))
    index = {
        "subject": "bible", "kind": "verses",
        "title": "Bible verses (Douay-Rheims)",
        "description": "Memorize well-known verses in the Douay-Rheims Bible (Challoner revision), the traditional Catholic English translation. Two typed drills: text to reference, and reference to text with a cloze ramp.",
        "schema_version": 1, "generated": today,
        "translation": {"name": "Douay-Rheims Bible, Challoner revision", "edition": "American edition of 1899 (Challoner text, 1749–1752 revision of the 1582/1609–10 Douay-Rheims)",
                        "license": "Public domain", "numbering": "Vulgate (psalms use the Greek/Vulgate numbers)"},
        "sources": {"primary": PRIM["source"], "primary_retrieved": PRIM["retrieved"],
                    "crosscheck": SEC["source"], "crosscheck_retrieved": SEC["retrieved"],
                    "modern_numbering_check": MOD["source"], "crosscheck_summary": crosscheck},
        "units": units,
        "totals": {"items": len(items_all), "cards": 2 * len(items_all), "quiz": 0, "glossary_terms": 0, "figures": 0},
        "books": books,
        "scoring": spec,
        "items": items_all,
    }
    json.dump(index, open(os.path.join(OUT, "index.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("items", len(items_all), "cards", 2 * len(items_all), crosscheck)
    for u in units: print(f"  {u['file']}: {u['item_count']} items")

if __name__ == "__main__":
    build()
