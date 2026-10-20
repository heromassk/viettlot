# Số ra ở kỳ mới có hay là số chưa xuất hiện trong 5 kỳ gần nhất? (anh 20/10/2026) — đếm số kỳ khung 20/50/100.
import json
ALL=json.load(open('build/all_data.json'))
for key,NB,KB,nm,modes in [('loto535',35,5,'Loto',[(None,'cả 2 giờ'),('13h','chỉ 13h'),('21h','chỉ 21h')]),('mega645',45,6,'Mega',[(None,'')]),('power655',55,6,'Power',[(None,'')])]:
    R=[set(r) for r in ALL[key]['res']];DT=ALL[key]['dates']
    for flt,lab in modes:
        idx=[i for i in range(len(R)) if flt is None or DT[i].endswith(flt)]
        print(f'\n## {nm} {lab}')
        for W in (20,50,100):
            ks=idx[-W:];m=[];szV=szO=hV=hO=0
            for k in ks:
                p=idx.index(k);prev=set().union(*[R[i] for i in idx[p-5:p]]);V=set(range(1,NB+1))-prev
                x=len(R[k]&V);m.append(x);szV+=len(V);szO+=NB-len(V);hV+=x;hO+=KB-x
            dist={j:sum(v==j for v in m) for j in range(KB+1)}
            print(f'{W} kỳ: số "mới" TB {sum(m)/W:.1f}/{KB} · phân bố '+' '.join(f'{j}:{dist[j]}' for j in range(KB+1) if dist[j])+f' · kỳ ≥3 số mới {sum(v>=3 for v in m)} · nhóm chưa ra 5 kỳ ~{szV/W:.0f} số, 1 số ra {hV/szV:.1%} | nhóm đã ra ~{szO/W:.0f} số, 1 số ra {hO/szO:.1%}')
