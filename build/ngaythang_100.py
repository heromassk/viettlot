#!/usr/bin/env python3
"""100 kỳ gần: mỗi kỳ trùng bao nhiêu số ngày tháng (anh, 07/10/2026). Nhóm "ngày tháng" = dương (thứ, ngày, tháng, thứ+ngày, thứ+tháng, ngày+tháng)
+ âm (ngày, tháng, ngày+tháng). So số kỳ trùng 0/1/2/≥3 với kỳ vọng ngẫu nhiên (siêu bội theo đúng số lượng số của từng kỳ).
  python3 build/ngaythang_100.py"""
import json, os, datetime
from math import comb
HERE = os.path.dirname(os.path.abspath(__file__))
A = json.load(open(os.path.join(HERE, 'all_data.json'))); LUN = json.load(open(os.path.join(HERE, 'max3d_lunar.json')))
def S(ds, NB):
    d = datetime.datetime.strptime(ds[:10], '%d/%m/%Y'); ld, lm, _ = LUN[ds[:10]]; th = d.weekday() + 2
    return {x for x in (th, d.day, d.month, th + d.day, th + d.month, d.day + d.month, ld, lm, ld + lm) if 1 <= x <= NB}
for g, key, NB, KB in (('POWER', 'power655', 55, 6), ('MEGA', 'mega645', 45, 6), ('LOTO', 'loto535', 35, 5)):
    D, R = A[key]['dates'], [set(r) for r in A[key]['res']]; N = len(R)
    cnt = [0] * 4; exp = [0.0] * 4; rows = []; tot = sz = 0
    for t in range(N - 100, N):
        s = S(D[t], NB); k = len(s); h = len(s & R[t]); cnt[min(h, 3)] += 1; tot += h; sz += k
        p = [comb(k, j) * comb(NB - k, KB - j) / comb(NB, KB) for j in range(min(k, KB) + 1)]
        for j, v in enumerate(p): exp[min(j, 3)] += v
        if h >= 2: rows.append(f'{D[t]}: {" ".join(f"{x:02d}" for x in sorted(R[t]))} → trùng {" ".join(f"{x:02d}" for x in sorted(s & R[t]))}')
    print(f'\n## {g} — 100 kỳ ({D[N-100]} → {D[-1]}), mỗi kỳ nhóm ngày tháng TB {sz/100:.1f} số\n')
    print('| Trùng | 0 số | 1 số | 2 số | ≥3 số | Tổng số trùng |\n|---|---|---|---|---|---|')
    print(f'| Thực tế (số kỳ) | {cnt[0]} | {cnt[1]} | {cnt[2]} | {cnt[3]} | {tot} |')
    print(f'| Ngẫu nhiên | {exp[0]:.0f} | {exp[1]:.0f} | {exp[2]:.1f} | {exp[3]:.1f} | {sz*KB/NB:.0f} |')
    print('\nKỳ trùng ≥2 số: ' + ('; '.join(rows) or '—'))
