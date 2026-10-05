#!/usr/bin/env python3
"""Số May Mắn Loto — hướng LOẠI và POOL rộng (như số chính): % kỳ đúng trên 4 khung 10/20/50/100 kỳ + 100 kỳ trước đó.
  python3 build/somayman3.py"""
import json, os
D = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'all_data.json')))['loto535']
L = D['lk']; T = len(L); K = range(1, 13)
def gap(t, k): return next((g for g in range(t) if L[t - 1 - g] == k), t)
def cnt(t, W): return {k: sum(L[u] == k for u in range(max(0, t - W), t)) for k in K}
rk_vang = lambda t: sorted(K, key=lambda k: (-gap(t, k), k))
segs = {'10 kỳ': (T - 10, T), '20 kỳ': (T - 20, T), '50 kỳ': (T - 50, T), '100 kỳ': (T - 100, T), '100 kỳ trước': (T - 200, T - 100)}
def row(name, f, mode, base):
    v = []
    for a, b in segs.values():
        ok = sum((L[t] not in f(t)) if mode == 'loai' else (L[t] in f(t)) for t in range(a, b)); v.append(ok / (b - a) * 100)
    nx = ' '.join(f'{x:02d}' for x in sorted(f(T)))
    print(f'| {name} | {base:.0f}% | ' + ' | '.join(f'{x:.0f}%' for x in v) + f' | {nx} |')
H = '| {} | Chia đều | ' + ' | '.join(segs) + ' | Kỳ tới |\n|---|---|' + '---|' * (len(segs) + 1)
print('## A. LOẠI số May Mắn — % kỳ đúng (số bị loại không về)\n'); print(H.format('Luật loại'))
row('Loại MM vừa ra kỳ trước (1 số)', lambda t: {L[t - 1]}, 'loai', 11 / 12 * 100)
row('Loại 2 MM của 2 kỳ gần nhất', lambda t: {L[t - 1], L[t - 2]}, 'loai', 10 / 12 * 100)
row('Loại 3 MM của 3 kỳ gần nhất', lambda t: {L[t - 1], L[t - 2], L[t - 3]}, 'loai', 9 / 12 * 100)
row('Loại số ra ≥2 lần trong 10 kỳ', lambda t: {k for k, c in cnt(t, 10).items() if c >= 2}, 'loai', 0)
row('Loại số ra nhiều nhất 20 kỳ (top 2)', lambda t: set(sorted(K, key=lambda k: (-cnt(t, 20)[k], k))[:2]), 'loai', 10 / 12 * 100)
row('Loại số ra nhiều nhất 50 kỳ (top 2)', lambda t: set(sorted(K, key=lambda k: (-cnt(t, 50)[k], k))[:2]), 'loai', 10 / 12 * 100)
print('\n## B. POOL số May Mắn — chọn N số xếp theo "vắng lâu nhất", % kỳ trúng\n'); print(H.format('Pool'))
for n in (3, 4, 5, 6, 7, 8):
    row(f'{n} số vắng lâu nhất', lambda t, n=n: set(rk_vang(t)[:n]), 'pool', n / 12 * 100)
print('\n## C. POOL = bỏ các số vừa ra (3 kỳ gần) → còn lại\n'); print(H.format('Pool'))
row('Bỏ MM 3 kỳ gần → 9 số còn lại', lambda t: set(K) - {L[t - 1], L[t - 2], L[t - 3]}, 'pool', 0)
