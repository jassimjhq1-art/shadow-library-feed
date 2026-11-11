import json
import re
from pathlib import Path
from urllib.parse import urlparse

root=Path(__file__).resolve().parents[1]
p=root/"catalog.json"
assert p.stat().st_size < 2_500_000, "catalog too large"
data=json.loads(p.read_text(encoding="utf-8"))
assert data.get("version")==1, "version must be 1"
assert isinstance(data.get("revision"),int) and data["revision"]>=1, "revision must be >=1"
assert isinstance(data.get("books"),list) and len(data["books"])<=100
def is_https(v):
    if v is None: return True
    if not isinstance(v,str): return False
    u=urlparse(v)
    return u.scheme=="https" and bool(u.hostname)
seen=set()
for b in data["books"]:
    assert isinstance(b,dict), "book must be object"
    bid=b.get("id","")
    assert isinstance(bid,str) and re.fullmatch(r"[A-Za-z0-9_-]{2,64}",bid), "invalid book id"
    assert bid not in seen, "duplicate book id"
    seen.add(bid)
    assert is_https(b.get("cover")), "cover must use https"
    chapters=b.get("chapters")
    assert isinstance(chapters,list) and len(chapters)<=200, "invalid chapters"
    if bid!="nightmare":
        assert isinstance(b.get("title"),str) and bool(b["title"].strip()), "book title required"
    for c in chapters:
        assert isinstance(c,dict), "chapter must be object"
        assert is_https(c.get("audio")), "audio must use https"
        parts=c.get("audioParts")
        if parts is not None:
            assert isinstance(parts,list) and 2<=len(parts)<=12, "audioParts must contain 2..12 URLs"
            assert all(isinstance(a,str) and is_https(a) for a in parts), "all audio parts must be HTTPS"
        if bid=="nightmare":
            assert str(c.get("id","")).isdigit(), "existing book patch needs numeric chapter id"
            assert 1<=int(c["id"])<=10, "chapter must be 1..10"
            continue
        assert isinstance(c.get("title"),str) and bool(c["title"].strip())
        assert c.get("category","crime") in {"horror","crime","heist","prison"}, "invalid category"
        paras=c.get("paragraphs")
        assert isinstance(paras,list) and 0<len(paras)<=500
        for par in paras:
            assert isinstance(par,dict) and par.get("t") in {"p","h2","h3"}
            assert isinstance(par.get("text"),str) and len(par["text"])<=12000
print("Shadow Library public catalog: VALID")
