#!/usr/bin/env python3
"""Max 3D / Pro — bộ ra nhiều BẤT THƯỜNG trong 20 kỳ (≥3 hoặc ≥4 lần) → các bộ QUANH nó có ra nhiều hơn ở kỳ sau không (anh, 05/10/2026).
Quanh: (A) đổi ±1 một chữ số (vd 584 → 484, 684, 574, 594, 583, 585: 6 bộ); (B) trùng 2 hàng, khác hàng còn lại (27 bộ); (C) ±1, ±2 về giá trị (583, 585, 582, 586).
Chấm: mỗi bộ quanh ra ≥1 lần ở kỳ kế (chia đều 1,98%) và trong 5 kỳ kế (chia đều 9,5%). Cả lịch sử.
  python3 build/max3d_quanh.py"""
import json, os
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
P1 = 1 - 0.999 ** 20; P5 = 1 - (1 - P1) ** 5
def A(s): return {s[:i] + str((int(s[i]) + d) % 10) + s[i + 1:] for i in range(3) for d in (-1, 1)}
def Bq(s): return {s[:i] + str(d) + s[i + 1:] for i in range(3) for d in range(10)} - {s}
def C(s): return {f'{(int(s) + d) % 1000:03d}' for d in (-2, -1, 1, 2)}
for f, nm in (('max3d_data.json', 'Max 3D+'), ('max3dpro_data.json', 'Max 3D Pro')):
    R = [set(r) for r in json.load(open(os.path.join(HERE, f)))['res']]; T = len(R)
    print(f'\n## {nm} — {T} kỳ\n\n| Bộ "nóng" (trong 20 kỳ) | Nhóm quanh | Số lần xét | Kỳ kế (×) | 5 kỳ kế (×) |\n|---|---|---|---|---|')
    for th in (3, 4):
        for nmq, fq in (('A. đổi ±1 một chữ số (6 bộ)', A), ('B. trùng 2 hàng (27 bộ)', Bq), ('C. ±1, ±2 giá trị (4 bộ)', C), ('Chính bộ đó', lambda s: {s})):
            n = h1 = h5 = 0; done = set()
            for t in range(20, T - 5):
                c = Counter(s for r in R[t - 20:t] for s in r)
                for s, k in c.items():
                    if k >= th and s in R[t - 1]:          # vừa đạt ngưỡng ở kỳ trước → xét 1 lần
                        q = fq(s)
                        for x in q:
                            n += 1; h1 += x in R[t]; h5 += any(x in R[u] for u in range(t, t + 5))
            if n: print(f'| ≥{th} lần | {nmq} | {n} | {h1 / n * 100:.2f}% (×{h1 / n / P1:.2f}) | {h5 / n * 100:.1f}% (×{h5 / n / P5:.2f}) |')
