#!/usr/bin/env python3
"""Nhịp RIÊNG của từng số: dựa vào chính lịch sử của số đó (W kỳ trước), khi nó đang vắng đúng g kỳ thì
trong quá khứ nó có hay ra ở kỳ kế tiếp không? Nếu ≥m lần đã ở đúng tình huống này mà tỉ lệ ra ≤ ngưỡng → loại.
  python3 build/nhip.py power|mega|loto [--W 200]"""
import json, os, sys
from math import comb
GM = {'power': ('power655', 55, 6), 'mega': ('mega645', 45, 6), 'loto': ('loto535', 35, 5)}
key, NB, KB = GM[sys.argv[1]]
WL = int(sys.argv[sys.argv.index('--W') + 1]) if '--W' in sys.argv else 200
D = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'all_data.json')))[key]
R = [set(r) for r in D['res']]; T = len(R)
def hazard(t, n):
    """(số lần đã vắng đúng g kỳ, trong đó ra ngay kỳ kế) theo lịch sử W kỳ trước t, g = số kỳ vắng hiện tại."""
    g = 0
    while g < t and n not in R[t - 1 - g]: g += 1
    seen = hit = 0; run = None
    for u in range(t - WL, t):
        # tại kỳ u: số n đang vắng bao nhiêu kỳ (tính từ lần ra gần nhất trước u)?
        if run is not None and run == g:
            seen += 1; hit += n in R[u]
        if n in R[u]: run = 0
        elif run is not None: run += 1
    return g, seen, hit
VAR = [(m, th) for m in (3, 4, 5) for th in (0.0, 0.1)]
segs = [(T - 100, T), (T - 200, T - 100), (T - 300, T - 200)]
H = {}
for a, b in segs:
    for t in range(a, b):
        H[t] = {n: hazard(t, n) for n in range(1, NB + 1)}
H[T] = {n: hazard(T, n) for n in range(1, NB + 1)}
print(f'## {key} — nhịp riêng từng số (lịch sử {WL} kỳ của chính số đó)\n')
print('| Luật: loại số mà lịch sử của nó ở đúng tình huống này đã gặp ≥m lần và tỉ lệ ra ≤ ngưỡng | Đúng 3 đoạn (gần→xa) | Bỏ TB/kỳ | Vé giữ lại | Tỉ lệ ra nhóm bị bỏ / còn lại (3 đoạn) | Kỳ tới bỏ |\n|---|---|---|---|---|---|')
for m, th in VAR:
    oks, bo, kp, rr = [], 0, 0, []
    for i, (a, b) in enumerate(segs):
        ok = h1 = n1 = h0 = n0 = 0
        for t in range(a, b):
            ex = {n for n, (g, s, h) in H[t].items() if s >= m and h / s <= th}
            ok += not (ex & R[t]); x = len(ex & R[t]); h1 += x; n1 += len(ex); h0 += KB - x; n0 += NB - len(ex)
            if i == 0: bo += len(ex); kp += comb(NB - len(ex), KB) / comb(NB, KB)
        oks.append(ok); rr.append(f'{h1 / max(n1, 1) * 100:.1f}/{h0 / n0 * 100:.1f}')
    ex = sorted(n for n, (g, s, h) in H[T].items() if s >= m and h / s <= th)
    print(f'| m≥{m}, ra ≤{th * 100:.0f}% | **{oks[0]}%** / {oks[1]}% / {oks[2]}% | {bo / 100:.1f} | {kp:.0f}% | {" · ".join(rr)} | {" ".join(f"{n:02d}" for n in ex) or "—"} |')
