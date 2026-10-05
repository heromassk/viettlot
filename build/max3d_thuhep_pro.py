#!/usr/bin/env python3
"""Max 3D Pro — thử các cách thu hẹp pool từ ~640 bộ xuống ~300–450. Mỗi cách: cỡ pool TB, % bộ trúng nằm trong pool so với % pool (chia đều), 3 đoạn 100 kỳ gần → xa,
và % kỳ cả 2 bộ ĐB nằm trong pool (chia đều = (cỡ/1000)²).
  python3 build/max3d_thuhep_pro.py [--file build/max3d_data.json]"""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
f = sys.argv[sys.argv.index('--file') + 1] if '--file' in sys.argv else os.path.join(HERE, 'max3dpro_data.json')
L = json.load(open(f))['res']; T = len(L); ALL = [f'{i:03d}' for i in range(1000)]
X = np.array([[[int(c) for c in s] for s in r] for r in L])
TIEN = {'012', '123', '234', '345', '456', '567', '678', '789'}; TH = {d * 3 for d in '0123456789'}; O0 = {f'00{d}' for d in '0123456789'}
KK = {s for s in ALL if s[0] == s[2] != s[1]}; Z = {s for s in ALL if (s[0] == '0' and s[2] == '0') or s[1:] == '00'}
def weight(t, W):
    c = np.stack([np.bincount(X[t - W:t, :, h].ravel(), minlength=10) for h in range(3)]) + 1.0
    return {s: c[0][int(s[0])] * c[1][int(s[1])] * c[2][int(s[2])] for s in ALL}
def base(t, NG): return set(ALL) - {s for r in L[t - NG:t] for s in r} - TIEN - TH - O0
def keep_top(t, S, W, k): w = weight(t, W); return set(sorted(S, key=lambda s: -w[s])[:k])
def keep_bot(t, S, W, k): w = weight(t, W); return set(sorted(S, key=lambda s: w[s])[:k])
M = {
    'Hiện tại: bỏ ra 20 kỳ, tiến, tam hoa, 00x': lambda t: base(t, 20),
    'Bỏ ra 30 kỳ (+ tiến, tam hoa, 00x)': lambda t: base(t, 30),
    'Bỏ ra 50 kỳ': lambda t: base(t, 50),
    'Bỏ ra 20 kỳ + kép kẹp + 0x0/x00': lambda t: base(t, 20) - KK - Z,
    'Bỏ ra 30 kỳ + kép kẹp + 0x0/x00': lambda t: base(t, 30) - KK - Z,
    'Hiện tại → giữ 340 bộ nặng 20 kỳ': lambda t: keep_top(t, base(t, 20), 20, 340),
    'Hiện tại → giữ 340 bộ nặng 100 kỳ': lambda t: keep_top(t, base(t, 20), 100, 340),
    'Bỏ ra 30 kỳ → giữ 340 bộ nặng 100 kỳ': lambda t: keep_top(t, base(t, 30), 100, 340),
    'Bỏ ra 30 kỳ → giữ 400 bộ nặng 100 kỳ': lambda t: keep_top(t, base(t, 30), 100, 400),
    'Hiện tại → giữ 340 bộ NHẸ 20 kỳ (ngược)': lambda t: keep_bot(t, base(t, 20), 20, 340),
}
segs = [(T - 100, T), (T - 200, T - 100), (T - 300, T - 200)]
print(f'## {os.path.basename(f)}\n\n| Cách | Cỡ pool | Bộ trúng trong pool (gần · giữa · xa) | Chia đều | Cả 2 ĐB trong pool | Chia đều |\n|---|---|---|---|---|---|')
for k, fn in M.items():
    hs = []; db = []; sz = 0
    for a, b in segs:
        h = e = d = 0
        for t in range(a, b):
            P = fn(t); sz += len(P); h += sum(s in P for s in L[t]); d += L[t][0] in P and L[t][1] in P
        hs.append(h / (20 * (b - a)) * 100); db.append(d)
    m = sz / 300
    print(f'| {k} | {m:.0f} | ' + ' · '.join(f'{x:.1f}%' for x in hs) + f' | {m / 10:.1f}% | ' + ' · '.join(f'{x}%' for x in db) + f' | {(m / 1000) ** 2 * 100:.0f}% |')
