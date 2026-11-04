import sys, collections
src = open("analyze.py").read().split("for path in sys.argv")[0]
ns = {}; exec(src, ns)
norm, evaluate, pos = ns["norm"], ns["evaluate"], ns["pos"]
pt,_ = norm(open("corpus/pt.txt",encoding="utf-8").read())
en,_ = norm(open("corpus/en.txt",encoding="utf-8").read())
pt = pt[:600000]; en = en[:300000]

def J(lay):
    a = evaluate(pt, lay); b = evaluate(en, lay)
    return (a["sfb"] + 0.6*b["sfb"] + 0.3*a["lsb"] + 0.2*b["lsb"]
            + 0.02*(100-a["home"]) + 0.01*(100-b["home"])
            + 0.03*max(0,a["pinky"]-16) + 0.03*max(0,b["pinky"]-16)
            - 0.01*a["alt"])

def swap(lay, p1, p2):
    g = [list(r) for r in lay]
    (r1,c1),(r2,c2) = p1,p2
    g[r1][c1], g[r2][c2] = g[r2][c2], g[r1][c1]
    return ["".join(r) for r in g]

base = ["bldwz'fouj", "nrtsgyhaei,", "qxmcvkp.-/"]
# ç no mindinho direito externo (home), ',' vai para a fileira de baixo
base = ["bldwz'fouj", "nrtsgyhaeiç", "qxmcvkp.,/"]
cur = base; best = J(cur); print("Graphite base J=%.3f"%best)
cells = [(r,c) for r,row in enumerate(base) for c,_ in enumerate(row)]
for step in range(5):
    cand = None
    for i in range(len(cells)):
        for j in range(i+1,len(cells)):
            l = swap(cur, cells[i], cells[j]); v = J(l)
            if v < best - 1e-4 and (cand is None or v < cand[0]): cand = (v, l, cells[i], cells[j])
    if not cand: break
    best, cur, a, b = cand
    print(f"swap {cur[a[0]][a[1]]}<->{cur[b[0]][b[1]]} at {a},{b}  J={best:.3f}")
    print("  ", " / ".join(cur))
print("FINAL"); print("\n".join(cur))
for name,t in (("pt",pt),("en",en)):
    m = evaluate(t, cur); print(name, {k:round(v,2) for k,v in m.items()})
