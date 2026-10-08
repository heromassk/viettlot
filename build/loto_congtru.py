"""Loto 5/35 (anh hỏi 08/10/2026): cộng/trừ ±d và nhân/chia ×÷m qua k kỳ → pool 10 số nhiều phiếu. Khung 100/200/500, 5 đoạn 100 kỳ."""
import json, os
B = os.path.dirname(os.path.abspath(__file__)); N = 35; K = 10
D = json.load(open(os.path.join(B, 'all_data.json')))['loto535']; R = [set(sorted(r)[:5]) for r in D['res']]; T = len(R)
def pool(t, f, k):
    v = {}
    for j in range(1, k + 1):
        for x in R[t - j]:
            for y in f(x):
                if 1 <= y <= N: v[y] = v.get(y, 0) + 1
    return sorted((m for m in v if m not in R[t - 1]), key=lambda m: (-v[m], m))[:K]
def run(f, k):
    h = [len(set(pool(t, f, k)) & R[t]) for t in range(T - 500, T)]
    seg = [sum(h[i:i + 100]) / 100 for i in range(0, 500, 100)]
    return [sum(h[-W:]) / W for W in (100, 200, 500)], seg, sum(x >= 3 for x in h[-200:])
rows = []
for d in range(1, 18):
    for k in (1, 2, 3, 5, 7, 10): rows.append((f'±{d}', k, *run(lambda x, d=d: (x - d, x + d), k)))
for m in (2, 3, 4, 5):
    for k in (1, 3, 5): rows.append((f'×÷{m}', k, *run(lambda x, m=m: (x * m, x // m if x % m == 0 else 0), k)))
mk = K * 5 / N
print(f'LOTO {T} kỳ, 500 kỳ gần ({D["dates"][T-500]} → {D["dates"][-1]}), pool {K} số, mức chia đều {mk:.2f}\n')
print('| Phép | k | TB 100 / 200 / 500 | 5 đoạn 100 (cũ→mới) | Đoạn ≥ mức | Pool ≥3 (200 kỳ) |')
for r in sorted(rows, key=lambda r: (-sum(x >= mk for x in r[3]), -min(r[3])))[:12]:
    print(f'| {r[0]} | {r[1]} | ' + ' / '.join(f'{x:.2f}' for x in r[2]) + ' | ' + ' '.join(f'{x:.2f}' for x in r[3]) + f' | {sum(x >= mk for x in r[3])}/5 | {r[4]} |')
print('\nSố phép có cả 5 đoạn ≥ mức:', sum(all(x >= mk for x in r[3]) for r in rows), '/', len(rows))
