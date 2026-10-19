# Kiểm ý anh (19/10/2026): pool = các số KHÔNG ra trong x kỳ gần nhất ("đang vắng") có phải tiềm năng?
# Mỗi kỳ t: V = số không có mặt trong x kỳ trước t. Đếm kết quả kỳ t có mấy số trong V.
# Chấm: tỉ lệ ra của 1 số trong V so với 1 số ngoài V (số đã ra trong x kỳ), khung 10/20/50/100 + 3 đoạn 100 kỳ.
import json,sys
D=json.load(open('build/all_data.json'))['loto535'];R=[set(r) for r in D['res']];DT=D['dates'];N=35
def vang(t,x,ses=None):
    idx=[i for i in range(t-1,-1,-1) if ses is None or DT[i].endswith(ses)][:x]
    if len(idx)<x:return None
    seen=set().union(*[R[i] for i in idx]);return set(range(1,N+1))-seen
def cham(ts,x,ses_mode):
    a=dict(n=0,sz=0,hit=0,g1=0,g2=0,g3=0,inV=0,outV=0,szo=0)
    for t in ts:
        ses=DT[t][-3:] if ses_mode else None
        V=vang(t,x,ses)
        if V is None:continue
        h=len(R[t]&V);a['n']+=1;a['sz']+=len(V);a['hit']+=h;a['g1']+=h>=1;a['g2']+=h>=2;a['g3']+=h>=3
        a['inV']+=h;a['outV']+=5-h;a['szo']+=N-len(V)
    n=a['n'];rv=a['inV']/a['sz'];ro=a['outV']/a['szo']
    return dict(n=n,sz=a['sz']/n,tb=a['hit']/n,g1=a['g1']/n,g2=a['g2']/n,g3=a['g3']/n,rv=rv,ro=ro)
T=len(R)
print('Số kỳ:',T,DT[0],'→',DT[-1])
for ses_mode,nm in [(False,'x kỳ liền nhau (13h+21h)'),(True,'x kỳ cùng giờ')]:
  print('\n##',nm)
  for x in [5,10,15,20]:
    print(f'\nx={x}: khung | cỡ pool vắng TB | trúng TB | ≥1 | ≥2 | ≥3 | 1 số vắng ra % / 1 số đã ra %')
    for w in [10,20,50,100]:
        s=cham(range(T-w,T),x,ses_mode);print(f'  {w:>3} kỳ | {s["sz"]:.1f} | {s["tb"]:.2f} | {s["g1"]:.0%} | {s["g2"]:.0%} | {s["g3"]:.0%} | {s["rv"]:.1%} / {s["ro"]:.1%}')
    for k in range(3):
        a,b=T-100*(k+1),T-100*k;s=cham(range(a,b),x,ses_mode)
        print(f'  đoạn {k+1} ({DT[a][:5]}–{DT[b-1][:5]}) | {s["sz"]:.1f} | {s["tb"]:.2f} | {s["g1"]:.0%} | {s["g2"]:.0%} | {s["g3"]:.0%} | {s["rv"]:.1%} / {s["ro"]:.1%}')
    s=cham(range(100,T),x,ses_mode);print(f'  toàn bộ {s["n"]} kỳ | {s["sz"]:.1f} | {s["tb"]:.2f} | {s["g1"]:.0%} | {s["g2"]:.0%} | {s["g3"]:.0%} | {s["rv"]:.1%} / {s["ro"]:.1%}')
print('\n## Các kỳ gần đây: pool vắng 10 kỳ (liền nhau) và số trúng')
for t in range(T-8,T):
    V=vang(t,10);print(DT[t],sorted(R[t]),'| vắng10:',len(V),'số | trúng',sorted(R[t]&V))
