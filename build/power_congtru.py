"""Power: phép cộng/trừ nào ổn định nhất qua toàn lịch sử (anh, 08/10/2026). Pool 12 nhiều phiếu nhất từ ±d (một hoặc hai khoảng) qua k kỳ.
Chấm TB trúng/kỳ ở 9 đoạn 100 kỳ (cũ→mới) + % kỳ pool ≥3. Ổn định = đoạn thấp nhất cao + số đoạn ≥ mức chia đều (1.31)."""
import json, os
from itertools import combinations
B = os.path.dirname(os.path.abspath(__file__)); N = 55
D = json.load(open(os.path.join(B, 'all_data.json')))['power655']; R = [set(sorted(r)[:6]) for r in D['res']]; T = len(R)
S = T - 900
def run(ds, k):
    h = []
    for t in range(S, T):
        v = {}
        for j in range(1, k + 1):
            for x in R[t - j]:
                for d in ds:
                    for m in (x - d, x + d):
                        if 1 <= m <= N: v[m] = v.get(m, 0) + 1
        p = sorted((m for m in v if m not in R[t - 1]), key=lambda m: (-v[m], m))[:12]
        h.append(len(set(p) & R[t]))
    seg = [sum(h[i:i + 100]) / 100 for i in range(0, 900, 100)]
    return dict(ds=ds, k=k, seg=seg, mn=min(seg), up=sum(s >= 6 * 12 / N for s in seg), a=sum(h) / 900, g3=100 * sum(x >= 3 for x in h) / 900,
                g4=sum(x >= 4 for x in h), last=[sum(h[-W:]) / W for W in (50, 100, 200)])
rows = [run((d,), k) for d in range(1, 28) for k in (1, 2, 3, 4, 5, 7, 10, 15)]
top = sorted(rows, key=lambda r: (-r['up'], -r['mn']))[:10]
singles = sorted({r['ds'][0] for r in top})
rows += [run(p, k) for p in combinations(singles, 2) for k in (2, 3, 5, 7)]
json.dump(rows, open(os.path.join(B, 'power_congtru.json'), 'w'))
print(f'POWER — {len(rows)} phép, 900 kỳ ({D["dates"][S]} → {D["dates"][-1]}), 9 đoạn 100 kỳ. Mức chia đều pool 12: {72/N:.2f}\n')
print('| Phép | k kỳ | 9 đoạn 100 kỳ (cũ→mới) | Đoạn thấp nhất | Số đoạn ≥1.31 | TB 900 | Pool ≥3 | Pool ≥4 | 50/100/200 kỳ gần |\n|---|---|---|---|---|---|---|---|---|')
for r in sorted(rows, key=lambda r: (-r['up'], -r['mn']))[:15]:
    print(f"| ±{'/'.join(map(str, r['ds']))} | {r['k']} | " + ' '.join(f'{x:.2f}' for x in r['seg']) + f" | {r['mn']:.2f} | {r['up']}/9 | {r['a']:.2f} | {r['g3']:.0f}% | {r['g4']} | " + '/'.join(f'{x:.2f}' for x in r['last']) + ' |')
# k nào ổn định nhất (gộp mọi d)
print('\nTheo k (TB các phép đơn): ' + ', '.join(f"k={k}: {sum(r['a'] for r in rows if len(r['ds'])==1 and r['k']==k)/27:.3f}" for k in (1, 2, 3, 4, 5, 7, 10, 15)))
