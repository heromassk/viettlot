"""Phép cộng/trừ nào ổn định trong 100 và 200 kỳ gần (anh, 08/10/2026): pool 12, chấm TB trúng ở 4 đoạn 50 kỳ của 200 kỳ.
Dùng: python3 build/congtru_200.py mega|power"""
import json, sys, os
g = sys.argv[1]; key, N = {'mega': ('mega645', 45), 'power': ('power655', 55)}[g]
D = json.load(open(os.path.join(os.path.dirname(__file__), 'all_data.json')))[key]
R = [set(sorted(r)[:6]) for r in D['res']]; T = len(R)
def pool(t, d, k):
    v = {}
    for j in range(1, k + 1):
        for x in R[t - j]:
            for m in (x - d, x + d):
                if 1 <= m <= N: v[m] = v.get(m, 0) + 1
    return sorted((m for m in v if m not in R[t - 1]), key=lambda m: (-v[m], m))[:12]
rows = []
for d in range(1, 23):
    for k in (1, 2, 3, 5, 7, 10):
        h = [len(set(pool(t, d, k)) & R[t]) for t in range(T - 200, T)]
        q = [sum(h[i:i + 50]) / 50 for i in (0, 50, 100, 150)]
        rows.append(dict(d=d, k=k, q=q, a100=sum(h[100:]) / 100, a200=sum(h) / 200, g3=sum(x >= 3 for x in h[100:]), g3b=sum(x >= 3 for x in h), g4=sum(x >= 4 for x in h)))
print(f'{g.upper()} — pool 12, 200 kỳ gần ({D["dates"][T-200]} → {D["dates"][-1]}). Mỗi kỳ chia đều pool 12: {6*12/N:.2f}\n')
print('| ± | k kỳ | 4 đoạn 50 kỳ (cũ→mới) | TB 100 | TB 200 | Pool ≥3 (100 / 200 kỳ) | Pool ≥4 (200) |\n|---|---|---|---|---|---|---|')
for r in sorted(rows, key=lambda r: -min(r['q']))[:12]:
    print(f"| {r['d']} | {r['k']} | " + ' · '.join(f'{x:.2f}' for x in r['q']) + f" | {r['a100']:.2f} | {r['a200']:.2f} | {r['g3']} / {r['g3b']} | {r['g4']} |")
