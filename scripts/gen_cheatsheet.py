import json, html, sys
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
SOFLE_GEO = ("https://raw.githubusercontent.com/qmk/qmk_firmware/master/keyboards/sofle/rev1/keyboard.json", "sofle_rev1_keyboard.json")
VIAL_KC = ("https://raw.githubusercontent.com/vial-kb/vial-gui/main/src/main/python/keycodes/keycodes.py", "vial_keycodes.py")
VIAL_ANY = ("https://raw.githubusercontent.com/vial-kb/vial-gui/main/src/main/python/any_keycode.py", "vial_any_keycode.py")
GEO = json.load(open(fetch(*SOFLE_GEO)))["layouts"]["LAYOUT"]["layout"]
ENC = {42, 43}
ROT = {53: 10, 54: 25, 55: -25, 56: -10}   # degrees, mimicking the Tergo sheet
KEY = 0.92

T = "▽"      # transparent
N = ""       # no-op

def K(main, shift=None, small=False):
    return {"m": main, "s": shift, "small": small}

# ---------- L1: Graphite-PT (ABNT2) ----------
L1 = [
 K("ESC",small=1), K("1","!"), K("2","@"), K("3","#"), K("4","$"), K("5","%"),
 K("6","¨"), K("7","&"), K("8","*"), K("9","("), K("0",")"), K("-","_"),
 K("TAB",small=1), K("B"), K("L"), K("D"), K("V"), K("Z"),
 K("'",'"'), K("F"), K("U"), K("O"), K("J"), K("=","+"),
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

def kb(labels, held=None, idp="a", ov2=None, ov5=None, clip=None):
    vb = {"L": "-0.1 -0.1 7.5 6.2", "R": "9.3 -0.1 7.4 6.2"}.get(clip, "-0.1 -0.1 16.7 6.2")
    out = [f'<svg viewBox="{vb}" xmlns="http://www.w3.org/2000/svg" class="kb">',
           f'<defs><pattern id="h{idp}" width="0.18" height="0.18" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="0.09" height="0.18" fill="#555"/></pattern></defs>']
    for i, g in enumerate(GEO):
        x, y = g["x"], g["y"]; h = g.get("h", 1)
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
    out.append('</svg>')
    return "\n".join(out)

CSS = """
@page { size: A4 landscape; margin: 7mm 8mm; }
html,body{margin:0;padding:0;background:#fff}
body{font-family:Menlo,"DejaVu Sans Mono",monospace;color:#111;width:281mm;height:196mm;display:flex;flex-direction:column}
h2{font-size:3.6mm;font-weight:normal;margin:0 0 1mm 0;letter-spacing:0.1mm}
h2 b{font-weight:bold;font-size:5mm;margin-right:3mm}
.top{height:104mm;display:flex;flex-direction:column}
.bottom{height:80mm;display:flex;gap:5mm;margin-top:1mm;border-top:0.3mm dashed #bbb;padding-top:1.5mm}
.half{flex:1;display:flex;flex-direction:column;min-width:0;justify-content:flex-start}
.kb{flex:1;width:100%;height:auto;max-height:100%}
.top .kb{max-height:96mm;margin:0 auto}
.bottom .kb{flex:0 0 auto;max-height:70mm}
.t{text-anchor:middle;dominant-baseline:central;font-family:Menlo,"DejaVu Sans Mono",monospace;font-size:0.34px;fill:#111}
.t.sm{font-size:0.2px} .t.xs{font-size:0.15px} .t.tr{fill:#777;font-size:0.3px}
.t.o2{fill:#111} .t.o5{fill:#777}
.t.q{font-size:0.3px} .t.q-sm{font-size:0.17px} .t.q-x{font-size:0.13px;fill:#444}
.combo .top{height:150mm} .combo .bottom{display:none}
.halves{display:flex;gap:4mm;height:113mm;justify-content:center;margin-top:1mm}
h2.below{margin:4mm 0 0 0}
.halves .kb{height:100%;width:auto;flex:0 0 auto;max-height:none;margin:0}
.notes{font-size:2.7mm;color:#333;margin:3mm 0 0 0;padding-top:1mm;display:flex;gap:6mm;flex-wrap:wrap}
.notes span b{font-weight:bold}
"""
HTML = f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Cola Tergo Sofle · Graphite-PT</title><style>{CSS}</style></head><body class="{'combo' if COMBO else ''}">
<div class="top">
{'' if COMBO else '''<h2><b>L1</b>Base — Graphite-PT (letras do Graphite com O↔U trocados · sistema em ABNT2):</h2>'''}
{('<div class="halves">' + kb(L1, None, "a", L2, L5, "L") + kb(L1, None, "b", L2, L5, "R") + '</div>') if COMBO else kb(L1, None, "a")}
{'''<h2 class="below"><b>L1</b>Base — Graphite-PT (letras do Graphite com O↔U trocados · sistema em ABNT2) · canto superior direito = com L2 segurado · canto inferior direito, cinza = com L5 segurado</h2>''' if COMBO else ''}
</div>
<div class="bottom">
<div class="half"><h2><b>L2</b>Símbolos e Navegação (segurar L2):</h2>{kb(L2, 53, "b")}</div>
<div class="half"><h2><b>L5</b>Numérico (segurar a tecla ^):</h2>{kb(L5, 50, "c")}</div>
</div>
<p class="notes"><span><b>Shift+~</b> = ^</span><span><b>Shift+´</b> = `</span><span><b>Shift+'</b> = "</span><span><b>L2 + BKSP</b> = DEL</span><span><b>^</b>: toque = ^ · segurar = L5</span><span>Encoder L4: girar = scroll horizontal</span><span>Encoder L3: girar = zoom − / + · clique rápido = zoom 100% · segurar = camada 3</span></p>
</body></html>"""
OUT = ROOT / "cheatsheet" / ("cheatsheet-combined.html" if COMBO else "cheatsheet.html")
open(OUT,"w").write(HTML)
print("ok", len(HTML))
