"""Quy luật cộng/trừ (anh, 08/10/2026): lấy số kỳ t−lag cộng/trừ d → pool kỳ t. Chấm tỉ lệ ra mỗi số của chính pool,
khung 10/20/50/100 kỳ + 3 đoạn 100 kỳ + cả lịch sử. Dùng: python3 build/congtru.py mega|power"""
import json, sys, os
g = sys.argv[1]; key, N = {'mega': ('mega645', 45), 'power': ('power655', 55)}[g]
D = json.load(open(os.path.join(os.path.dirname(__file__), 'all_data.json')))[key]
R = [set(sorted(r)[:6]) for r in D['res']]; T = len(R); TB = 600 / N
def pool(t, lag, d):
    p = R[t - lag]
    if d == 'g': return {N + 1 - x for x in p} - R[t - 1]          # số gương N+1−x
    return {x + s for x in p for s in ((d, -d) if d > 0 else (0,)) if 1 <= x + s <= N} - (R[t - 1] if d else set())
def rate(ts, lag, d):
    h = c = 0
    for t in ts: P = pool(t, lag, d); h += len(P & R[t]); c += len(P)
    return 100 * h / c if c else 0, c / len(ts)
rows = []
for lag in (1, 2, 3):
    for d in list(range(0, 23)) + ['g']:
        if d == 0 and lag == 1: lab = 'trùng kỳ trước'
        r = {W: rate(range(T - W, T), lag, d)[0] for W in (10, 20, 50, 100)}
        dd = [rate(range(T - 100 * k - 100, T - 100 * k), lag, d)[0] for k in (2, 1, 0)]
        al, sz = rate(range(3, T), lag, d)
        rows.append((lag, d, sz, r, dd, al))
# ổn định: cả 4 khung, 3 đoạn và cả lịch sử cùng phía so với mức TB mỗi số
def side(x): return all(v > TB for v in x) - all(v < TB for v in x)
print(f'{g.upper()} — mức TB mỗi số {TB:.1f}%\n')
print('| Kỳ | ± | Pool | 10 | 20 | 50 | 100 | 3 đoạn | Cả LS | Ổn định |\n|---|---|---|---|---|---|---|---|---|---|')
for lag, d, sz, r, dd, al in sorted(rows, key=lambda x: -abs(x[5] - TB)):
    sd = side(list(r.values())[2:] + dd + [al])
    print(f"| t−{lag} | {'gương' if d == 'g' else ('trùng' if d == 0 else d)} | {sz:.1f} | " + ' | '.join(f'{r[W]:.1f}' for W in (10, 20, 50, 100))
          + f" | {'/'.join(f'{x:.1f}' for x in dd)} | {al:.1f} | {'↑ ra nhiều' if sd > 0 else '↓ ra ít' if sd < 0 else ''} |")
