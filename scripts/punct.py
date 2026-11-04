import sys, unicodedata, collections
def norm(t):
    out=[]
    for ch in t.lower():
        if ch=='ç': out.append('ç'); continue
        d=unicodedata.normalize('NFD',ch)
        b=d[0]
        if 'a'<=b<='z' or b in ",.-/;'": out.append(b)
        else: out.append(' ')
    return ''.join(out)
# finger per key, right half cols: 0,1=RI 2=RM 3=RR 4=RP 5=RP(outer)
LEFT={'b':'LR','l':'LM','d':'LI','w':'LI','z':'LI','n':'LR','r':'LM','t':'LI','s':'LI','g':'LI','q':'LR','x':'LM','m':'LI','c':'LI','v':'LI','ç':'LP'}
# wait: left cols 1..5 -> LP? No: col0 outer=LP, col1=LP? Sofle left: col0 (TAB/SHIFT/Ç)=pinky, col1=pinky, col2=ring, col3=middle, col4=index, col5=index
LEFT={'b':'LP','l':'LR','d':'LM','w':'LI','z':'LI','n':'LP','r':'LR','t':'LM','s':'LI','g':'LI','q':'LP','x':'LR','m':'LM','c':'LI','v':'LI','ç':'LP'}
RIGHTBASE={"'":'RI','f':'RI','u':'RM','o':'RR','j':'RP','y':'RI','h':'RI','a':'RM','e':'RR','i':'RP','k':'RI','p':'RI'}
CANDS={
 'atual  (, outer-home | . RM  - RR  / RP)': {',':'RP','.':'RM','-':'RR','/':'RP'},
 'B      (- outer-home | , RM  . RR  / RP)': {'-':'RP',',':'RM','.':'RR','/':'RP'},
 'C      (- outer-home | . RM  , RR  / RP)': {'-':'RP','.':'RM',',':'RR','/':'RP'},
 'D      (shift outer  | , RM  . RR  - RP)': {',':'RM','.':'RR','-':'RP'},
 'E      (shift outer  | . RM  , RR  - RP)': {'.':'RM',',':'RR','-':'RP'},
 'F      (shift outer  | , RI? no: . RM , RP - RR)': {'.':'RM',',':'RP','-':'RR'},
}
for path in sys.argv[1:]:
    t=norm(open(path,encoding='utf-8',errors='ignore').read())
    n=sum(1 for c in t if c!=' ')
    cnt=collections.Counter(c for c in t if c in ",.-/;'")
    print(path, 'per 100 chars:', {k:round(v*100/n,2) for k,v in cnt.items()})
    big=collections.Counter()
    for a,b in zip(t,t[1:]):
        if a!=' ' and b!=' ': big[a+b]+=1
    tot=sum(big.values())
    for name,c in CANDS.items():
        F={**LEFT,**RIGHTBASE,**c}
        sfb=0; worst=collections.Counter()
        for bg,v in big.items():
            a,b=bg
            if a in F and b in F and a!=b and F[a]==F[b] and (a in ",.-/" or b in ",.-/"):
                sfb+=v; worst[bg]+=v
        print(f'  {name}: punct-SFB {sfb*100/tot:.3f}%  top {[(k,round(v*100/tot,3)) for k,v in worst.most_common(4)]}')
