import re,glob,os,json
def clean(s):
    s=re.sub(r'\\f .*?\\f\*','',s)
    s=re.sub(r'\\x .*?\\x\*','',s)
    s=re.sub(r'\\w ([^|\\]*)\|[^\\]*\\w\*',r'\1',s)
    s=re.sub(r'\\w ([^\\]*)\\w\*',r'\1',s)
    s=re.sub(r'\\\+?[a-z]+\d*\*?','',s)
    return re.sub(r'\s+',' ',s).strip()
def load(d):
    out={}
    for f in sorted(glob.glob(d+'/*.usfm')):
        txt=open(f,encoding='utf8').read()
        book=re.search(r'\\id (\w+)',txt).group(1)
        ch=None;cur=None
        for line in txt.split('\n'):
            m=re.match(r'\\c (\d+)',line)
            if m: ch=int(m.group(1));cur=None;continue
            m=re.match(r'\\v (\d+)(?:-\d+)? (.*)',line)
            if m and ch:
                cur=(book,ch,int(m.group(1)));out[cur]=m.group(2);continue
            if cur and not re.match(r'\\(s\d?|ms|mt|d|r|h|toc|id|ide|cl)\b',line):
                body=re.sub(r'^\\(p|q\d?|m|pi\d?|nb|li\d?|b|pmo|mi)\s*','',line)
                if body.strip(): out[cur]+=' '+body
    return {k:clean(v) for k,v in out.items()}
