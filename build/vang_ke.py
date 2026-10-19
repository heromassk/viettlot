# Kết hợp số vắng x kỳ với số kề ±1 của kỳ trước / 2 kỳ trước (anh 19/10/2026).
# Mỗi kỳ t: A = vắng x kỳ; K = {n±1 : n thuộc kỳ tham chiếu}. Chấm nhóm A∩K và A\K: cỡ TB, % ra của 1 số, kỳ có ≥1 số.
import json
ALL=json.load(open('build/all_data.json'))
CF=[('loto535',35,5,8,'Loto',[(100,'100 kỳ'),(200,'đoạn 2'),(300,'đoạn 3')]),('mega645',45,6,8,'Mega',[(50,'50 kỳ'),(100,'100 kỳ')]),('power655',55,6,12,'Power',[(50,'50 kỳ'),(100,'100 kỳ')])]
for key,NB,KB,X,nm,wins in CF:
    R=[set(r) for r in ALL[key]['res']];T=len(R);base=KB/NB
    def ke(S):return {m for n in S for m in (n-1,n+1) if 1<=m<=NB}
    REF={'±1 kỳ trước':lambda t:ke(R[t-1]),'±1 kỳ t−2':lambda t:ke(R[t-2]),'±1 kỳ trước hoặc t−2':lambda t:ke(R[t-1]|R[t-2])}
    print(f'\n## {nm} (vắng {X} kỳ; 1 số trung bình ra {base:.1%}/kỳ)')
    for rn,rf in REF.items():
        line=[]
        for w,lab in wins:
            a,b=(T-w,T) if lab.endswith('kỳ') else (T-w,T-w+100)
            s=dict(gs=0,gh=0,g1=0,os=0,oh=0,ks=0,kh=0)
            for t in range(a,b):
                A=set(range(1,NB+1))-set().union(*R[t-X:t]);K=rf(t);G=A&K;O=A-K;K2=K-A
                s['gs']+=len(G);s['gh']+=len(G&R[t]);s['g1']+=bool(G&R[t]);s['os']+=len(O);s['oh']+=len(O&R[t]);s['ks']+=len(K2);s['kh']+=len(K2&R[t])
            n=b-a
            line.append(f"{lab}: giao {s['gs']/n:.1f} số ra {s['gh']/max(1,s['gs']):.1%} (≥1: {s['g1']/n:.0%}) · vắng không kề {s['oh']/max(1,s['os']):.1%} · kề không vắng {s['kh']/max(1,s['ks']):.1%}")
        print(f'- {rn}: '+' | '.join(line))
    t=T;A=set(range(1,NB+1))-set().union(*R[t-X:t])
    for rn,rf in REF.items():print(f'  kỳ tới, {rn}: '+' '.join(f'{n:02d}' for n in sorted(A&rf(t))))
