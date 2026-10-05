#!/usr/bin/env python3
"""Max 3D+ / Pro — GỘP dấu vết để loại bớt bộ số: điểm bộ = tích độ nặng chữ số theo hàng (khung W kỳ, cả 20 bộ) ; bỏ bộ vừa ra kỳ trước.
Giữ lại p% bộ điểm cao nhất → % bộ trúng (20 bộ/kỳ) nằm trong nhóm giữ, và % kỳ cả 2 bộ ĐB đều nằm trong nhóm giữ.
Chia đều: bộ trúng trong nhóm = p%; cả 2 ĐB = p%². Chấm 3 đoạn 100 kỳ gần → xa.
  python3 build/max3d_loai.py [--file build/max3dpro_data.json]"""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
f = sys.argv[sys.argv.index('--file') + 1] if '--file' in sys.argv else os.path.join(HERE, 'max3d_data.json')
D = json.load(open(f)); L = D['res']; T = len(L)
X = np.array([[[int(c) for c in s] for s in r] for r in L])
IDX = np.array([[i // 100, i // 10 % 10, i % 10] for i in range(1000)])
def score(t, W):
    c = np.stack([np.bincount(X[t - W:t, :, h].ravel(), minlength=10) for h in range(3)]) + 1.0
    lc = np.log(c / c.sum(1, keepdims=True) * 10)
    return lc[0][IDX[:, 0]] + lc[1][IDX[:, 1]] + lc[2][IDX[:, 2]]
segs = [(T - 100, T), (T - 200, T - 100), (T - 300, T - 200)]
print(f'## {os.path.basename(f)} — giữ lại p% bộ điểm cao (gộp dấu vết)\n')
print('| Cách | Giữ | Bộ trúng nằm trong nhóm giữ (gần · giữa · xa) | Chia đều | Cả 2 ĐB trong nhóm giữ | Chia đều |\n|---|---|---|---|---|---|')
import itertools
for (W, NG), p in itertools.product([(50, 1), (50, 5), (50, 10), (50, 20)], (50, 34)):
    if True:
        k = p * 10; a1 = []; a2 = []
        for a, b in segs:
            h = n = e = 0
            for t in range(a, b):
                sc = score(t, W); prev = sorted({int(s) for u in range(t - NG, t) for s in L[u]}); sc[prev] -= 99
                keep = set(np.argsort(-sc)[:k].tolist()); nums = [int(s) for s in L[t]]
                h += sum(x in keep for x in nums); n += 20; e += nums[0] in keep and nums[1] in keep
            a1.append(h / n * 100); a2.append(e / (b - a) * 100)
        print(f'| Nặng {W} kỳ + bỏ bộ đang nghỉ (ra trong {NG} kỳ gần) | {p}% | ' + ' · '.join(f'{x:.1f}%' for x in a1) + f' | {p}% | ' + ' · '.join(f'{x:.0f}%' for x in a2) + f' | {p * p / 100:.0f}% |')
