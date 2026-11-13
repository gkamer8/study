import json, os, re
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TYPES = {"recall","cloze","identify","apply"}
def build(unit, slug, title, summary, lesson, cards, quiz, glossary_accept=None):
    pre = f"u{unit}"
    cs = []
    for i,c in enumerate(cards,1):
        t,front,back,tags,accept = c
        assert t in TYPES, t
        assert accept and all(isinstance(a,str) and a.strip() for a in accept), (i,front)
        assert len(accept[0]) <= 60, (i, accept[0])
        seen=[]
        for a in accept:
            if a.strip().lower() not in [x.lower() for x in seen]: seen.append(a.strip())
        cs.append({"id":f"{pre}-c{i:02d}","front":front,"back":back,"accept":seen,"tags":tags,"type":t})
    qs = []
    for i,(q,ch,a,ex) in enumerate(quiz,1):
        assert len(ch)==4 and 0<=a<4
        qid=f"{pre}-q{i:02d}"
        import random, hashlib
        rng=random.Random(int(hashlib.md5(qid.encode()).hexdigest(),16))
        order=list(range(4)); rng.shuffle(order)
        ch2=[ch[j] for j in order]; a2=order.index(a)
        qs.append({"id":qid,"question":q,"choices":ch2,"answer_index":a2,"explanation":ex})
    words = len(re.findall(r"[A-Za-z0-9]+(?:['’-][A-Za-z0-9]+)*", lesson))
    glossary=[]; LEAKS=[]
    m = re.search(r"### Key terms\n+(.*?)\n\n", lesson, re.S)
    assert m, "lesson must start with a Key terms glossary"
    gacc = glossary_accept or {}
    for line in m.group(1).splitlines():
        g = re.match(r"- \*\*(.+?)\*\*:\s*(.*)", line.strip())
        assert g, line
        raw, definition = g.group(1), g.group(2).strip()
        pm = re.match(r"(.+?) \((.+)\)$", raw)
        term, abbr = (pm.group(1), pm.group(2)) if pm else (raw, None)
        acc = [term] + ([abbr] if abbr else [])
        for a in list(acc):
            if re.fullmatch(r"[A-Za-z][a-z-]+( [a-z-]+)*", a) and not re.search(r"(s|x|sh|ch)$", a):
                acc.append(a[:-1]+"ies" if re.search(r"[^aeiou]y$", a) else a+"s")
        acc += gacc.get(term, [])
        seen=[]
        for a in acc:
            if a.lower() not in [x.lower() for x in seen]: seen.append(a)
        for a in seen:
            if len(a) >= 3:
                if re.search(r"(?<![A-Za-z0-9])"+re.escape(a)+r"(?![A-Za-z0-9])", definition, re.I): LEAKS.append((unit, term, a))
        glossary.append({"term":term,"definition":definition,"accept":seen})
    assert not LEAKS, LEAKS
    terms=[x["term"].lower() for x in glossary]; defs=[x["definition"] for x in glossary]
    assert len(set(terms))==len(terms), (unit,"dup term")
    assert len(set(defs))==len(defs), (unit,"dup definition")
    for x in glossary: assert x["term"] in gacc or True
    for k in gacc: assert k in [x["term"] for x in glossary], (unit,"glossary_accept key not in glossary",k)
    d = {"unit":unit,"slug":slug,"title":title,"summary":summary,"glossary":glossary,"lesson":lesson.strip()+"\n","cards":cs,"quiz":qs}
    fn = f"{unit:02d}-{slug}.json"
    with open(os.path.join(OUT,fn),"w") as f: json.dump(d,f,indent=2,ensure_ascii=False)
    print(fn, "words",words,"cards",len(cs),"quiz",len(qs))
    return d
