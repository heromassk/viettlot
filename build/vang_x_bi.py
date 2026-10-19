# Pool "số đang vắng x kỳ" trên Mega / Power (anh 19/10/2026). Bi thay 1–2 tháng/lần → chỉ chấm trong 100 kỳ gần, khung 10/20/50/100 + 2 nửa 50 kỳ.
# Mỗi kỳ t: V = số không ra trong x kỳ liền trước t. "lệch" = % ra của 1 số vắng − % ra của 1 số đã ra (điểm %).
import json,sys
ALL=json.load(open('build/all_data.json'))
for key,NB,KB,nm in [('mega645',45,6,'Mega 6/45'),('power655',55,6,'Power 6/55')]:
    R=[set(r) for r in ALL[key]['res']];DT=ALL[key]['dates'];T=len(R)
    def st(x,ts):
        n=sz=h=g=[0]*0 or 0;sz=h=0;g=[0]*5;szo=0
        for t in ts:
            V=set(range(1,NB+1))-set().union(*R[t-x:t]);k=len(R[t]&V);n+=1;sz+=len(V);h+=k;szo+=NB-len(V)
            for j in range(1,5):g[j]+=k>=j
        return dict(sz=sz/n,tb=h/n,g=[v/n for v in g],d=(h/sz-(KB*n-h)/szo)*100 if sz else 0)
    print(f'\n## {nm}  ({DT[T-100]} → {DT[-1]})')
    print('x | cỡ nhóm | trúng TB (100) | ≥1/≥2/≥3 (100 kỳ) | lệch 10 / 20 / 50 / 100 | lệch nửa xa / nửa gần | kỳ tới')
    for x in [3,4,5,6,7,8,9,10,12,15]:
        w={W:st(x,range(T-W,T)) for W in (10,20,50,100)};h1=st(x,range(T-100,T-50));h2=w[50]
        nx=sorted(set(range(1,NB+1))-set().union(*R[T-x:T]))
        print(f'{x:>2} | {w[100]["sz"]:.1f} | {w[100]["tb"]:.2f} | '+'/'.join(f'{v:.0%}' for v in w[100]['g'][1:4])+' | '+' / '.join(f'{w[W]["d"]:+.1f}' for W in (10,20,50,100))+f' | {h1["d"]:+.1f} / {h2["d"]:+.1f} | {len(nx)} số: '+' '.join(f'{n:02d}' for n in nx))
