# Dấu vết trong pool hiệu (anh 20/10/2026): chia pool hiệu (|a−b| mọi cặp kỳ trước) thành nhóm, so % ra mỗi số của nhóm với phần còn lại của pool.
# Chỉ so trong chính pool hiệu. Khung: Loto 3 đoạn 100 kỳ; Mega/Power 2 nửa 50 kỳ (≤100 kỳ).
import json,itertools
from collections import Counter
ALL=json.load(open('build/all_data.json'))
def feats(prev,NB,prev2,vang8):
    c=Counter(abs(a-b) for a,b in itertools.combinations(prev,2));s=sorted(prev)
    adj={s[i+1]-s[i] for i in range(len(s)-1)};H=set(c)
    tong={a+b for a,b in itertools.combinations(prev,2) if a+b<=NB}
    G={'hiệu 2 số liền nhau (khoảng cách)':adj,'hiệu lặp (≥2 cặp ra cùng 1 số)':{n for n in H if c[n]>=2},
       f'hiệu nhỏ (≤{NB//3})':{n for n in H if n<=NB//3},'hiệu trùng số kỳ trước':H&set(prev),
       'hiệu kề ±1 số kỳ trước':{n for n in H if (n-1 in prev or n+1 in prev) and n not in prev},
       'hiệu cũng nằm trong pool tổng':H&tong,'hiệu trùng số kỳ t−2':H&set(prev2),'hiệu đang vắng 8 kỳ':H&vang8}
    return H,G
for key,NB,nm,segs in [('loto535',35,'Loto',[(100,'100 gần'),(200,'đoạn 2'),(300,'đoạn 3')]),('mega645',45,'Mega',[(50,'50 gần'),(100,'50 trước')]),('power655',55,'Power',[(50,'50 gần'),(100,'50 trước')])]:
    R=[set(r) for r in ALL[key]['res']];T=len(R)
    print(f'\n## {nm}  (% ra 1 số trong nhóm / phần còn lại của pool hiệu; [cỡ nhóm TB])')
    acc={}
    for W,lab in segs:
        a,b=T-W,T-W+(100 if nm=='Loto' else 50)
        for t in range(a,b):
            v8=set(range(1,NB+1))-set().union(*R[t-8:t])
            H,G=feats(R[t-1],NB,R[t-2],v8)
            for g,S in G.items():
                x=acc.setdefault(g,{}).setdefault(lab,[0,0,0,0])
                x[0]+=len(S);x[1]+=len(S&R[t]);x[2]+=len(H-S);x[3]+=len((H-S)&R[t])
    n=100 if nm=='Loto' else 50
    for g,d in acc.items():
        print(f'- {g}: '+' | '.join(f"{lab}: {v[1]/max(1,v[0]):.0%} / {v[3]/max(1,v[2]):.0%} [{v[0]/n:.1f}]" for lab,v in d.items()))
    t=T;v8=set(range(1,NB+1))-set().union(*R[t-8:t]);H,G=feats(R[t-1],NB,R[t-2],v8)
    print('  kỳ tới:',' · '.join(f"{g.split(' (')[0]}: {' '.join(f'{x:02d}' for x in sorted(S))}" for g,S in G.items() if S))
