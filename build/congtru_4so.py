"""Mọi phép cộng/trừ ±1..22 × k kỳ trước (pool 12): đếm kỳ pool trúng ≥4 số trong 500 kỳ gần (anh, 08/10/2026).
Dùng: python3 build/congtru_4so.py mega|power"""
import json, sys, os
g = sys.argv[1]; key, N = {'mega': ('mega645', 45), 'power': ('power655', 55)}[g]
D = json.load(open(os.path.join(os.path.dirname(__file__), 'all_data.json')))[key]
R = [set(sorted(r)[:6]) for r in D['res']]; T = len(R)
rows = []
for d in range(1, 23):
    for k in (1, 2, 3, 5, 7, 10):
        ev = []
        for t in range(T - 500, T):
            v = {}
            for j in range(1, k + 1):
                for x in R[t - j]:
                    for n in (x - d, x + d):
                        if 1 <= n <= N: v[n] = v.get(n, 0) + 1
            p = sorted((n for n in v if n not in R[t - 1]), key=lambda n: (-v[n], n))[:12]
            h = len(set(p) & R[t])
            if h >= 4: ev.append((D['dates'][t], h))
        rows.append((d, k, ev))
tot4 = sum(len(e) for _, _, e in rows)
print(f'{g.upper()} 500 kỳ ({D["dates"][T-500]} → {D["dates"][-1]}), {len(rows)} phép — tổng {tot4} lần pool trúng ≥4, TB {tot4/len(rows):.1f}/phép')
print('Phân bố số lần ≥4/phép:', {c: sum(len(e) == c for *_, e in rows) for c in sorted({len(e) for *_, e in rows})})
for d, k, ev in sorted(rows, key=lambda r: (-len(r[2]), -sum(h for _, h in r[2])))[:12]:
    n5 = sum(h >= 5 for _, h in ev)
    print(f'±{d:<2} k={k:<2}: {len(ev)} kỳ ≥4 ({n5} kỳ ≥5) | gần nhất: ' + ', '.join(f'{dt}({h})' for dt, h in ev[-4:]))
json.dump([dict(d=d, k=k, ev=ev) for d, k, ev in rows], open(os.path.join(os.path.dirname(__file__), f'congtru_4so_{g}.json'), 'w'), ensure_ascii=False)
