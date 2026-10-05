#!/usr/bin/env python3
"""Keno: kiểm kỹ 10 kỳ gần nhất — có ra lặp lại không (anh, 05/10/2026).
1) Từng kỳ: trùng mấy số với kỳ ngay trước (kỳ vọng 5,0), với 2/3 kỳ trước.
2) Số ra nhiều trong 10 kỳ (kỳ vọng 2,5 lần).
3) Luật: số ra ≥k lần trong 10 kỳ → kỳ kế ra bao nhiêu % (25%), khung 10/20/50/100, 3 đoạn 100, 5000 kỳ, cả lịch sử.
  python3 build/keno_10ky.py"""
import json, numpy as np
D = [json.loads(l) for l in open('/home/user/vietvudanh/vietlott-data/data/keno.jsonl')]
D = list({d['id']: d for d in D}.values())  # kho có 26 kỳ bị ghi 2 dòng → bỏ trùng
D.sort(key=lambda d: int(d['id'].lstrip('#')))
X = np.zeros((len(D), 80), bool)
for i, d in enumerate(D): X[i, np.array(d['result']) - 1] = True
N = len(X)
print('## 1. 10 kỳ gần nhất — trùng với kỳ trước (kỳ vọng 5,0 số)\n\n| Kỳ | Ngày | 20 số | Trùng kỳ trước | Số trùng | Trùng 1 trong 2–3 kỳ trước |\n|---|---|---|---|---|---|')
for t in range(N - 10, N):
    tr = np.flatnonzero(X[t] & X[t - 1]) + 1; t23 = np.flatnonzero(X[t] & ~X[t - 1] & (X[t - 2] | X[t - 3])) + 1
    print(f'| {D[t]["id"]} | {D[t]["date"]} | {" ".join(f"{n:02d}" for n in D[t]["result"])} | **{len(tr)}** | {" ".join(f"{n:02d}" for n in tr)} | {len(t23)} |')
ov = (X[1:] & X[:-1]).sum(1)
print(f'\nTB trùng kỳ trước: 10 kỳ gần {ov[-10:].mean():.2f} · 100 kỳ {ov[-100:].mean():.2f} · cả lịch sử {ov.mean():.3f} (kỳ vọng 5,000; 10 kỳ dao động ±0,6)')
c10 = X[-10:].sum(0)
print('\n## 2. Số ra trong 10 kỳ gần nhất (kỳ vọng 2,5 lần)\n')
for k in range(c10.max(), -1, -1):
    s = np.flatnonzero(c10 == k) + 1
    if len(s): print(f'- {k} lần ({len(s)} số): ' + ' '.join(f'{n:02d}' for n in s))
from math import comb
exp = [80 * comb(10, k) * .25 ** k * .75 ** (10 - k) for k in range(11)]
print('\nSo với ngẫu nhiên (số lượng số ra k lần): ' + ' · '.join(f'{k}: {(c10 == k).sum()} (≈{exp[k]:.1f})' for k in range(0, 8)))
print('\n## 3. Luật: số ra nhiều/ít trong 10 kỳ → kỳ kế (kỳ vọng 25,0%)\n')
C = np.vstack([np.zeros(80, int), np.cumsum(X, 0)])
G = {'≥5 lần': lambda c: c >= 5, '4 lần': lambda c: c == 4, '3 lần': lambda c: c == 3, '2 lần': lambda c: c == 2, '1 lần': lambda c: c == 1, '0 lần': lambda c: c == 0}
R = {k: [] for k in G}
for t in range(10, N):
    c = C[t] - C[t - 10]
    for k, f in G.items():
        m = f(c); R[k].append(X[t][m].mean() if m.any() else np.nan)
f = lambda a: f'{np.nanmean(a) * 100:.1f}%'
print('| Ra trong 10 kỳ trước | 10 kỳ | 20 kỳ | 50 kỳ | 100 kỳ | 3 đoạn 100 kỳ | 5000 kỳ | Cả lịch sử |\n|---|---|---|---|---|---|---|---|')
for k, a in R.items():
    a = np.array(a); n = len(a)
    print(f'| {k} | ' + ' | '.join(f(a[-w:]) for w in (10, 20, 50, 100)) + ' | ' + ' · '.join(f(a[n - 100 * (i + 1):n - 100 * i]) for i in range(3)) + f' | {f(a[-5000:])} | {f(a)} |')
