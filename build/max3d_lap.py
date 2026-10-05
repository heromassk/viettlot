#!/usr/bin/env python3
"""Max 3D / Pro — bộ đã ra trong 5 / 10 kỳ gần có lặp lại kỳ kế không. Chấm 3 đoạn 100 kỳ gần → xa.
Mỗi bộ: % ra (≥1 lần trong 20 bộ) kỳ kế, chia đều 1,98%. Thêm: % kỳ có ≥1 bộ lặp lại từ nhóm, so với kỳ vọng.
  python3 build/max3d_lap.py"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
P = 1 - 0.999 ** 20
for f, nm in (('max3d_data.json', 'Max 3D (3D+)'), ('max3dpro_data.json', 'Max 3D Pro')):
    L = [set(r) for r in json.load(open(os.path.join(HERE, f)))['res']]; T = len(L)
    GR = {
        'Ra ở kỳ trước': lambda t: L[t - 1],
        'Ra trong 2–5 kỳ trước (không tính kỳ trước)': lambda t: set().union(*L[t - 5:t - 1]) - L[t - 1],
        'Ra trong 6–10 kỳ trước': lambda t: set().union(*L[t - 10:t - 5]) - set().union(*L[t - 5:t]),
        'Ra trong 5 kỳ gần (gộp)': lambda t: set().union(*L[t - 5:t]),
        'Ra trong 10 kỳ gần (gộp)': lambda t: set().union(*L[t - 10:t]),
        'Ra ≥2 lần trong 10 kỳ': lambda t: {s for s in set().union(*L[t - 10:t]) if sum(s in L[u] for u in range(t - 10, t)) >= 2},
    }
    print(f'\n## {nm} — {T} kỳ\n\n| Nhóm | Cỡ TB | Mỗi bộ ra kỳ kế (gần · giữa · xa) | Chia đều | Kỳ có ≥1 bộ lặp lại (thực · kỳ vọng) |\n|---|---|---|---|---|')
    for k, fn in GR.items():
        v = []; sz = 0; kr = ke = 0
        for a, b in ((T - 100, T), (T - 200, T - 100), (T - 300, T - 200)):
            h = n = 0
            for t in range(a, b):
                g = fn(t); m = len(g & L[t]); h += m; n += len(g); sz += len(g); kr += m > 0; ke += 1 - (1 - P) ** len(g)
            v.append(h / max(n, 1) * 100)
        r = [x / (P * 100) for x in v]
        print(f'| {k} | {sz / 300:.0f} | ' + ' · '.join(f'{x:.2f}% (×{y:.2f})' for x, y in zip(v, r)) + f' | {P * 100:.2f}% | {kr / 3:.0f}% · {ke / 3:.0f}% |')
