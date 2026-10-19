# Tổng / hiệu 2 số kỳ trước có ra ở kỳ sau? (anh 20/10/2026) — chỉ đếm số kỳ, khung 20/50/100.
# Kỳ t: T = {a+b ≤ NB}, H = {|a−b|} từ mọi cặp của kỳ t−1 (lọc giờ thì kỳ cùng giờ trước). Đếm số trúng của kỳ t trong T, H, T∪H.
import json,itertools
ALL=json.load(open('build/all_data.json'))
def sets(prev,NB):
    T={a+b for a,b in itertools.combinations(prev,2) if a+b<=NB};H={abs(a-b) for a,b in itertools.combinations(prev,2)}
    return T,H
def run(key,NB,flt=None):
    R=[set(r) for r in ALL[key]['res']];DT=ALL[key]['dates'];idx=[i for i in range(len(R)) if flt is None or DT[i].endswith(flt)]
    out=[]
    for k in range(1,len(idx)):
        T,H=sets(R[idx[k-1]],NB);r=R[idx[k]];out.append((len(T),len(H),len(T|H),len(r&T),len(r&H),len(r&(T|H))))
    return out,R,idx,DT
for key,NB,nm,modes in [('loto535',35,'Loto',[(None,'cả 2 giờ'),('13h','chỉ 13h'),('21h','chỉ 21h')]),('mega645',45,'Mega',[(None,'')]),('power655',55,'Power',[(None,'')])]:
    for flt,lab in modes:
        o,R,idx,DT=run(key,NB,flt)
        print(f'\n## {nm} {lab}')
        for W in (20,50,100):
            s=o[-W:];n=len(s)
            f=lambda j,m:sum(x[j]>=m for x in s)
            print(f'{W} kỳ: nhóm tổng ~{sum(x[0] for x in s)/n:.0f} số, hiệu ~{sum(x[1] for x in s)/n:.0f}, gộp ~{sum(x[2] for x in s)/n:.0f} | TỔNG: kỳ có ≥1 {f(3,1)}, ≥2 {f(3,2)}, ≥3 {f(3,3)} | HIỆU: ≥1 {f(4,1)}, ≥2 {f(4,2)}, ≥3 {f(4,3)} | GỘP: ≥1 {f(5,1)}, ≥2 {f(5,2)}, ≥3 {f(5,3)}, TB {sum(x[5] for x in s)/n:.1f} số/kỳ')
        last=R[idx[-1]];T,H=sets(last,NB)
        print(f'  kỳ tới (từ {DT[idx[-1]]} {sorted(last)}): tổng {sorted(T)} | hiệu {sorted(H)}')
