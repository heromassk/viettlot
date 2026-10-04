#!/usr/bin/env python3
"""Pool từng vị trí u,v,w,x,y,z (dãy xếp tăng dần). Chạy tiến, chấm theo từng kỳ.
  python3 build/vitri.py power|mega|loto [--W 100] [--q 85]
Mỗi vị trí: học L=200 kỳ trước → khoảng hẹp nhất chứa ≥q% giá trị (A: theo giá trị; B: theo chênh lệch so với kỳ trước
cùng vị trí). Kỳ đúng = giá trị thật nằm trong khoảng. Báo % kỳ đúng (W gần / W trước), số lượng số mỗi vị trí, % kỳ đúng
CẢ dãy, phần vé giữ lại, và khoảng áp cho kỳ tới."""
import json, os, sys, random
GM = {'power': ('power655', 55, 6), 'mega': ('mega645', 45, 6), 'loto': ('loto535', 35, 5)}
key, NB, KB = GM[sys.argv[1]]
arg = lambda k, d: type(d)(sys.argv[sys.argv.index(k) + 1]) if k in sys.argv else d
W, Q, L = arg('--W', 100), arg('--q', 85), 200
D = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'all_data.json')))[key]
S = [sorted(r) for r in D['res']]; T = len(S)
PN = 'uvwxyz'[:KB]
random.seed(3); MC = [sorted(random.sample(range(1, NB + 1), KB)) for _ in range(3000)]

def narrow(vals, q):
    v = sorted(vals); n = len(v); k = max(1, -(-q * n // 100))
    best = min(range(n - k + 1), key=lambda i: (v[i + k - 1] - v[i], i))
    return v[best], v[best + k - 1]

def intervals(t, mode):
    out = []
    for p in range(KB):
        if mode == 'A':
            out.append(narrow([S[u][p] for u in range(t - L, t)], Q))
        else:
            lo, hi = narrow([S[u][p] - S[u - 1][p] for u in range(t - L, t)], Q)
            b = S[t - 1][p]; out.append((max(1, b + lo), min(NB, b + hi)))
    return out

def run(a, b, mode):
    okp = [0] * KB; okall = 0; width = [0] * KB; keep = 0
    for t in range(a, b):
        iv = intervals(t, mode); allin = True
        for p, (lo, hi) in enumerate(iv):
            ok = lo <= S[t][p] <= hi; okp[p] += ok; allin &= ok; width[p] += hi - lo + 1
        okall += allin
        if t % 5 == 0: keep += sum(all(lo <= tk[p] <= hi for p, (lo, hi) in enumerate(iv)) for tk in MC) / len(MC)
    n = b - a
    return [x / n * 100 for x in okp], okall / n * 100, [w / n for w in width], keep / (n / 5) * 100

for mode, lab in (('A', 'A. Khoảng theo giá trị'), ('B', 'B. Khoảng theo chênh lệch so với kỳ trước')):
    r1 = run(T - W, T, mode); r0 = run(T - 2 * W, T - W, mode)
    print(f'## {key} — {lab} (mỗi vị trí chứa ≥{Q}% của {L} kỳ trước)\n')
    print(f'| Vị trí | Đúng {W} kỳ gần | {W} kỳ trước | Số lượng số TB |\n|---|---|---|---|')
    for p in range(KB):
        print(f'| {PN[p]} | **{r1[0][p]:.0f}%** | {r0[0][p]:.0f}% | {r1[2][p]:.1f} |')
    print(f'\nĐúng CẢ {KB} vị trí: **{r1[1]:.0f}%** ({W} kỳ gần) · {r0[1]:.0f}% ({W} kỳ trước) · vé giữ lại {r1[3]:.0f}%\n')
    iv = intervals(T, mode)
    print('Áp kỳ tới: ' + ' · '.join(f'{PN[p]} {lo:02d}–{hi:02d}' for p, (lo, hi) in enumerate(iv)) + '\n')
