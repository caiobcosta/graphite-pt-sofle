import sys, collections, importlib.util
spec = importlib.util.spec_from_file_location("a", "analyze.py"); 
src = open("analyze.py").read().split("for path in sys.argv")[0]
ns = {}; exec(src, ns)
text, _ = ns["norm"](open(sys.argv[1], encoding="utf-8").read())
names = sys.argv[2:]
for name in names:
    lay = ns["LAYOUTS"][name]; p = ns["pos"](lay); FING = ns["FING"]
    c = collections.Counter(); prev=None; big=0
    for ch in text:
        if ch not in p: prev=None; continue
        if prev and FING[p[prev][1]]==FING[p[ch][1]] and prev!=ch: c["".join(sorted(prev+ch))]+=1
        if prev: big+=1
        prev=ch
    print(name, " ".join(f"{k}:{100*v/big:.2f}" for k,v in c.most_common(8)))
