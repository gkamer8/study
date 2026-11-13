import json, os, re
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TYPES = {"recall","cloze","identify","apply"}
def build(unit, slug, title, summary, lesson, cards, quiz):
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
    glossary=[]
    m = re.search(r"### Key terms\n+(.*?)\n\n", lesson, re.S)
    assert m, "lesson must start with a Key terms glossary"
    for line in m.group(1).splitlines():
        g = re.match(r"- \*\*(.+?)\*\*:?\s*(.*)", line.strip())
        assert g, line
        glossary.append({"term":g.group(1).rstrip(":"),"definition":g.group(2).lstrip(": ").strip()})
    d = {"unit":unit,"slug":slug,"title":title,"summary":summary,"glossary":glossary,"lesson":lesson.strip()+"\n","cards":cs,"quiz":qs}
    fn = f"{unit:02d}-{slug}.json"
    with open(os.path.join(OUT,fn),"w") as f: json.dump(d,f,indent=2,ensure_ascii=False)
    print(fn, "words",words,"cards",len(cs),"quiz",len(qs))
    return d
