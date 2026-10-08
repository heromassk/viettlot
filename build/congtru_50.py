"""50 kỳ gần (anh, 08/10/2026): mọi phép ±1..22 × k kỳ — pool 12 trúng ≥4 bao nhiêu kỳ, vé ma trận 6 vé trúng ≥4 bao nhiêu kỳ.
Dùng: python3 build/congtru_50.py mega|power [số kỳ]"""
import json, sys, os, importlib.util
B = os.path.dirname(os.path.abspath(__file__)); g = sys.argv[1]; W = int(sys.argv[2]) if len(sys.argv) > 2 else 50
sys.argv = [sys.argv[0], g]
spec = importlib.util.spec_from_file_location('cv', os.path.join(B, 'congtru_ve.py'))
key, N = {'mega': ('mega645', 45), 'power': ('power655', 55)}[g]
D = json.load(open(os.path.join(B, 'all_data.json')))[key]; R = [set(sorted(r)[:6]) for r in D['res']]; T = len(R)
import numpy as np
from itertools import combinations
def parts(r):
    if not r: yield []; return
    for b, c in combinations(r[1:], 2):
        for t in parts([x for x in r[1:] if x not in (b, c)]): yield [(r[0], b, c)] + t
PT = np.array(list(parts(list(range(12))))); PAIRS = list(combinations(range(4), 2))
def tickets(pool):
    a = np.array(pool); odd = (a % 2)[PT].sum(2); sm = a[PT].sum(2)
    to = np.stack([odd[:, i] + odd[:, j] for i, j in PAIRS], 1); ts = np.stack([sm[:, i] + sm[:, j] for i, j in PAIRS], 1)
    p = PT[((np.abs(to - 3) > 1).sum(1) * 1000 + ts.max(1) - ts.min(1)).argmin()]
    return [a[list(p[i]) + list(p[j])].tolist() for i, j in PAIRS]
rows = []
for d in range(1, 23):
    for k in (1, 2, 3, 5, 7, 10):
        p3 = p4 = v3 = v4 = 0; ex = []
        for t in range(T - W, T):
            v = {}
            for j in range(1, k + 1):
                for x in R[t - j]:
                    for m in (x - d, x + d):
                        if 1 <= m <= N: v[m] = v.get(m, 0) + 1
            pool = sorted((m for m in v if m not in R[t - 1]), key=lambda m: (-v[m], m))[:12]
            if len(pool) < 12: continue
            h = len(set(pool) & R[t]); b = max(len(set(tk) & R[t]) for tk in tickets(pool))
            p3 += h >= 3; p4 += h >= 4; v3 += b >= 3; v4 += b >= 4
            if b >= 4: ex.append(D['dates'][t][:5])
        rows.append((d, k, p3, p4, v3, v4, ex))
print(f'{g.upper()} {W} kỳ gần ({D["dates"][T-W]} → {D["dates"][-1]}), 132 phép')
print('Phép có vé ≥4:', sum(r[5] > 0 for r in rows), '· tổng lượt vé ≥4:', sum(r[5] for r in rows))
print('| ± | k | pool ≥3 | pool ≥4 | vé ≥3 | vé ≥4 | kỳ vé ≥4 |')
for r in sorted(rows, key=lambda r: (-r[5], -r[3], -r[4]))[:12]:
    print(f'| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} | {r[5]} | {" ".join(r[6])} |')
