#!/usr/bin/env python3
"""Chữ số theo số lần ra kỳ trước → tỉ lệ ra kỳ sau (anh, 05/10/2026: "chữ số", "kiểm toàn bộ", không theo hàng).
Mỗi kỳ 20 bộ = 60 chữ số. Xếp 10 chữ số kỳ trước theo số lần ra (hạng 1 = nhiều nhất; hòa thì chia đều),
đo tỉ lệ của chữ số ở mỗi hạng trong 60 chữ số kỳ sau (chia đều 10%). Thêm: nhóm top 2/3/5, đáy 2/3/5,
và theo số lần ra kỳ trước (0–3, 4, 5, 6, 7, 8, ≥9).
Nguồn kỳ trước: cùng game, hoặc game kia (Max 3D+ ↔ Pro chung bộ quay; kỳ gần nhất trước đó, cách ≤3 ngày).
Khung 10/20/50/100 kỳ + 3 đoạn 100 kỳ + cả lịch sử.
  python3 build/max3d_chusonhieu.py"""
import json, os, datetime
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
def load(f):
    D = json.load(open(os.path.join(HERE, f)))
    return [datetime.datetime.strptime(d, '%d/%m/%Y').date() for d in D['dates']], D['res']
G = {'Max 3D+': load('max3d_data.json'), 'Max 3D Pro': load('max3dpro_data.json')}
def cnt(r):
    c = np.zeros(10, int)
    for s in r:
        for ch in s: c[int(ch)] += 1
    return c
def pairs(tgt, src):
    dt, R = G[tgt]
    if src == tgt: return [(t, R[t - 1]) for t in range(1, len(R))]
    ds, S = G[src]; out = []; j = 0
    for t in range(len(dt)):
        while j + 1 < len(ds) and ds[j + 1] < dt[t]: j += 1
        if ds[j] < dt[t] and (dt[t] - ds[j]).days <= 3: out.append((t, S[j]))
    return out
def rank_share(prev, nxt):
    """share[k] = tỉ lệ (trên 60) của chữ số hạng k+1 kỳ trước, hòa thì chia đều trong nhóm."""
    c, n = cnt(prev), cnt(nxt) / 60
    order = sorted(range(10), key=lambda d: -c[d]); out = np.zeros(10); i = 0
    while i < 10:
        j = i
        while j < 10 and c[order[j]] == c[order[i]]: j += 1
        out[i:j] = np.mean([n[d] for d in order[i:j]]); i = j
    return out
LV = [('0–3 lần', range(0, 4)), ('4 lần', [4]), ('5 lần', [5]), ('6 lần (TB)', [6]), ('7 lần', [7]), ('8 lần', [8]), ('≥9 lần', range(9, 61))]
KH = (10, 20, 50, 100)
f = lambda a: f'{np.nanmean(a) * 100:.1f}%' if len(a) else '–'
def row(nm, a, ex=''):  # a: mảng theo kỳ (nan = kỳ không có)
    seg = ' · '.join(f(a[max(0, len(a) - 100 * (i + 1)):len(a) - 100 * i]) for i in range(3))
    return f'| {nm} | ' + ' | '.join(f(a[-k:]) for k in KH) + f' | {seg} | {f(a)}{ex} |'
HD = '| Nhóm | ' + ' | '.join(f'{k} kỳ' for k in KH) + ' | 3 đoạn 100 kỳ (gần → xa) | Cả lịch sử |\n|' + '---|' * 7
for tgt in G:
    for src in (tgt, [s for s in G if s != tgt][0]):
        prs = pairs(tgt, src); R = G[tgt][1]
        RS = np.array([rank_share(p, R[t]) for t, p in prs])
        print(f'\n## {tgt} ← kỳ trước {"cùng game" if src == tgt else "của " + src} ({len(prs)} cặp kỳ)\n')
        print(HD)
        for k in range(10): print(row(f'Hạng {k + 1}', RS[:, k]))
        for k in (2, 3, 5): print(row(f'Top {k}', RS[:, :k].mean(1)))
        for k in (2, 3, 5): print(row(f'Đáy {k}', RS[:, -k:].mean(1)))
        print('\n' + HD.replace('Nhóm', 'Số lần ra kỳ trước'))
        for nm, vs in LV:
            a = []
            for t, p in prs:
                c, n = cnt(p), cnt(R[t]) / 60
                m = [n[d] for d in range(10) if c[d] in vs]
                a.append(np.mean(m) if m else np.nan)
            a = np.array(a); print(row(nm, a[~np.isnan(a)], f' ({(~np.isnan(a)).sum()} kỳ)'))
print('\nChia đều 10,0%. Nhiễu 1 chữ số: ±3,9 điểm/kỳ → 10 kỳ ±1,2 · 20 kỳ ±0,9 · 50 kỳ ±0,55 · 100 kỳ ±0,4 · cả lịch sử ±0,1–0,14.')
for tgt in G:
    c = cnt(G[tgt][1][-1]); o = sorted(range(10), key=lambda d: -c[d])
    print(f'\n{tgt} {G[tgt][0][-1]:%d/%m/%Y}: ' + ' · '.join(f'{d}:{c[d]}' for d in o))
