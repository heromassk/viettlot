#!/usr/bin/env python3
"""Keno: chép số kỳ trước mua ngay kỳ sau (anh, 05/10/2026) — chấm bậc 7–10 trên dữ liệu thật (đã bỏ 26 dòng trùng của kho).
  python3 build/keno_chep.py"""
import json, numpy as np
from math import comb
D = [json.loads(l) for l in open('/home/user/vietvudanh/vietlott-data/data/keno.jsonl')]
D = list({d['id']: d for d in D}.values()); D.sort(key=lambda d: int(d['id'].lstrip('#')))
X = np.zeros((len(D), 80), bool)
for i, d in enumerate(D): X[i, np.array(d['result']) - 1] = True
N = len(X); C = np.vstack([np.zeros(80, int), np.cumsum(X, 0)])
GIAI = {10: {10: 2e9, 9: 150e6, 8: 7.4e6, 7: 600e3, 6: 80e3, 5: 20e3, 0: 10e3},
        9: {9: 800e6, 8: 12e6, 7: 1.5e6, 6: 150e3, 5: 30e3, 4: 10e3, 0: 10e3},
        8: {8: 200e6, 7: 5e6, 6: 500e3, 5: 50e3, 4: 10e3, 0: 10e3},
        7: {7: 40e6, 6: 1.2e6, 5: 100e3, 4: 20e3, 3: 10e3}}
def rep(t, n):  # số kỳ trước, ưu tiên số vừa lặp (ra cả t-1 và t-2), rồi số nóng 10 kỳ
    s = X[t - 1] * 100 + X[t - 2] * 10 + (C[t] - C[t - 10])
    return np.argsort(-s, kind='stable')[:n]
CACH = {'chép n số đầu kỳ trước': lambda t, n: np.flatnonzero(X[t - 1])[:n],
        'chép số kỳ trước, ưu tiên số vừa lặp + nóng 10 kỳ': rep}
ov = (X[1:] & X[:-1]).sum(1); p = lambda k: comb(20, k) * comb(60, 20 - k) / comb(80, 20)
print(f'Dữ liệu {N} kỳ. Kỳ sau trùng ≥9 số với kỳ trước: thực tế {(ov >= 9).sum()} lần, lý thuyết {sum(p(k) for k in range(9, 21)) * (N - 1):.0f}\n')
print('| Cách | Bậc | Trúng hết (thực tế / kỳ vọng) | Trúng thiếu 1 (thực tế / kỳ vọng) | TB số trúng (kỳ vọng) | Tiền về |\n|---|---|---|---|---|---|')
for nm, f in CACH.items():
    for n in (7, 8, 9, 10):
        h = np.array([X[t][f(t, n)].sum() for t in range(10, N)]); m = len(h)
        q = lambda k: comb(20, k) * comb(60, n - k) / comb(80, n)
        pay = np.array([GIAI[n].get(k, 0) for k in h]).sum() / (m * 1e4)
        print(f'| {nm} | {n} | {(h == n).sum()} / {m * q(n):.2f} | {(h == n - 1).sum()} / {m * q(n - 1):.1f} | {h.mean():.3f} ({n / 4:.2f}) | {pay * 100:.0f}% |')
