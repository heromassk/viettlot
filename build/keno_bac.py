#!/usr/bin/env python3
"""Keno: chấm các cách chọn bậc 7–10 số trên dữ liệu thật (anh, 05/10/2026).
Bảng giải (vé 10.000đ) theo các trang hướng dẫn Vietlott; mọi bậc trả ~55% (tính theo xác suất) → bảng tự khớp.
Mỗi cách chọn cố định qua các kỳ; đo: tiền về / tiền bỏ, % kỳ có giải, phân bố số trúng. Khung 100/1000/10000 kỳ + cả lịch sử.
  python3 build/keno_bac.py"""
import json, numpy as np
from math import comb
GIAI = {10: {10: 2e9, 9: 150e6, 8: 7.4e6, 7: 600e3, 6: 80e3, 5: 20e3, 0: 10e3},
        9: {9: 800e6, 8: 12e6, 7: 1.5e6, 6: 150e3, 5: 30e3, 4: 10e3, 0: 10e3},
        8: {8: 200e6, 7: 5e6, 6: 500e3, 5: 50e3, 4: 10e3, 0: 10e3},
        7: {7: 40e6, 6: 1.2e6, 5: 100e3, 4: 20e3, 3: 10e3},
        6: {6: 12.5e6, 5: 450e3, 4: 40e3, 3: 10e3}, 5: {5: 4.4e6, 4: 150e3, 3: 10e3},
        4: {4: 400e3, 3: 50e3, 2: 10e3}, 3: {3: 200e3, 2: 20e3}, 2: {2: 90e3}, 1: {1: 20e3}}
D = [json.loads(l) for l in open('/home/user/vietvudanh/vietlott-data/data/keno.jsonl')]
D = list({d['id']: d for d in D}.values())  # kho có 26 kỳ bị ghi 2 dòng → bỏ trùng
D.sort(key=lambda d: int(d['id'].lstrip('#')))
X = np.zeros((len(D), 80), bool)
for i, d in enumerate(D): X[i, np.array(d['result']) - 1] = True
N = len(X); C = np.vstack([np.zeros(80, int), np.cumsum(X, 0)])
gap = np.zeros((N, 80), int); g = np.zeros(80, int)
for t in range(N): gap[t] = g; g = np.where(X[t], 0, g + 1)
def pick(t, how, n):
    if how == 'nóng 100 kỳ': s = -(C[t] - C[t - 100])
    elif how == 'lạnh 100 kỳ': s = C[t] - C[t - 100]
    elif how == 'nóng 20 kỳ': s = -(C[t] - C[t - 20])
    elif how == 'vắng lâu nhất': s = -gap[t]
    elif how == 'vừa ra, vắng ngắn': s = gap[t] + (C[t] - C[t - 100]) * -0.01
    elif how == 'cố định 1–n': return np.arange(n)
    return np.argsort(s, kind='stable')[:n]
print('## Lý thuyết mỗi bậc (vé 10.000đ)\n\n| Bậc | Trả thưởng TB | % kỳ có giải | Giải thường gặp nhất |\n|---|---|---|---|')
for n in range(10, 0, -1):
    p = {k: comb(20, k) * comb(60, n - k) / comb(80, n) for k in range(n + 1)}
    rtp = sum(p[k] * v for k, v in GIAI[n].items()) / 1e4
    kk = max(GIAI[n], key=lambda k: p[k])
    print(f'| {n} | {rtp * 100:.1f}% | {sum(p[k] for k in GIAI[n]) * 100:.1f}% | trúng {kk}: {GIAI[n][kk]:,.0f}đ ({p[kk] * 100:.1f}%) |')
HOW = ['nóng 100 kỳ', 'lạnh 100 kỳ', 'nóng 20 kỳ', 'vắng lâu nhất', 'cố định 1–n']
T0 = 200
for n in (7, 8, 9, 10):
    print(f'\n## Bậc {n} — tiền về / tiền bỏ (kỳ vọng {sum(comb(20,k)*comb(60,n-k)/comb(80,n)*v for k,v in GIAI[n].items())/1e4*100:.1f}%) · % kỳ có giải\n')
    print('| Cách chọn | 100 kỳ | 1000 kỳ | 10000 kỳ | Cả lịch sử | % kỳ có giải (cả LS) | TB số trúng (kỳ vọng ' + f'{n / 4:.2f}) |\n|---|---|---|---|---|---|---|')
    for how in HOW:
        hits = np.array([X[t][pick(t, how, n)].sum() for t in range(T0, N)])
        pay = np.array([GIAI[n].get(h, 0) for h in hits]) / 1e4
        f = lambda a: f'{a.mean() * 100:.0f}%'
        print(f'| {how} | ' + ' | '.join(f(pay[-w:]) for w in (100, 1000, 10000)) + f' | {f(pay)} | {np.isin(hits, list(GIAI[n])).mean() * 100:.1f}% | {hits.mean():.3f} |')
print(f'\nDữ liệu: {N} kỳ ({D[0]["date"]} → {D[-1]["date"]}). Tiền về 1 kỳ dao động rất mạnh (giải lớn hiếm) → khung 100–1000 kỳ có thể lệch hàng chục %; TB số trúng mới là thước đo ổn định.')
