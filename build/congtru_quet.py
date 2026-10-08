"""Quét mọi khoảng cộng/trừ d=1..22 × số kỳ trước k (anh, 08/10/2026). Pool 12 số nhiều phiếu nhất (bỏ số kỳ trước).
In: TB trúng 10/20/50/100, 3 đoạn 100 kỳ, 500 kỳ, % kỳ trúng ≥2 và ≥3 số (500 kỳ). Dùng: python3 build/congtru_quet.py mega|power"""
import json, sys, os
g = sys.argv[1]; key, N = {'mega': ('mega645', 45), 'power': ('power655', 55)}[g]
D = json.load(open(os.path.join(os.path.dirname(__file__), 'all_data.json')))[key]
R = [set(sorted(r)[:6]) for r in D['res']]; T = len(R); K = 12
def hits(k, d):
    out = []
    for t in range(T - 500, T):
        v = {}
        for j in range(1, k + 1):
            for x in R[t - j]:
                for n in (x - d, x + d):
                    if 1 <= n <= N: v[n] = v.get(n, 0) + 1
        p = sorted((n for n in v if n not in R[t - 1]), key=lambda n: (-v[n], n))[:K]
        out.append(len(set(p) & R[t]))
    return out
rows = []
for d in range(1, 23):
    for k in (1, 2, 3, 5, 7, 10):
        h = hits(k, d); m = lambda a: sum(a) / len(a)
        rows.append(dict(d=d, k=k, w=[m(h[-W:]) for W in (10, 20, 50, 100)], dd=[m(h[i:i + 100]) for i in (200, 300, 400)],
                         a=m(h), g2=100 * sum(x >= 2 for x in h) / 500, g3=100 * sum(x >= 3 for x in h) / 500))
json.dump(rows, open(os.path.join(os.path.dirname(__file__), f'congtru_quet_{g}.json'), 'w'))
rows.sort(key=lambda r: -(min(r['dd']) + r['a']))
print(f'{g.upper()} {T} kỳ — top 15 theo độ ổn định (đoạn thấp nhất + TB 500 kỳ)\n')
print('| ± | k kỳ | 10 | 20 | 50 | 100 | 3 đoạn | 500 kỳ | ≥2 số | ≥3 số |\n|---|---|---|---|---|---|---|---|---|---|')
for r in rows[:15]:
    print(f"| {r['d']} | {r['k']} | " + ' | '.join(f'{x:.2f}' for x in r['w']) + ' | ' + '/'.join(f'{x:.2f}' for x in r['dd']) + f" | {r['a']:.2f} | {r['g2']:.0f}% | {r['g3']:.0f}% |")
