#!/usr/bin/env python3
"""Suy luận Max 3D / 3D+ (cùng kết quả, thứ 2-4-6) hoặc Max 3D Pro: nhóm BỘ SỐ nào ra nhiều/ít hơn ở kỳ kế.
Chấm từng kỳ, 3 đoạn 100 kỳ gần → xa. Mỗi bộ số có xác suất ra (≥1 lần trong 20 bộ) ≈ 1,98%/kỳ.
  python3 build/max3d_suyluan.py [--file build/max3dpro_data.json]"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
f = sys.argv[sys.argv.index('--file') + 1] if '--file' in sys.argv else os.path.join(HERE, 'max3d_data.json')
D = json.load(open(f)); R = [set(r) for r in D['res']]; L = D['res']; T = len(R)
ALL = [f'{i:03d}' for i in range(1000)]
BASE = 1 - 0.999 ** 20
def poscnt(t, W):
    c = [[0] * 10 for _ in range(3)]
    for u in range(max(0, t - W), t):
        for s in L[u]:
            for i, ch in enumerate(s): c[i][int(ch)] += 1
    return c
def wt(t, W):
    c = poscnt(t, W); return {s: c[0][int(s[0])] * c[1][int(s[1])] * c[2][int(s[2])] for s in ALL}
def last_seen(t, s):
    for u in range(t - 1, max(-1, t - 200), -1):
        if s in R[u]: return t - 1 - u
    return 999
G = {
    'Bộ vừa ra kỳ trước': lambda t, X: R[t - 1],
    'Bộ ra trong 10 kỳ gần': lambda t, X: set().union(*R[t - 10:t]),
    'Bộ ra ≥2 lần trong 50 kỳ': lambda t, X: {s for s in ALL if sum(s in R[u] for u in range(t - 50, t)) >= 2},
    'Bộ vắng ≥100 kỳ': lambda t, X: {s for s in ALL if all(s not in R[u] for u in range(t - 100, t))},
    'Giải ĐB kỳ trước': lambda t, X: set(L[t - 1][:2]),
    'Lộn (đảo chữ số) của bộ kỳ trước': lambda t, X: {''.join(p) for s in R[t - 1] for p in __import__('itertools').permutations(s)} - R[t - 1],
    'Bộ ±1 của bộ kỳ trước': lambda t, X: {f'{(int(s) + d) % 1000:03d}' for s in R[t - 1] for d in (-1, 1)},
    'Tam hoa (aaa)': lambda t, X: {f'{d}{d}{d}' for d in range(10)},
    'Có 2 chữ số giống nhau (aab, aba, baa)': lambda t, X: {s for s in ALL if len(set(s)) == 2},
    '100 bộ NẶNG nhất (chữ số theo hàng, 100 kỳ)': lambda t, X: set(sorted(ALL, key=lambda s: -X[100][s])[:100]),
    '100 bộ NHẸ nhất (chữ số theo hàng, 100 kỳ)': lambda t, X: set(sorted(ALL, key=lambda s: X[100][s])[:100]),
    '343 bộ tránh 3 chữ số nhẹ mỗi hàng (100 kỳ)': lambda t, X: (lambda c: {s for s in ALL if all(int(s[i]) not in sorted(range(10), key=lambda d: c[i][d])[:3] for i in range(3))})(poscnt(t, 100)),
    '100 bộ NẶNG nhất (20 kỳ)': lambda t, X: set(sorted(ALL, key=lambda s: -X[20][s])[:100]),
    '100 bộ NẶNG nhất (50 kỳ)': lambda t, X: set(sorted(ALL, key=lambda s: -X[50][s])[:100]),
}
segs = [(T - 100, T), (T - 200, T - 100), (T - 300, T - 200)]
print(f'## {os.path.basename(f)} — {T} kỳ ({D["dates"][0]} → {D["dates"][-1]}). Mỗi bộ ra ≥1 lần/kỳ: chia đều {BASE * 100:.2f}%\n')
print('| Nhóm bộ số | Cỡ TB | Đoạn 1 (gần) | Đoạn 2 | Đoạn 3 | Kết luận | Kỳ tới |\n|---|---|---|---|---|---|---|')
res = {k: [[0, 0] for _ in segs] for k in G}
for si, (a, b) in enumerate(segs):
    for t in range(a, b):
        X = {W: wt(t, W) for W in (20, 50, 100)}
        for k, fn in G.items():
            g = fn(t, X); res[k][si][0] += len(g & R[t]); res[k][si][1] += len(g)
X = {W: wt(T, W) for W in (20, 50, 100)}
for k, fn in G.items():
    v = [h / max(n, 1) * 100 for h, n in res[k]]; sz = sum(n for _, n in res[k]) / 300
    r = [x / (BASE * 100) for x in v]
    c = '▲ nhiều hơn 3/3' if all(x > 1.05 for x in r) else '▼ ít hơn 3/3' if all(x < 0.95 for x in r) else '—'
    nx = sorted(fn(T, X)); nxs = ' '.join(nx) if len(nx) <= 8 else f'{len(nx)} bộ'
    print(f'| {k} | {sz:.0f} | ' + ' | '.join(f'{x:.2f}% (×{y:.2f})' for x, y in zip(v, r)) + f' | {c} | {nxs} |')
