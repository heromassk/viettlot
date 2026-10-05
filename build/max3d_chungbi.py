#!/usr/bin/env python3
"""Max 3D và Max 3D Pro có dùng CHUNG bộ bi/máy không? Dự đoán chữ số theo hàng của kỳ kế bằng độ nặng lấy từ:
(a) chính game đó, (b) game kia, (c) gộp cả 2 — các kỳ quay TRƯỚC ngày đó trong W ngày gần. 5 chữ số nặng nhất mỗi hàng → % chữ số kỳ kế rơi vào (chia đều 50%).
  python3 build/max3d_chungbi.py"""
import json, os, datetime
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
def load(f):
    D = json.load(open(os.path.join(HERE, f)))
    return [datetime.datetime.strptime(d, '%d/%m/%Y').date() for d in D['dates']], np.array([[[int(c) for c in s] for s in r] for r in D['res']])
G = {'Max 3D': load('max3d_data.json'), 'Max 3D Pro': load('max3dpro_data.json')}
def counts(game, day, W):
    ds, X = G[game]; idx = [i for i, d in enumerate(ds) if day - datetime.timedelta(days=W) <= d < day]
    return np.stack([np.bincount(X[idx, :, h].ravel(), minlength=10) for h in range(3)]) if idx else np.zeros((3, 10))
print('| Đích | Độ nặng lấy từ | Khung | Đoạn 1 (gần) | Đoạn 2 | Đoạn 3 |\n|---|---|---|---|---|---|')
for tgt, oth in (('Max 3D', 'Max 3D Pro'), ('Max 3D Pro', 'Max 3D')):
    ds, X = G[tgt]; T = len(ds)
    for W in (45, 120):
        for src in ('chính nó', 'game kia', 'gộp cả 2'):
            out = []
            for a, b in ((T - 100, T), (T - 200, T - 100), (T - 300, T - 200)):
                h = n = 0
                for t in range(a, b):
                    c = counts(tgt, ds[t], W) * (src != 'game kia') + counts(oth, ds[t], W) * (src != 'chính nó')
                    for k in range(3):
                        top = np.argsort(-c[k] - np.arange(10) * 1e-6)[:5]; h += np.isin(X[t, :, k], top).sum(); n += 20
                out.append(h / n * 100)
            print(f'| {tgt} | {src} | {W} ngày (~{W * 3 // 7} kỳ) | ' + ' | '.join(f'{x:.1f}%' for x in out) + ' |')
