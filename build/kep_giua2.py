# Lô kẹp Loto (anh 19/10/2026): kỳ t có a và a+2 (không có a+1) → a+1 có ra trong 2 kỳ tới không?
# Ba chế độ: liền nhau (13h+21h), chỉ 13h (2 kỳ 13h tới), chỉ 21h. So với các số khác không có ở kỳ t.
# Chấm % ra ở kỳ +1, kỳ +2, trong 2 kỳ; khung 3 đoạn 100 kỳ (gần → xa) + toàn bộ.
import json
D=json.load(open('build/all_data.json'))['loto535'];R=[set(r) for r in D['res']];DT=D['dates'];T=len(R)
def run(idx):   # idx = danh sách chỉ số kỳ theo thứ tự (đã lọc giờ)
    out=[]
    for k in range(len(idx)-2):
        t=idx[k];a,b=R[idx[k+1]],R[idx[k+2]]
        kep={n+1 for n in R[t] if n+2 in R[t] and n+1 not in R[t]}
        oth=set(range(1,36))-R[t]-kep
        out.append((len(kep),sum(n in a for n in kep),sum(n in a or n in b for n in kep),sum(n in b for n in kep),len(oth),sum(n in a for n in oth),sum(n in a or n in b for n in oth),bool(kep&(a|b))))
    return out
def fmt(o):
    nk=sum(x[0] for x in o);no=sum(x[4] for x in o);ky=sum(1 for x in o if x[0]);hit=sum(x[7] for x in o)
    return f"{ky} kỳ có kẹp ({nk} số) · kỳ +1: {sum(x[1] for x in o)/nk:.1%} vs {sum(x[5] for x in o)/no:.1%} · trong 2 kỳ: {sum(x[2] for x in o)/nk:.1%} vs {sum(x[6] for x in o)/no:.1%} · kỳ có kẹp mà số kẹp về trong 2 kỳ: {hit}/{ky} ({hit/max(1,ky):.0%})"
for nm,flt in [('Cả 2 giờ (liền nhau)',None),('Chỉ 13h','13h'),('Chỉ 21h','21h')]:
    idx=[i for i in range(T) if flt is None or DT[i].endswith(flt)]
    o=run(idx);n=len(o)
    print(f'\n## {nm}  (số kẹp vs số khác)')
    for lab,(a,b) in [('100 kỳ gần',(n-100,n)),('đoạn 2',(n-200,n-100)),('đoạn 3',(n-300,n-200)),('toàn bộ',(0,n))]:
        print(f'- {lab}: '+fmt(o[max(0,a):b]))
    t=idx[-1];kep=sorted(n+1 for n in R[t] if n+2 in R[t] and n+1 not in R[t])
    print(f'  kỳ cuối {DT[t]} {sorted(R[t])} → số kẹp: {kep}')
