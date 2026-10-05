#!/usr/bin/env python3
"""Max 3D / Pro — KHOẢNG NGHỈ (vắng bao nhiêu kỳ) → kỳ kế ra nhiều hay ít. Chấm 3 đoạn 100 kỳ gần → xa.
A. Chữ số theo hàng (20 bộ chung lồng): đang vắng g kỳ ở hàng đó → tỉ lệ chiếm trong 20 lần quay kỳ kế (chia đều 10%).
B. 6 vị trí của 2 bộ ĐB: chữ số đang vắng g kỳ ở vị trí đó → % ra ở vị trí đó kỳ kế (chia đều 10%).
C. Bộ số 000–999: đang vắng g kỳ → % ra (≥1 lần trong 20 bộ) kỳ kế (chia đều 1,98%).
  python3 build/max3d_nghi.py [--file build/max3dpro_data.json]"""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
f = sys.argv[sys.argv.index('--file') + 1] if '--file' in sys.argv else os.path.join(HERE, 'max3d_data.json')
D = json.load(open(f)); L = D['res']; T = len(L)
X = np.array([[[int(c) for c in s] for s in r] for r in L])        # (T,20,3)
segs = [(T - 100, T), (T - 200, T - 100), (T - 300, T - 200)]
def table(title, groups, base, rows):
    print(f'\n### {title} (chia đều {base})\n\n| Đang vắng | Cỡ TB/kỳ | Đoạn 1 (gần) | Đoạn 2 | Đoạn 3 | Nhận xét |\n|---|---|---|---|---|---|')
    for g in groups:
        v = [rows[g][s][0] / max(rows[g][s][1], 1) * 100 for s in range(3)]; b = float(base.rstrip('%').replace(',', '.'))
        nx = '▲ nhiều hơn 3/3' if all(x > b * 1.03 for x in v) else '▼ ít hơn 3/3' if all(x < b * 0.97 for x in v) else '—'
        print(f'| {g} | {sum(rows[g][s][1] for s in range(3)) / 300:.1f} | ' + ' | '.join(f'{x:.2f}%' for x in v) + f' | {nx} |')
gl = lambda g, cuts: next(n for n, lo, hi in cuts if lo <= g <= hi)
# A
CA = [('0 (vừa ra kỳ trước)', 0, 0), ('1 kỳ', 1, 1), ('2 kỳ', 2, 2), ('≥3 kỳ', 3, 9999)]
rows = {n: [[0, 0] for _ in range(3)] for n, _, _ in CA}
for si, (a, b) in enumerate(segs):
    for t in range(a, b):
        for h in range(3):
            for d in range(10):
                g = next((k for k in range(t) if d in X[t - 1 - k, :, h]), t)
                r = rows[gl(g, CA)][si]; r[0] += int((X[t, :, h] == d).sum()); r[1] += 20
table('A. Chữ số theo hàng (20 bộ) — tỉ lệ chiếm trong 20 lần quay kỳ kế', [n for n, _, _ in CA], '10%', rows)
print('\n(Cỡ TB/kỳ ở bảng A tính theo lần quay: 20 lần × số chữ số trong nhóm × 3 hàng.)')
# B
CB = [('0–4 kỳ', 0, 4), ('5–9 kỳ', 5, 9), ('10–19 kỳ', 10, 19), ('20–29 kỳ', 20, 29), ('≥30 kỳ', 30, 9999)]
rows = {n: [[0, 0] for _ in range(3)] for n, _, _ in CB}
for si, (a, b) in enumerate(segs):
    for t in range(a, b):
        for bo in (0, 1):
            for h in range(3):
                col = X[:t, bo, h]
                for d in range(10):
                    idx = np.nonzero(col == d)[0]; g = t - 1 - idx[-1] if len(idx) else t
                    r = rows[gl(g, CB)][si]; r[0] += int(X[t, bo, h] == d); r[1] += 1
table('B. 6 vị trí của 2 bộ ĐB — % ra ở vị trí đó kỳ kế', [n for n, _, _ in CB], '10%', rows)
# C
CC = [('0 (vừa ra)', 0, 0), ('1–9 kỳ', 1, 9), ('10–49 kỳ', 10, 49), ('50–99 kỳ', 50, 99), ('100–199 kỳ', 100, 199), ('≥200 kỳ', 200, 99999)]
last = {}; G = {}
rows = {n: [[0, 0] for _ in range(3)] for n, _, _ in CC}
for t in range(T):
    if t >= T - 300:
        si = next(i for i, (a, b) in enumerate(segs) if a <= t < b); now = set(L[t])
        for i in range(1000):
            s = f'{i:03d}'; g = t - 1 - last[s] if s in last else t
            r = rows[gl(g, CC)][si]; r[0] += s in now; r[1] += 1
    for s in L[t]: last[s] = t
table('C. Bộ số — % ra kỳ kế', [n for n, _, _ in CC], '1,98%', rows)
gnow = {f'{i:03d}': (T - 1 - last[f"{i:03d}"] if f'{i:03d}' in last else T) for i in range(1000)}
lng = sorted(gnow, key=lambda s: -gnow[s])[:10]
print(f'\nBộ vắng lâu nhất hiện tại: ' + ', '.join(f'{s} ({gnow[s]} kỳ)' for s in lng))
