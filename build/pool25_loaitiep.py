# Thử loại tiếp trong Pool 25 Power (anh 10/10/2026): bỏ k số điểm thấp theo 291 cách + luật sổ kiểm chứng. python3 build/pool25_loaitiep.py
import sys, json, importlib.util, numpy as np
sys.path.insert(0,'build')
sp=importlib.util.spec_from_file_location('p25','build/pool25_power.py'); P25=importlib.util.module_from_spec(sp)
import io,contextlib
with contextlib.redirect_stdout(io.StringIO()): sp.loader.exec_module(P25)
POOLX={e['t']:e['p'] for e in P25.rec}
__file__='/home/user/viettlot/build/pool25_quet.py'; sys.argv=['x','power']
exec(open(__file__).read().split("Y = P[ts]")[0])
POOL=POOLX; R=P25.R; T=P25.T
ts100=list(range(T-100,T))
def ev(keep):   # keep: t-> set
    h=np.array([len(keep[t]&R[t]) for t in ts100]); sz=np.mean([len(keep[t]) for t in ts100])
    return h,sz
base=ev({t:set(POOL[t]) for t in ts100})
f4=lambda h:np.mean(h>=4)*100; f3=lambda h:np.mean(h>=3)*100
out=[]
# 1) cắt bớt k số điểm thấp nhất trong pool theo từng phương pháp
for name,f in M.items():
    S={t:f(t) for t in ts100}
    for drop in (5,7,10):
        keep={t:set(sorted(POOL[t],key=lambda n:S[t][n-1])[drop:]) for t in ts100}
        h,sz=ev(keep); out.append((f'Bỏ {drop} số thấp nhất theo "{name}"',h,sz))
# 2) luật loại trong sổ kiểm chứng
import theodoi as TD
C={t:TD.ctx(R,55,t) for t in ts100}
for i,l,f in TD.RULES:
    try: keep={t:set(POOL[t])-set(f(R,t,C[t])) for t in ts100}
    except Exception: continue
    h,sz=ev(keep)
    if sz<25: out.append((f'Luật sổ: {l}',h,sz))
print('Pool 25 gốc: ≥4 %.0f%% ≥3 %.0f%% (hai nửa ≥4 %.0f·%.0f%%)'%(f4(base[0]),f3(base[0]),f4(base[0][:50]),f4(base[0][50:])))
for sz in (20,18,15):
    cand=[x for x in out if abs(x[2]-sz)<=0.6 or (sz==20 and 19<=x[2]<=21) or (sz==18 and 17.5<=x[2]<=18.5) or (sz==15 and 14.5<=x[2]<=15.5)]
    cand=sorted(cand,key=lambda x:-min(f4(x[1][:50]),f4(x[1][50:])))[:6]
    print(f'\n### Pool ~{sz} số')
    for k,h,s in cand: print(f'| {k} | {s:.1f} | ≥4 {f4(h):.0f}% (nửa {f4(h[:50]):.0f}·{f4(h[50:]):.0f}) | ≥3 {f3(h):.0f}% |')
rl=[x for x in out if x[0].startswith('Luật sổ')]
print('\n### Luật sổ (bỏ khỏi pool 25)')
for k,h,s in sorted(rl,key=lambda x:-f4(x[1]))[:12]: print(f'| {k} | {s:.1f} | ≥4 {f4(h):.0f}% (nửa {f4(h[:50]):.0f}·{f4(h[50:]):.0f}) | ≥3 {f3(h):.0f}% |')
