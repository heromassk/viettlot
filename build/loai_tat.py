import sys, os, json, itertools
B=r'C:\Users\User\OneDrive\Desktop\viettlot-main\build'; sys.path.insert(0,B); os.chdir(B)
GAME=sys.argv[1]; sys.argv=['pool_chon.py',GAME]
os.environ['KS']='12,15,18'
src=open('pool_chon.py',encoding='utf-8').read(); src=src[:src.index("print(f'## ")]
g={'__file__':os.path.join(B,'pool_chon.py'),'__name__':'x'}; exec(compile(src,'pool_chon.py','exec'),g)
GY,TS,R,T,NB,NUMS,SIG=g['GY'],g['TS'],g['R'],g['T'],g['NB'],g['NUMS'],g['SIG']
PC=json.load(open('pool_chon.json',encoding='utf-8'))[GAME]
def sc(st): return (st['50'][1]*2+st['100'][1], st['50'][0]*2+st['100'][0])
CH={}
for K in ('12','15','18'):
    a,b=PC['stat'].get(K),PC.get('stat50',{}).get(K)
    CH[int(K)]=[tuple(x) for x in (PC['chon50'][K] if a and b and sc(b)>sc(a) else PC['chon'][K])]
KEYS=['vang']+list(GY['LOAI'][GAME])
def pool(t,K,off):
    e={}
    for nm,w in CH[K]:
        for n in NUMS[t].get(nm,()): e[n]=e.get(n,0)+w
    f,s=SIG[t]; s2=dict(s)
    for k in off: s2[k]=set()
    return GY['pool_of'](GY['score'](f,s2,e),s2,K)
def stat(off,K):
    P={t:pool(t,K,off) for t in TS}; o=[]
    for W in (50,100):
        hs=[len(set(P[t])&set(R[t])) for t in range(T-W,T)]; o+=[sum(h>=3 for h in hs)*100//W,sum(h>=4 for h in hs)*100//W,round(sum(hs)/W,2)]
    return o
V=[('Đang dùng (không tắt cách nào)',())]+[(f'Tắt: {k}',(k,)) for k in KEYS]+[('Tắt cả '+str(len(KEYS)),tuple(KEYS))]
print(GAME,'cỡ pool: 12 / 15 / 18 — mỗi ô: ≥3 · ≥4 · TB số trúng (50 kỳ | 100 kỳ)')
for lab,off in V:
    print(f'| {lab} | '+' | '.join(f'{K}: '+' '.join(map(str,stat(off,K)[:3]))+' | '+' '.join(map(str,stat(off,K)[3:])) for K in (12,15,18))+' |')
