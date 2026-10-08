"""Power, 200 kỳ gần (anh, 08/10/2026): phép cộng/trừ nào cho pool 12 và vé ma trận 6 vé trúng nhiều nhất, có đều qua 4 đoạn 50 kỳ không."""
import json, sys
from itertools import combinations
sys.argv = ['x', 'power']; __file__ = '/home/user/viettlot/build/congtru_50.py'
exec(open(__file__).read().split('rows = []')[0])
W = 200
def ev(ds, k):
    h = []; b = []
    for t in range(T - W, T):
        v = {}
        for j in range(1, k + 1):
            for x in R[t - j]:
                for d in ds:
                    for m in (x - d, x + d):
                        if 1 <= m <= N: v[m] = v.get(m, 0) + 1
        p = sorted((m for m in v if m not in R[t - 1]), key=lambda m: (-v[m], m))[:12]
        h.append(len(set(p) & R[t])); b.append(max(len(set(tk) & R[t]) for tk in tickets(p)) if len(p) == 12 else 0)
    q = [sum(h[i:i + 50]) / 50 for i in (0, 50, 100, 150)]
    return dict(ds=ds, k=k, q=q, a=sum(h) / W, p3=sum(x >= 3 for x in h), p4=sum(x >= 4 for x in h), v3=sum(x >= 3 for x in b), v4=sum(x >= 4 for x in b))
rows = [ev((d,), k) for d in range(1, 28) for k in (2, 3, 5, 7, 10)]
best = sorted({r['ds'][0] for r in sorted(rows, key=lambda r: -r['a'])[:8]} | {1, 11, 22})
rows += [ev(p, k) for p in combinations(best, 2) for k in (3, 5)]
json.dump(rows, open('/home/user/viettlot/build/power_ct200.json', 'w'))
print(f'POWER 200 kỳ ({D["dates"][T-W]} → {D["dates"][-1]}), {len(rows)} phép\n')
print('| Phép | k | 4 đoạn 50 (cũ→mới) | TB | Pool ≥3 | Pool ≥4 | Vé ≥3 | Vé ≥4 |')
for key in ('a', 'v3', 'v4'):
    print(f'-- xếp theo {key}')
    for r in sorted(rows, key=lambda r: (-r[key], -min(r['q'])))[:8]:
        print(f"| ±{'/'.join(map(str, r['ds']))} | {r['k']} | " + ' '.join(f'{x:.2f}' for x in r['q']) + f" | {r['a']:.2f} | {r['p3']} | {r['p4']} | {r['v3']} | {r['v4']} |")
for ds, k in (((1, 22), 3), ((11, 22), 3), ((1,), 5)):
    r = next((r for r in rows if r['ds'] == ds and r['k'] == k), None) or ev(ds, k)
    print(f"tham chiếu ±{'/'.join(map(str, ds))} k{k}: " + ' '.join(f'{x:.2f}' for x in r['q']) + f" TB {r['a']:.2f} p3 {r['p3']} p4 {r['p4']} v3 {r['v3']} v4 {r['v4']}")
