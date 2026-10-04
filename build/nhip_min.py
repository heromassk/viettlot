#!/usr/bin/env python3
"""Nhịp tối thiểu của từng số (ý anh): trong quá khứ, mỗi lần ra xong số đó luôn nghỉ ÍT NHẤT x kỳ mới ra lại.
Nếu bây giờ nó mới nghỉ < x kỳ → kỳ này nó ra là phá nhịp → loại.
  python3 build/nhip_min.py power|mega|loto
Biến thể: cửa sổ lịch sử W kỳ, cần ≥m lần ra trong cửa sổ để tin nhịp; chỉ dùng x ≥ 1."""
import json, os, sys
from math import comb
GM = {'power': ('power655', 55, 6), 'mega': ('mega645', 45, 6), 'loto': ('loto535', 35, 5)}
key, NB, KB = GM[sys.argv[1]]
D = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'all_data.json')))[key]
R = [set(r) for r in D['res']]; T = len(R)
def info(t, n, W):
    hits = [u for u in range(max(0, t - W), t) if n in R[u]]
    gaps = [b - a - 1 for a, b in zip(hits, hits[1:])]   # số kỳ nghỉ giữa 2 lần ra
    cur = t - 1 - hits[-1] if hits else None               # đang nghỉ bao nhiêu kỳ
    return len(hits), (min(gaps) if gaps else None), cur
segs = [(T - 100, T), (T - 200, T - 100), (T - 300, T - 200)]
print(f'## {key} — nhịp tối thiểu từng số: "luôn nghỉ ≥x kỳ" mà mới nghỉ <x → loại\n')
print('| Biến thể (lịch sử W kỳ, cần ≥m lần ra) | Đúng 3 đoạn (gần→xa) | Bỏ TB/kỳ | Vé giữ lại | Tỉ lệ ra nhóm bỏ / còn lại (3 đoạn) | Kỳ tới bỏ (số: nghỉ tối thiểu x, đang nghỉ) |\n|---|---|---|---|---|---|')
for W in (100, 200):
    for m in (5, 8):
        oks, rr, bo, kp = [], [], 0, 0
        for i, (a, b) in enumerate(segs):
            ok = h1 = n1 = h0 = n0 = 0
            for t in range(a, b):
                ex = set()
                for n in range(1, NB + 1):
                    k, mg, cur = info(t, n, W)
                    if k >= m and mg is not None and mg >= 1 and cur is not None and cur < mg: ex.add(n)
                x = len(ex & R[t]); ok += not x; h1 += x; n1 += len(ex); h0 += KB - x; n0 += NB - len(ex)
                if i == 0: bo += len(ex); kp += comb(NB - len(ex), KB) / comb(NB, KB)
            oks.append(ok / (b - a) * 100); rr.append(f'{h1 / max(n1, 1) * 100:.1f}/{h0 / n0 * 100:.1f}')
        now = []
        for n in range(1, NB + 1):
            k, mg, cur = info(T, n, W)
            if k >= m and mg is not None and mg >= 1 and cur is not None and cur < mg: now.append(f'{n:02d}(x={mg}, nghỉ {cur})')
        print(f'| W={W}, m≥{m} | **{oks[0]:.0f}%** / {oks[1]:.0f}% / {oks[2]:.0f}% | {bo / 100:.1f} | {kp:.0f}% | {" · ".join(rr)} | {", ".join(now) or "—"} |')
