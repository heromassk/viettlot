"""Chấm lùi VÉ ma trận 12→6 vé của phép cộng/trừ (anh, 08/10/2026): pool 12 = số nhiều phiếu nhất từ ±d qua k kỳ,
chia 4 nhóm×3 (vé chẵn/lẻ 2-4/4-2/3-3, tổng vé đều nhau), mỗi vé = 2 nhóm. Đếm kỳ có vé trúng ≥3/≥4/≥5 trên toàn lịch sử, theo đoạn 100 kỳ.
Dùng: python3 build/congtru_ve.py mega|power"""
import json, sys, os
import numpy as np
from itertools import combinations
g = sys.argv[1]; key, N = {'mega': ('mega645', 45), 'power': ('power655', 55)}[g]
D = json.load(open(os.path.join(os.path.dirname(__file__), 'all_data.json')))[key]
R = [set(sorted(r)[:6]) for r in D['res']]; T = len(R)
def parts(r):
    if not r: yield []; return
    for b, c in combinations(r[1:], 2):
        for t in parts([x for x in r[1:] if x not in (b, c)]): yield [(r[0], b, c)] + t
PT = np.array(list(parts(list(range(12)))))            # (15400, 4, 3)
PAIRS = list(combinations(range(4), 2))
def tickets(pool):
    a = np.array(pool); odd = (a % 2)[PT].sum(2); sm = a[PT].sum(2)   # (P,4)
    to = np.stack([odd[:, i] + odd[:, j] for i, j in PAIRS], 1); ts = np.stack([sm[:, i] + sm[:, j] for i, j in PAIRS], 1)
    cost = (np.abs(to - 3) > 1).sum(1) * 1000 + ts.max(1) - ts.min(1)
    p = PT[cost.argmin()]
    return [sorted(a[list(p[i]) + list(p[j])].tolist()) for i, j in PAIRS]
CASES = {'mega': [(14, 5), (14, 10), (21, 10), (16, 3), (13, 7), (6, 10), (1, 3), (10, 1)],
         'power': [(11, 7), (3, 10), (3, 7), (2, 7), (5, 3), (1, 5), (8, 3), (1, 1)]}[g]
start = 15; n = T - start
print(f'{g.upper()} — chấm {n} kỳ ({D["dates"][start]} → {D["dates"][-1]}), 6 vé/kỳ. Đoạn = 100 kỳ, đoạn cuối là gần nhất.\n')
out = {}
for d, k in CASES:
    best = []; ex = []
    for t in range(start, T):
        v = {}
        for j in range(1, k + 1):
            for x in R[t - j]:
                for m in (x - d, x + d):
                    if 1 <= m <= N: v[m] = v.get(m, 0) + 1
        pool = sorted((m for m in v if m not in R[t - 1]), key=lambda m: (-v[m], m))[:12]
        if len(pool) < 12: pool += [m for m in range(1, N + 1) if m not in pool and m not in R[t - 1]][:12 - len(pool)]
        b = max(len(set(tk) & R[t]) for tk in tickets(pool)); best.append(b)
        if b >= 4: ex.append((D['dates'][t], b))
    seg = [best[max(0, n - 100 * (i + 1)):n - 100 * i] for i in range(9, -1, -1)]
    c4 = [sum(x >= 4 for x in s) for s in seg]; c3 = [sum(x >= 3 for x in s) for s in seg]
    out[f'{d},{k}'] = dict(c4=c4, ex=ex)
    print(f'±{d} qua {k} kỳ: vé ≥3: {sum(x >= 3 for x in best)} kỳ ({100*sum(x>=3 for x in best)/n:.1f}%) · vé ≥4: {sum(x >= 4 for x in best)} kỳ ({100*sum(x>=4 for x in best)/n:.2f}%) · vé ≥5: {sum(x >= 5 for x in best)}')
    print(f'   ≥4 theo đoạn 100 kỳ (cũ→mới): {c4}  ·  ≥3: {c3}')
    print(f'   các kỳ ≥4: ' + ', '.join(f'{a}({b})' for a, b in ex))
json.dump(out, open(os.path.join(os.path.dirname(__file__), f'congtru_ve_{g}.json'), 'w'), ensure_ascii=False)
