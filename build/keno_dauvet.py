#!/usr/bin/env python3
"""Keno 20/80 — kiểm nhanh dấu vết (anh hỏi 05/10/2026). Dữ liệu: kho vietvudanh/vietlott-data (keno.jsonl).
Mỗi kỳ ra 20/80 số → mỗi số ra 25%. Đo tỉ lệ ra kỳ sau của từng nhóm số, khung 10/20/50/100 kỳ, 3 đoạn 100 kỳ, 5000 kỳ, cả lịch sử.
  python3 build/keno_dauvet.py"""
import json, numpy as np
D = [json.loads(l) for l in open('/home/user/vietvudanh/vietlott-data/data/keno.jsonl')]
D.sort(key=lambda d: int(d['id'].lstrip('#')))
X = np.zeros((len(D), 81), bool)
for i, d in enumerate(D): X[i, d['result']] = True
X = X[:, 1:]; N = len(X)
C = np.cumsum(np.vstack([np.zeros(80, int), X]), 0)   # C[t] = số lần ra trong kỳ 0..t-1
gap = np.zeros((N, 80), int); g = np.zeros(80, int)
for t in range(N): gap[t] = g; g = np.where(X[t], 0, g + 1)   # gap[t]: đang vắng trước kỳ t
def grp(t, kind):
    if kind == 'ra kỳ trước': return X[t - 1]
    if kind == 'vắng ≥5 kỳ': return gap[t] >= 5
    if kind == 'vắng ≥10 kỳ': return gap[t] >= 10
    if kind == 'vắng ≥15 kỳ': return gap[t] >= 15
    w = int(kind.split()[-2]); c = C[t] - C[t - w]
    o = np.argsort(-c, kind='stable')
    m = np.zeros(80, bool); m[o[:10] if kind.startswith('10 nóng') else o[-10:]] = True; return m
KINDS = ['ra kỳ trước', 'vắng ≥5 kỳ', 'vắng ≥10 kỳ', 'vắng ≥15 kỳ', '10 nóng nhất 20 kỳ', '10 lạnh nhất 20 kỳ', '10 nóng nhất 100 kỳ', '10 lạnh nhất 100 kỳ', '10 nóng nhất 500 kỳ', '10 lạnh nhất 500 kỳ']
T0 = 600
rate = {k: np.full(N, np.nan) for k in KINDS}
for t in range(T0, N):
    for k in KINDS:
        m = grp(t, k)
        if m.any(): rate[k][t] = X[t][m].mean()
f = lambda a: f'{np.nanmean(a) * 100:.1f}%'
print(f'Keno: {N} kỳ ({D[0]["date"]} → {D[-1]["date"]}); kỳ vọng 25,0%\n')
print('| Nhóm | 10 kỳ | 20 kỳ | 50 kỳ | 100 kỳ | 3 đoạn 100 kỳ | 5000 kỳ | Cả lịch sử |\n|---|---|---|---|---|---|---|---|')
for k in KINDS:
    a = rate[k]
    print(f'| {k} | ' + ' | '.join(f(a[-w:]) for w in (10, 20, 50, 100)) + ' | ' + ' · '.join(f(a[N - 100 * (i + 1):N - 100 * i]) for i in range(3)) + f' | {f(a[-5000:])} | {f(a[T0:])} |')
# số ra lệch lâu dài?
tot = X.sum(0); e = N * .25; sd = np.sqrt(N * .25 * .75)
z = (tot - e) / sd
print(f'\nTần suất cả lịch sử: lệch lớn nhất z = {z.max():+.1f} (số {z.argmax() + 1}), nhỏ nhất {z.min():+.1f} (số {z.argmin() + 1}); ngẫu nhiên 80 số thường trong ±2,5.')
h1, h2 = X[:N // 2].mean(0), X[N // 2:].mean(0)
print(f'Tương quan tần suất nửa đầu ↔ nửa sau: {np.corrcoef(h1, h2)[0, 1]:+.3f} (0 = không có số "ruột")')
