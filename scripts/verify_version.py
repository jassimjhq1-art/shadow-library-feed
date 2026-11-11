import json
from pathlib import Path
from urllib.parse import urlparse
x=json.loads((Path(__file__).resolve().parents[1]/"app-version.json").read_text(encoding="utf-8"))
assert x.get("schemaVersion")==1
assert type(x.get("versionCode")) is int and x["versionCode"]>=1
assert isinstance(x.get("versionName"),str) and len(x["versionName"])<=32
assert x.get("downloadUrl") is None or (
    isinstance(x.get("downloadUrl"),str)
    and urlparse(x["downloadUrl"]).scheme=="https"
    and bool(urlparse(x["downloadUrl"]).hostname)
)
assert x.get("sha256") is None or (
    isinstance(x.get("sha256"),str) and len(x["sha256"])==64
    and all(c in "0123456789abcdefABCDEF" for c in x["sha256"])
)
print("Shadow Library app version manifest: VALID")
