#!/usr/bin/env python3
"""Chữ số ra nhiều nhất kỳ trước có ra nhiều ở kỳ sau không (anh, 05/10/2026).
Mỗi kỳ 20 bộ = 60 chữ số (mỗi hàng 20). Lấy chữ số nhiều nhất (hòa thì lấy hết) của kỳ trước:
  - cả 60 chữ số, hoặc từng hàng (trăm/chục/đơn vị) riêng;
rồi đo tỉ lệ chữ số đó trong kỳ sau (chia đều 10%). Đối chứng: chữ số ít nhất kỳ trước.
Nguồn kỳ trước: cùng game, hoặc game kia (Max 3D ↔ Pro chung bộ quay; kỳ gần nhất trước đó, cách ≤3 ngày).
Khung 10/20/50/100 kỳ + 3 đoạn 100 kỳ + cả lịch sử. Lần đúng = chữ số đó ra > mức TB (≥7/60 cả bộ; ≥3/20 mỗi hàng).
  python3 build/max3d_chusonhieu.py"""
import json, os, datetime
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
def load(f):
    D = json.load(open(os.path.join(HERE, f)))
    return [datetime.datetime.strptime(d, '%d/%m/%Y').date() for d in D['dates']], D['res']
G = {'Max 3D+': load('max3d_data.json'), 'Max 3D Pro': load('max3dpro_data.json')}
def cnt(r, h=None):
    c = np.zeros(10, int)
    for s in r:
        for i in (range(3) if h is None else (h,)): c[int(s[i])] += 1
    return c
def pairs(tgt, src):
    dt, R = G[tgt]
    if src == tgt: return [(t, R[t - 1]) for t in range(1, len(R))]
    ds, S = G[src]; out = []; j = 0
    for t in range(len(dt)):
        while j + 1 < len(ds) and ds[j + 1] < dt[t]: j += 1
        if ds[j] < dt[t] and (dt[t] - ds[j]).days <= 3: out.append((t, S[j]))
    return out
def score(tgt, prs, h, kieu):
    R = G[tgt][1]; sh = []; ok = []
    n = 60 if h is None else 20
    for t, prev in prs:
        c = cnt(prev, h); m = c.max() if kieu == 'nhiều' else c.min()
        ds = np.flatnonzero(c == m); nx = cnt(R[t], h)
        sh.append(nx[ds].mean() / n); ok.append(np.mean(nx[ds] > n / 10))
    return np.array(sh), np.array(ok)
# xác suất "đúng" của 1 chữ số bất kỳ (chia đều)
from math import comb
def p_over(n): return sum(comb(n, k) * .1 ** k * .9 ** (n - k) for k in range(n // 10 + 1, n + 1))
KH = (10, 20, 50, 100)
for tgt in G:
    src2 = [s for s in G if s != tgt][0]
    print(f'\n## {tgt} — {len(G[tgt][1])} kỳ\n')
    print('| Kỳ trước lấy từ | Chữ số | Phạm vi | ' + ' | '.join(f'{k} kỳ' for k in KH) + ' | 3 đoạn 100 kỳ | Cả lịch sử | Đúng (cả LS) |')
    print('|' + '---|' * (9 + len(KH) - 4))
    for src in (tgt, src2):
        prs = pairs(tgt, src)
        for kieu in ('nhiều', 'ít'):
            for h, nm in ((None, 'cả 60'), (0, 'hàng trăm'), (1, 'hàng chục'), (2, 'hàng đơn vị')):
                sh, ok = score(tgt, prs, h, kieu)
                f = lambda a: f'{a.mean() * 100:.1f}%'
                d3 = ' · '.join(f(sh[-100 * (i + 1):len(sh) - 100 * i]) for i in range(3))
                po = p_over(60 if h is None else 20)
                print(f'| {"cùng game" if src == tgt else src} | {kieu} nhất | {nm} | ' + ' | '.join(f(sh[-k:]) for k in KH)
                      + f' | {d3} | {f(sh)} | {ok.mean() * 100:.1f}% (TB {po * 100:.1f}%) |')
    print('\nChia đều: 10,0%. Độ nhiễu 1 kỳ: cả 60 ±3,9 điểm, 1 hàng ±6,7 điểm → khung 100 kỳ ±0,4 / ±0,7, cả lịch sử ±0,1–0,2.')
# kỳ gần nhất
for tgt in G:
    r = G[tgt][1][-1]; c = cnt(r)
    print(f'\n{tgt} {G[tgt][0][-1]:%d/%m/%Y}: chữ số nhiều nhất cả 60: ' + ' '.join(str(d) for d in np.flatnonzero(c == c.max())) + f' ({c.max()} lần); mỗi hàng: '
          + ' / '.join(','.join(str(d) for d in np.flatnonzero(cnt(r, h) == cnt(r, h).max())) for h in range(3)))
