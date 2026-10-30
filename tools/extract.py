"""Daily refresh for the public Fundamental Pullback page.

Reads the latest Google Sheets get_values results from this session's transcript (.jsonl),
writes the page's data files and updates data/manifest.js.

Usage:  python3 extract.py <transcript.jsonl> <workdir>
  <workdir>/data/manifest.js must already exist (downloaded from the published page).
Prints the list of data files to publish.
"""
import json, os, re, sys, datetime

src, work = sys.argv[1], sys.argv[2]
data = os.path.join(work, "data")
os.makedirs(data, exist_ok=True)

mf_txt = open(os.path.join(data, "manifest.js"), encoding="utf-8").read()
mf = json.loads(re.search(r"=\s*(\{.*\})\s*;?\s*$", mf_txt, re.S).group(1))
scan_start = int(mf.get("scanRows", 0)) + 2          # first sheet row not yet published

FULL = {"Decisiones": "A1:AN", "Operaciones": "A1:L", "Cuenta": "A1:F", "Historial": "A1:AP", "Retrospectiva": "A1:O", "Gestión": "A1:L"}
# older reads of Decisiones (before the "Cálculo" and "Informe (ID)" columns) are still accepted
ALT = {"Decisiones": ("A1:AD", "A1:AE", "A1:AF", "A1:AG", "A1:AJ", "A1:AL")}
NAMES = {"Decisiones": "dec", "Operaciones": "ops", "Cuenta": "acct", "Historial": "hist", "Retrospectiva": "retro", "Gestión": "ges"}
found, scan_new = {}, None

def texts(c):
    if isinstance(c, str):
        yield c
    elif isinstance(c, list):
        for x in c:
            if isinstance(x, dict):
                if x.get("type") == "text":
                    yield x.get("text", "")
                elif "content" in x:
                    yield from texts(x["content"])

with open(src, encoding="utf-8") as f:
    for line in f:
        if '"range"' not in line and "Output has been saved to" not in line:
            continue
        try:
            ev = json.loads(line)
        except Exception:
            continue
        content = (ev.get("message") or {}).get("content")
        if not isinstance(content, list):
            continue
        for part in content:
            if not isinstance(part, dict) or part.get("type") != "tool_result":
                continue
            for t in texts(part.get("content")):
                t = t.strip()
                if not t.startswith("{"):
                    # large results are saved to a file; the transcript only holds its path
                    m = re.search(r"Output has been saved to (\S+?\.(?:txt|json))", t)
                    if not m or not os.path.exists(m.group(1)):
                        continue
                    try:
                        t = open(m.group(1), encoding="utf-8").read().strip()
                    except Exception:
                        continue
                    if not t.startswith("{"):
                        continue
                try:
                    d = json.loads(t)
                except Exception:
                    continue
                r = str(d.get("range", ""))
                if "!" not in r:
                    continue
                sheet, rng = r.split("!", 1)
                sheet = sheet.strip("'")
                v = d.get("values")
                if sheet in FULL and (rng.startswith(FULL[sheet]) or rng.startswith(ALT.get(sheet, ("\0",)))) and isinstance(v, list):
                    found[sheet] = v
                elif sheet == "Escáner" and rng.startswith("A%d:" % scan_start):
                    scan_new = v if isinstance(v, list) else []

missing = [s for s in FULL if s not in found]
if missing:
    print("MISSING READS:", missing)
    sys.exit(1)

out = []
for sheet, v in found.items():
    key = NAMES[sheet]
    with open(os.path.join(data, key + ".js"), "w", encoding="utf-8") as g:
        g.write("window.FP=window.FP||{};FP.%s=%s;\n" % (key, json.dumps(v, ensure_ascii=False, separators=(",", ":"))))
    out.append("data/%s.js" % key)
    if "data/%s.js" % key not in mf["files"]:
        mf["files"].append("data/%s.js" % key)

rows = [r for r in (scan_new or []) if r and str(r[0]).strip()]
if rows:
    name = "data/scan-%d.js" % scan_start
    with open(os.path.join(work, name), "w", encoding="utf-8") as g:
        g.write("window.FP=window.FP||{};FP.scan=(FP.scan||[]).concat(%s);\n" % json.dumps(rows, ensure_ascii=False, separators=(",", ":")))
    out.append(name)
    if name not in mf["files"]:
        mf["files"].insert(len([x for x in mf["files"] if x.startswith("data/scan")]), name)
    mf["scanRows"] = int(mf.get("scanRows", 0)) + len(rows)
print("new scanner rows:", len(rows), "(scan_new read found)" if scan_new is not None else "(NO Escáner read found for row %d)" % scan_start)

# as-of date = last SPY close in Historial (serial date in column A)
as_of = mf.get("asOf")
for r in reversed(found["Historial"][2:]):
    try:
        ser = float(str(r[0]).replace(".", "").replace(",", "."))
        as_of = (datetime.date(1899, 12, 30) + datetime.timedelta(days=int(ser))).isoformat()
        break
    except Exception:
        continue
mf["asOf"] = as_of
mf["generated"] = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
with open(os.path.join(data, "manifest.js"), "w", encoding="utf-8") as g:
    g.write("window.FP_MANIFEST=%s;\n" % json.dumps(mf, ensure_ascii=False))
out.append("data/manifest.js")
print("asOf:", as_of, "scanRows:", mf["scanRows"])
print("PUBLISH:", json.dumps(out))
