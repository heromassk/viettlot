#!/usr/bin/env python3
"""Max 3D và Max 3D Pro dùng chung bộ quay (anh, 05/10/2026) → so chéo: kỳ Pro ngay trước ảnh hưởng gì kỳ 3D sau (và ngược lại).
Ghép theo ngày: mỗi kỳ của game này lấy kỳ gần nhất TRƯỚC ĐÓ của game kia (cách ≤3 ngày). Chấm cả lịch sử + 300 lần gần.
  python3 build/max3d_cheo.py"""
import json, os, datetime
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
P1 = 1 - 0.999 ** 20
def load(f):
    D = json.load(open(os.path.join(HERE, f)))
    return [datetime.datetime.strptime(d, '%d/%m/%Y').date() for d in D['dates']], D['res']
G = {'Max 3D': load('max3d_data.json'), 'Max 3D Pro': load('max3dpro_data.json')}
A = lambda s: {s[:i] + str((int(s[i]) + d) % 10) + s[i + 1:] for i in range(3) for d in (-1, 1)}
def cnt(r): return np.array([[sum(int(s[h]) == d for s in r) for d in range(10)] for h in range(3)])
def cr(a, b): return np.corrcoef(a, b)[0, 1] if a.std() and b.std() else np.nan
for tgt, src in (('Max 3D', 'Max 3D Pro'), ('Max 3D Pro', 'Max 3D')):
    dt, R = G[tgt]; ds, S = G[src]
    pairs = []
    j = 0
    for t in range(1, len(dt)):
        while j + 1 < len(ds) and ds[j + 1] < dt[t]: j += 1
        if ds[j] < dt[t] and (dt[t] - ds[j]).days <= 3: pairs.append((t, j))
    print(f'\n## {tgt} kỳ t ← {src} kỳ ngay trước ({len(pairs)} cặp kỳ)\n')
    print('| Nhóm từ kỳ trước | Cả lịch sử | 300 lần gần | So với: cùng game kỳ trước (cả lịch sử) |\n|---|---|---|---|')
    def rate(prs, fn, own=False):
        h = n = 0
        for t, j in prs:
            g = fn(R[t - 1] if own else S[j]); n += len(g); h += len(g & set(R[t]))
        return h / n / P1
    for nm, fn in (('20 bộ của kỳ trước', lambda r: set(r)), ('2 bộ ĐB kỳ trước', lambda r: set(r[:2])),
                   ('Lộn 2 bộ ĐB kỳ trước', lambda r: {s[::-1] for s in r[:2]} - set(r[:2])),
                   ('Quanh (±1 một chữ số) 20 bộ kỳ trước', lambda r: set().union(*[A(s) for s in r]) - set(r))):
        print(f'| {nm} | ×{rate(pairs, fn):.2f} | ×{rate(pairs[-300:], fn):.2f} | ×{rate(pairs, fn, True):.2f} |')
    # chữ số theo hàng: tương quan tần suất kỳ trước (game kia) ↔ kỳ này, so với cùng game
    v1 = [cr(cnt(S[j])[h], cnt(R[t])[h]) for t, j in pairs for h in range(3)]
    v2 = [cr(cnt(R[t - 1])[h], cnt(R[t])[h]) for t, j in pairs for h in range(3)]
    rng = np.random.default_rng(1); v0 = []
    for _ in range(len(v1)):
        a = rng.integers(0, 10, 20); b = rng.integers(0, 10, 20)
        v0.append(cr(np.bincount(a, minlength=10), np.bincount(b, minlength=10)))
    print(f'\n- Chữ số theo hàng: tương quan với kỳ trước của {src}: {np.nanmean(v1):+.3f} · với kỳ trước cùng game: {np.nanmean(v2):+.3f} · quay ngẫu nhiên: {np.nanmean(v0):+.3f} (±{np.nanstd(v0) / np.sqrt(len(v0)) * 2:.3f})')
    # kỳ tới
    t = len(dt); j = len(ds) - 1
print('\n## Kỳ gần nhất mỗi game')
for k, (d, R) in G.items(): print(f'- {k} {d[-1].strftime("%d/%m/%Y")}: ĐB {" ".join(R[-1][:2])} · Nhất {" ".join(R[-1][2:6])} · Nhì {" ".join(R[-1][6:12])} · Ba {" ".join(R[-1][12:])}')
