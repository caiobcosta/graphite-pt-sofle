"""Normalize keycode aliases to Vial primary ids, validate every keycode, print the main layers."""
import json, re
from pathlib import Path
import urllib.request
ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "cache"; CACHE.mkdir(exist_ok=True)
def fetch(url, name):
    """Download a third-party reference file once into cache/ (not committed)."""
    p = CACHE / name
    if not p.exists():
        urllib.request.urlretrieve(url, p)
    return p
TERGO_INFO = ("https://raw.githubusercontent.com/TergoTeclados/vial-qmk-firmware/vial/keyboards/tergo_sofle/rev0/info.json", "tergo_sofle_rev0_info.json")
SOFLE_GEO = ("https://raw.githubusercontent.com/qmk/qmk_firmware/master/keyboards/sofle/rev1/keyboard.json", "sofle_rev1_keyboard.json")
VIAL_KC = ("https://raw.githubusercontent.com/vial-kb/vial-gui/main/src/main/python/keycodes/keycodes.py", "vial_keycodes.py")
VIAL_ANY = ("https://raw.githubusercontent.com/vial-kb/vial-gui/main/src/main/python/any_keycode.py", "vial_any_keycode.py")
src=open(fetch(*VIAL_KC)).read()
prim={}   # any id/alias -> primary qmk_id
for m in re.finditer(r'K\("([^"]+)"', src):
    pid=m.group(1); prim[pid]=pid
    tail=src[m.end(): src.find('K("', m.end()) if src.find('K("', m.end())>0 else len(src)]
    al=re.search(r"(?<!recorder_)alias=\[([^\]]*)\]", tail)
    if al:
        for a in re.findall(r'"([^"]+)"', al.group(1)): prim[a]=pid
for n in range(16):
    for p in ("MO","DF","TG","TT","OSL","TO","TD"): prim[f"{p}({n})"]=f"{p}({n})"
    prim[f"USER{n:02}"]=f"USER{n:02}"
funcs=set(re.findall(r'"([A-Z_]+)": [A-Z_]+', open(fetch(*VIAL_ANY)).read()))
unknown=set()
def norm(k):
    if k in prim: return prim[k]
    m=re.fullmatch(r'([A-Z_0-9]+)\(([A-Z_0-9]+)\)', k)
    if m and m.group(1) in funcs and m.group(2) in prim: return f"{m.group(1)}({prim[m.group(2)]})"
    unknown.add(k); return k
p=ROOT/"keymap"/"tergo-sofle-graphite-pt.vil"; v=json.load(open(p))
v["layout"]=[[[norm(k) for k in r] for r in L] for L in v["layout"]]
v["encoder_layout"]=[[[norm(k) for k in e] for e in L] for L in v["encoder_layout"]]
v["tap_dance"]=[[norm(k) for k in td[:4]]+[td[4]] for td in v["tap_dance"]]
json.dump(v, open(p,"w"), ensure_ascii=False)
print("unknown:", sorted(unknown))
pos=[tuple(k["matrix"]) for k in json.load(open(fetch(*TERGO_INFO)))["layouts"]["LAYOUT"]["layout"]]
names={0:"BASE",3:"SYMB/NAV (L2)",6:"NUMPAD (L5)"}
for li,name in names.items():
    L=v["layout"][li]; seq=[L[r][c] for r,c in pos]
    print(f"\n[{li}] {name}")
    for a,b in ((0,12),(12,24),(24,36),(36,50),(50,60)): print("  ", " ".join(seq[a:b]))
print("\nencoders L0:", v["encoder_layout"][0], " tap_dance:", v["tap_dance"])
