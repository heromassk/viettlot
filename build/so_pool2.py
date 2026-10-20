# So nhóm "Có mặt ≥2 pool" (bảng pool trong app) với pool của app (pool_thuc.json, chấm lùi 100 kỳ) — anh 20/10/2026.
import json,itertools
ALL=json.load(open('build/all_data.json'));PT=json.load(open('build/pool_thuc.json'))
def nh(R,t,NB,X):
    pv,pv2=R[t-1],R[t-2]
    seen=set().union(*R[t-X:t]);vang={n for n in range(1,NB+1) if n not in seen}
    T={a+b for a,b in itertools.combinations(pv,2) if a+b<=NB};H={abs(a-b) for a,b in itertools.combinations(pv,2)}
    ke=lambda S:{m for n in S for m in (n-1,n+1) if 1<=m<=NB and m not in S}
    kep=lambda S:{a+1 for a in S if a+2 in S and a+1 not in S}
    kp=kep(pv)|{n for n in kep(pv2) if n not in pv}
    C={}
    for S in (vang,T,H,ke(pv),ke(pv2),set(pv),kp):
        for n in S:C[n]=C.get(n,0)+1
    return {n for n in C if C[n]>=2},{n for n in C if C[n]>=3}
for key,g,NB,X in [('loto535','loto',35,8),('mega645','mega',45,8),('power655','power',55,12)]:
    R=[set(r) for r in ALL[key]['res']];DT=ALL[key]['dates'];P=PT[g];den=DT.index(P['den']);T=den+1
    hits=P['hits']
    print(f"\n## {g} (100 kỳ đến {P['den']})")
    for W in (50,100):
        a=[nh(R,t,NB,X) for t in range(T-W,T)];h2=[len(x[0]&R[t]) for x,t in zip(a,range(T-W,T))];sz=sum(len(x[0]) for x in a)/W
        h3=[len(x[1]&R[t]) for x,t in zip(a,range(T-W,T))];sz3=sum(len(x[1]) for x in a)/W
        f=lambda h,m:sum(v>=m for v in h)
        print(f"{W} kỳ | ≥2 pool: cỡ {sz:.1f} TB {sum(h2)/W:.2f} ≥2 {f(h2,2)} ≥3 {f(h2,3)} ≥4 {f(h2,4)} | ≥3 pool: cỡ {sz3:.1f} TB {sum(h3)/W:.2f} ≥1 {f(h3,1)} ≥2 {f(h3,2)}")
        for K in ('10','12','15','18','20'):
            if K in hits:
                hh=hits[K][-W:];print(f"      app pool {K}: TB {sum(hh)/W:.2f} ≥2 {f(hh,2)} ≥3 {f(hh,3)} ≥4 {f(hh,4)}")
