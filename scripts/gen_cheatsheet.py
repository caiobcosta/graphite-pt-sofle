import json, html, sys, math
COMBO = "--combo" in sys.argv
HOME = {25,26,27,28,31,32,33,34}   # N R T S | H A E I
DOTS = {28,31}                     # S, H
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
VIAL_KC = ("https://raw.githubusercontent.com/vial-kb/vial-gui/main/src/main/python/keycodes/keycodes.py", "vial_keycodes.py")
VIAL_ANY = ("https://raw.githubusercontent.com/vial-kb/vial-gui/main/src/main/python/any_keycode.py", "vial_any_keycode.py")
# Key geometry of the Tergo Sofle, in key units (1u = 19.05 mm), LAYOUT order.
# Thumbs, encoder and inner columns follow Tergo's own layout drawing (Tergo-Sofle-Documentation,
# static/img/base_abnt.svg). The column stagger was measured on photos of the board: the two
# outer columns sit level, 0.375u below the middle-finger column. Tergo's drawing puts them at
# 0.625u and the stock QMK Sofle drawing at 0.375u/0.5u; fitting each candidate to two close-up
# photos left an RMS error of 0.05u, 0.04u and 0.015u (measured values) respectively.
STAGGER = [0.375, 0.375, 0.125, 0.0, 0.125, 0.25]      # left half, outer -> inner column
def _geometry():
    geo, rot = [], {}
    def add(cx, cy, h=1, r=0):
        if r: rot[len(geo)] = r
        geo.append({"x": cx - 0.5, "y": cy - h / 2, "h": h})
    def row(r):
        for c in range(6): add(c + 0.5, STAGGER[c] + 0.5 + r)            # left, outer -> inner
        if r == 3: add(6.625, STAGGER[5] + 3.5); add(9.375, STAGGER[5] + 3.5)   # encoders
        for c in range(5, -1, -1): add(15.5 - c, STAGGER[c] + 0.5 + r)   # right, inner -> outer
    for r in range(4): row(r)
    thumbs = [(2.5, 4.625, 1, 0), (3.5, 4.5, 1, 0), (4.5, 4.625, 1, 0), (5.643, 4.893, 1, 22.5), (6.75, 5.196, 1.5, 30)]
    for cx, cy, h, r in thumbs: add(cx, cy, h, r)
    for cx, cy, h, r in reversed(thumbs): add(16 - cx, cy, h, -r)
    return geo, rot
GEO, ROT = _geometry()
assert len(GEO) == 60
ENC = {42, 43}

# The halves are drawn splayed: each one rotated HALF_ANGLE degrees (left clockwise, right
# counter-clockwise). On the author's desk each half sits at about 21 degrees, but the drawing puts
# the halves much closer together than they are on the desk, so the true angle reads as too steep
# on paper; 15 keeps the cue and the legends readable. Override with --angle=N (0 draws them straight).
HALF_ANGLE = next((float(a.split("=", 1)[1]) for a in sys.argv if a.startswith("--angle=")), 15.0)
HALF_GAP = 0.7                 # clearance between the two halves at their closest point, in u
PIVOT = (3.9, 3.1)             # rotation centre of the left half; the right half mirrors it about x = 8
def _splay():
    a = math.radians(HALF_ANGLE); ca, sa = math.cos(a), math.sin(a)
    pts = []
    for i, g in enumerate(GEO):
        h = g.get("h", 1); cx, cy = g["x"] + 0.5, g["y"] + h / 2
        if cx > 8: continue
        r = math.radians(ROT.get(i, 0)); cr, sr = math.cos(r), math.sin(r)
        for dx, dy in ((-.5, -h/2), (.5, -h/2), (.5, h/2), (-.5, h/2)):
            x, y = cx + dx*cr - dy*sr - PIVOT[0], cy + dx*sr + dy*cr - PIVOT[1]
            pts.append((PIVOT[0] + x*ca - y*sa, PIVOT[1] + x*sa + y*ca))
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    tx = (16 - 2*max(xs) - HALF_GAP) / 2          # shift that leaves HALF_GAP between the halves
    x0 = min(xs) + tx - 0.1; y0 = min(ys) - 0.1
    return tx, f"{x0:.3f} {y0:.3f} {16 - 2*x0:.3f} {max(ys) - min(ys) + 0.2:.3f}"
SPLAY_TX, VIEWBOX = _splay()
KEY = 0.92

T = "▽"      # transparent
N = ""       # no-op

def K(main, shift=None, small=False):
    return {"m": main, "s": shift, "small": small}

# ---------- L1: Graphite-PT (ABNT2) ----------
L1 = [
 K("ESC",small=1), K("1","!"), K("2","@"), K("3","#"), K("4","$"), K("5","%"),
 K("6","¨"), K("7","&"), K("8","*"), K("9","("), K("0",")"), K("=","+"),
 K("TAB",small=1), K("B"), K("L"), K("D"), K("V"), K("Z"),
 K("'",'"'), K("F"), K("U"), K("O"), K("J"), K("-","_"),
 K("SHIFT",small=1), K("N"), K("R"), K("T"), K("S"), K("G"),
 K("Y"), K("H"), K("A"), K("E"), K("I"), K("SHIFT",small=1),
 K("Ç"), K("Q"), K("X"), K("M"), K("C"), K("W"),
 K("L4","scroll ↔",small=1), K("L3","zoom 100%",small=1),
 K("K"), K("P"), K(",","<"), K(".",">"), K(";",":"), K("/","?"),
 K("^","L5",small=1), K("~","^"), K("´","`"), K("L2",small=1), K("SPACE",small=1),
 K("ENTER",small=1), K("BKSP",small=1), K("CMD",small=1), K("OPT",small=1), K("CTRL",small=1),
]
# ---------- L2: Símbolos e Navegação ----------
L2 = [
 K("F1",small=1), K("F2",small=1), K("F3",small=1), K("F4",small=1), K("F5",small=1), K("F6",small=1),
 K("F7",small=1), K("F8",small=1), K("F9",small=1), K("F10",small=1), K("F11",small=1), K("F12",small=1),
 K("INS",small=1), K("`"), K("^"), K("+"), K("{"), K("}"),
 K("PGUP",small=1), K("HOME",small=1), K("↑"), K("END",small=1), K("{"), K("}"),
 K("PRINT",small=1), K("~"), K("="), K("−"), K("("), K(")"),
 K("PGDN",small=1), K("←"), K("↓"), K("→"), K("("), K(")"),
 K("PAUSE",small=1), K("\\"), K("|"), K("_"), K("["), K("]"),
 K(T), K(T),
 K("CAPS",small=1), K("OPT+←",small=1), K("ESC",small=1), K("OPT+→",small=1), K("["), K("]"),
 K(T), K(T), K(T), K("L2",small=1), K(T),
 K("•"), K("DEL",small=1), K("ª"), K("º"), K("°"),
]
# ---------- L5: Numérico ----------
L5 = [
 K(T), K(T), K(T), K(T), K(T), K(T),
 K(T), K("NUM LK",small=1), K("/"), K("*"), K("−"), K(T),
 K(T), K(N), K(N), K(N), K(N), K(N),
 K(N), K("7"), K("8"), K("9"), K("+"), K(T),
 K(T), K(N), K(N), K(N), K(N), K(N),
 K(N), K("4"), K("5"), K("6"), K("+"), K(T),
 K(T), K(N), K(N), K(N), K(N), K(N),
 K(T), K(T),
 K(N), K("1"), K("2"), K("3"), K("ENTER",small=1), K(T),
 K("L5",small=1), K(T), K(T), K(T), K(T),
 K(T), K(","), K("0"), K("0"), K("."),
]
assert len(L1)==len(L2)==len(L5)==60
def _arg(name, default=None):
    return next((a.split("=", 1)[1] for a in sys.argv if a.startswith(f"--{name}=")), default)
# Optional local overrides kept out of the repository (same file gen_vil.py takes): relabel keys.
if _arg("overrides"):
    for k in json.load(open(_arg("overrides"))).get("keys", []):
        target = {0: L1, 3: L2, 6: L5}.get(k["layer"])
        if target is not None and k.get("label"): target[k["index"]] = K(k["label"], small=1)
SCALE = float(_arg("scale", "0.8"))      # printed size relative to a full A4 landscape page

def kb(labels, held=None, idp="a", ov2=None, ov5=None):
    head = [f'<svg viewBox="{VIEWBOX}" xmlns="http://www.w3.org/2000/svg" class="kb">',
            f'<defs><pattern id="h{idp}" width="0.18" height="0.18" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="0.09" height="0.18" fill="#555"/></pattern></defs>']
    halves = {"L": [f'<g transform="translate({SPLAY_TX:.3f} 0) rotate({HALF_ANGLE} {PIVOT[0]} {PIVOT[1]})">'],
              "R": [f'<g transform="translate({-SPLAY_TX:.3f} 0) rotate({-HALF_ANGLE} {16 - PIVOT[0]} {PIVOT[1]})">']}
    for i, g in enumerate(GEO):
        x, y = g["x"], g["y"]; h = g.get("h", 1)
        out = halves["L" if x + 0.5 < 8 else "R"]
        lab = labels[i]
        cx, cy = x + 0.5, y + h/2
        rot = ROT.get(i, 0)
        tr = f' transform="rotate({rot} {cx} {cy})"' if rot else ""
        fill = f"url(#h{idp})" if i == held else ("#ffffff" if i in HOME else "#ececec")
        out.append(f'<g{tr}>')
        if i in ENC:
            out.append(f'<circle cx="{cx}" cy="{cy}" r="{KEY/2}" fill="{fill}" stroke="#888" stroke-width="0.03"/>')
        else:
            out.append(f'<rect x="{x+(1-KEY)/2}" y="{y+(1-KEY)/2}" width="{KEY}" height="{h-(1-KEY)}" rx="0.12" fill="{fill}" stroke="#888" stroke-width="0.03"/>')
        m, s, small = lab["m"], lab["s"], lab["small"]
        if i == held:
            out.append(f'<rect x="{cx-0.3}" y="{cy-0.16}" width="0.6" height="0.32" rx="0.05" fill="#fff" stroke="#555" stroke-width="0.02"/><text x="{cx}" y="{cy}" class="t sm">{html.escape(m)}</text>')
        elif m == T:
            out.append(f'<text x="{cx}" y="{cy}" class="t tr">{T}</text>')
        elif m and ov2 is not None and i not in ENC:
            cls = "t q-sm" if small else "t q"
            out.append(f'<text x="{cx-0.04}" y="{cy+0.06}" class="{cls}">{html.escape(m)}</text>')
            if s and i != 50:
                out.append(f'<text x="{x+0.15}" y="{y+0.21}" class="t q-x" text-anchor="start">{html.escape(s)}</text>')
        elif m:
            cls = "t sm" if small else "t"
            if s:
                scls = "t xs" if small else "t sm"
                out.append(f'<text x="{cx}" y="{cy-0.17}" class="{cls}">{html.escape(m)}</text>')
                out.append(f'<text x="{cx}" y="{cy+0.2}" class="{scls}">{html.escape(s)}</text>')
            else:
                out.append(f'<text x="{cx}" y="{cy}" class="{cls}">{html.escape(m)}</text>')
        if i in DOTS:
            for dx in (-0.12, 0, 0.12):
                out.append(f'<circle cx="{cx+dx}" cy="{cy+0.3}" r="0.03" fill="#111"/>')
        for ov, cls, yy in ((ov2, "t o2", y+0.21), (ov5, "t o5", y+h-0.19)):
            if ov is None or i == held or i in ENC: continue
            o = ov[i]["m"]
            if o and o != T and o != m:
                fs = 0.16 if len(o) <= 2 else (0.11 if len(o) <= 4 else 0.085)
                tl = f' textLength="{min(len(o)*fs*0.62, 0.46):.2f}" lengthAdjust="spacingAndGlyphs"' if len(o) >= 3 else ''
                out.append(f'<text x="{x+0.82}" y="{yy}" class="{cls}" style="font-size:{fs}px" text-anchor="end"{tl}>{html.escape(o)}</text>')
        out.append('</g>')
    return "\n".join(head + halves["L"] + ['</g>'] + halves["R"] + ['</g>', '</svg>'])

CSS = """
@page { size: A4 landscape; margin: 7mm 8mm; }
html,body{margin:0;padding:0;background:#fff}
body{font-family:Menlo,"DejaVu Sans Mono",monospace;color:#111;width:281mm;height:196mm;display:flex;flex-direction:column;zoom:__SCALE__;margin:0 auto}
h2{font-size:3.6mm;font-weight:normal;margin:0 0 1mm 0;letter-spacing:0.1mm}
h2 b{font-weight:bold;font-size:5mm;margin-right:3mm}
.top{height:110mm;display:flex;flex-direction:column}
.bottom{height:69mm;display:flex;gap:5mm;margin-top:1mm;border-top:0.3mm dashed #bbb;padding-top:1.5mm}
.half{flex:1;display:flex;flex-direction:column;min-width:0;justify-content:flex-start}
.kb{flex:1;width:100%;height:auto;max-height:100%}
.top .kb{max-height:102mm;margin:0 auto}
.bottom .kb{flex:0 0 auto;max-height:60mm}
.t{text-anchor:middle;dominant-baseline:central;font-family:Menlo,"DejaVu Sans Mono",monospace;font-size:0.34px;fill:#111}
.t.sm{font-size:0.2px} .t.xs{font-size:0.15px} .t.tr{fill:#777;font-size:0.3px}
.t.o2{fill:#111} .t.o5{fill:#777}
.t.q{font-size:0.3px} .t.q-sm{font-size:0.17px} .t.q-x{font-size:0.13px;fill:#444}
.combo .top{height:160mm} .combo .top .kb{max-height:136mm} .combo .bottom{display:none}
h2.below{margin:4mm 0 0 0}
.notes{font-size:2.7mm;color:#333;margin:3mm 0 0 0;padding-top:1mm;display:flex;gap:6mm;flex-wrap:wrap}
.notes span b{font-weight:bold}
"""
CSS = CSS.replace("__SCALE__", str(SCALE))
HTML = f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Cola Tergo Sofle · Graphite-PT</title><style>{CSS}</style></head><body class="{'combo' if COMBO else ''}">
<div class="top">
{'' if COMBO else '''<h2><b>L1</b>Base — Graphite-PT (letras do Graphite com O↔U trocados · sistema em ABNT2):</h2>'''}
{kb(L1, None, "a", L2, L5) if COMBO else kb(L1, None, "a")}
{'''<h2 class="below"><b>L1</b>Base — Graphite-PT (letras do Graphite com O↔U trocados · sistema em ABNT2) · canto superior direito = com L2 segurado · canto inferior direito, cinza = com L5 segurado</h2>''' if COMBO else ''}
</div>
<div class="bottom">
<div class="half"><h2><b>L2</b>Símbolos e Navegação (segurar L2):</h2>{kb(L2, 53, "b")}</div>
<div class="half"><h2><b>L5</b>Numérico (segurar a tecla ^):</h2>{kb(L5, 50, "c")}</div>
</div>
<p class="notes"><span><b>Shift+~</b> = ^</span><span><b>Shift+´</b> = `</span><span><b>Shift+'</b> = "</span><span><b>L2 + BKSP</b> = DEL</span><span><b>^</b>: toque = ^ · segurar = L5</span><span>Encoder L4: girar = scroll horizontal</span><span>Encoder L3: girar = zoom − / + · clique rápido = zoom 100% · segurar = camada 3</span></p>
</body></html>"""
OUT = Path(_arg("outdir", ROOT / "cheatsheet")) / ("cheatsheet-combined.html" if COMBO else "cheatsheet.html")
open(OUT,"w").write(HTML)
print("ok", len(HTML))
