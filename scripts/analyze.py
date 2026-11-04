import sys, unicodedata, collections

LAYOUTS = {
 "QWERTY ABNT2":   ["qwertyuiop", "asdfghjklç", "zxcvbnm,.;"],
 "Colemak ABNT2 (Tiago)": ["qwfpgjluyç", "arstdhneio", "zxcvbkm,.;"],
 "Colemak-DH":     ["qwfpbjluyç", "arstgmneio", "zxcdvkh,./"],
 "BR Nativo":      ["/,.hxwltcp", "ieaoumdsrn", "yçjbkqvgfz"],
 "Dvorak":         ["',.pyfgcrl", "aoeuidhtns", ";qjkxbmwvz"],
 "ENIAC GA 2020":  ["zgscveawuj", "dnmptkyçhi", "lbfrq  xo "],
 "Gallium v2":     ["bldcvjyouç", "nrtsgphaei", "xqmwzkf';."],
 "Graphite":       ["bldwz'fouç", "nrtsgyhaei", "qxmcvkp.-/"],
 "Graphite-PT (o<->u)": ["bldwz'fuoj", "nrtsgyhaeiç", "qxmcvkp.,/"],
 "Graphite-PT 5 swaps": ["bldwz'fqoy", "hrtsgjnaeiu", "çxmcvkp.,/"],
 "Canary":         ["wlypkzxouç", "crstbfneia", "jvdgqmh/,."],
}
FING = ["LP","LR","LM","LI","LI","RI","RI","RM","RR","RP","RP"]
HAND = lambda c: "L" if c < 5 else "R"

def pos(layout):
    p = {}
    for r, row in enumerate(layout):
        for c, ch in enumerate(row):
            if ch.strip():
                p.setdefault(ch, (r, c))
    return p

def norm(text):
    out = []
    acc = collections.Counter()
    names = {"\u0301":"agudo ´","\u0300":"grave `","\u0302":"circunflexo ^","\u0303":"til ~","\u0308":"trema ¨"}
    for ch in text.lower():
        if ch == "ç":
            out.append("ç"); continue
        d = unicodedata.normalize("NFD", ch)
        base = d[0]
        for m in d[1:]:
            if m in names: acc[names[m]] += 1
        out.append(base if ("a" <= base <= "z") else " ")
    return "".join(out), acc

def evaluate(text, layout):
    p = pos(layout)
    letters = 0; home = 0; pinky = 0; left = 0
    alt = 0; sfb = 0; lsb = 0; rin = 0; rout = 0; bigr = 0
    rows = [0,0,0]
    prev = None
    for ch in text:
        if ch not in p:
            prev = None; continue
        r, c = p[ch]
        letters += 1; rows[r] += 1
        if r == 1: home += 1
        if FING[c] in ("LP","RP"): pinky += 1
        if HAND(c) == "L": left += 1
        if prev:
            pr, pc = prev; bigr += 1
            if HAND(pc) != HAND(c):
                alt += 1
            else:
                if FING[pc] == FING[c] and (pr, pc) != (r, c): sfb += 1
                elif {pc, c} in ({2,4},{5,7}): lsb += 1
                elif FING[pc] != FING[c]:
                    order = ["LP","LR","LM","LI","RI","RM","RR","RP"]
                    a, b = order.index(FING[pc]), order.index(FING[c])
                    inward = (b > a) if HAND(c) == "L" else (b < a)
                    if abs(a-b) == 1: 
                        if inward: rin += 1
                        else: rout += 1
        prev = (r, c)
    pct = lambda n, d: 100.0*n/d if d else 0
    return dict(home=pct(home,letters), top=pct(rows[0],letters), bottom=pct(rows[2],letters),
                pinky=pct(pinky,letters), left=pct(left,letters), alt=pct(alt,bigr),
                sfb=pct(sfb,bigr), lsb=pct(lsb,bigr), rolls=pct(rin+rout,bigr))

for path in sys.argv[1:]:
    raw = open(path, encoding="utf-8").read()
    text, acc = norm(raw)
    n = sum(1 for ch in text if ch != " ")
    print(f"\n== {path}  ({n} letras)")
    if acc:
        tot = sum(acc.values())
        print("acentos por 100 letras: " + ", ".join(f"{k} {100*v/n:.2f}" for k, v in acc.most_common()))
        print(f"total acentos {100*tot/n:.2f}/100 letras; ç {100*text.count('ç')/n:.2f}/100")
    print(f"{'layout':24s} {'home%':>6s} {'top%':>5s} {'bot%':>5s} {'pinky%':>7s} {'esq%':>5s} {'altern%':>8s} {'SFB%':>5s} {'LSB%':>5s} {'rolls%':>7s}")
    for name, lay in LAYOUTS.items():
        m = evaluate(text, lay)
        print(f"{name:24s} {m['home']:6.1f} {m['top']:5.1f} {m['bottom']:5.1f} {m['pinky']:7.1f} {m['left']:5.1f} {m['alt']:8.1f} {m['sfb']:5.2f} {m['lsb']:5.2f} {m['rolls']:7.1f}")
