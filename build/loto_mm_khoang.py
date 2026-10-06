#!/usr/bin/env python3
"""Loto 5/35 — số May Mắn (1–12) theo KHOẢNG (anh, 06/10/2026): chia 3 khoảng (1–4, 5–8, 9–12), 4 khoảng (1–3…), 6 khoảng (1–2…).
Thử các cách chọn 1 khoảng (cố định qua các kỳ), chấm % kỳ MM rơi vào khoảng chọn, so với chia đều (1/3, 1/4, 1/6).
Khung 10/20/50/100/200 kỳ + 3 đoạn 100 kỳ + cả lịch sử. Thêm luật LOẠI 1 khoảng (đúng = MM không rơi vào khoảng bị loại).
  python3 build/loto_mm_khoang.py"""
import json, os
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
A = json.load(open(os.path.join(HERE, 'all_data.json')))['loto535']
MM, DT = A['lk'], A['dates']; N = len(MM)
SES = ['13' if '13h' in d else '21' for d in DT]; SES.append('13' if SES[-1] == '21' else '21')
def run(K):
    w = 12 // K; g = [(m - 1) // w for m in MM]
    def most(t, W, rev=False):
        c = Counter(g[max(0, t - W):t]); return min(range(K), key=lambda k: ((c[k] if rev else -c[k]), k))
    def gapk(t):
        last = {k: -1 for k in range(K)}
        for u in range(t): last[g[u]] = u
        return last
    def markov(t, W=200):
        c = Counter(g[u] for u in range(max(1, t - W), t) if g[u - 1] == g[t - 1])
        return max(range(K), key=lambda k: (c[k], -k))
    def phien(t, W=100):
        c = Counter(g[u] for u in range(max(0, t - 3 * W), t) if SES[u] == SES[t]); return max(range(K), key=lambda k: (c[k], -k))
    M = {'Khoảng kỳ trước (lặp lại)': lambda t: g[t - 1],
         'Khoảng kỳ t−2': lambda t: g[t - 2],
         'Nhiều nhất 10 kỳ': lambda t: most(t, 10), 'Nhiều nhất 20 kỳ': lambda t: most(t, 20),
         'Nhiều nhất 50 kỳ': lambda t: most(t, 50), 'Nhiều nhất 100 kỳ': lambda t: most(t, 100),
         'Ít nhất 10 kỳ': lambda t: most(t, 10, True), 'Ít nhất 20 kỳ': lambda t: most(t, 20, True),
         'Ít nhất 50 kỳ': lambda t: most(t, 50, True),
         'Vắng lâu nhất': lambda t: min(range(K), key=lambda k: gapk(t)[k]),
         'Hay theo sau khoảng kỳ trước (200 kỳ)': markov,
         'Nhiều nhất cùng phiên (13h/21h)': phien}
    T0 = 200; base = 1 / K
    print(f'\n## Chia {K} khoảng: ' + ' · '.join(f'{k * w + 1}–{k * w + w}' for k in range(K)) + f' (chia đều {base * 100:.1f}%)\n')
    c = Counter(g); print('Cả lịch sử mỗi khoảng: ' + ' · '.join(f'{k * w + 1}–{k * w + w}: {c[k] / N * 100:.1f}%' for k in range(K)))
    c = Counter(g[-100:]); print('100 kỳ gần: ' + ' · '.join(f'{c[k]}%' for k in range(K)) + '\n')
    print('| Cách chọn 1 khoảng | 10 kỳ | 20 kỳ | 50 kỳ | 100 kỳ | 200 kỳ | 3 đoạn 100 kỳ (gần→xa) | Cả LS | Kỳ tới |\n|---|---|---|---|---|---|---|---|---|')
    for nm, f in M.items():
        h = [g[t] == f(t) for t in range(T0, N)]; p = lambda a: f'{sum(a) / len(a) * 100:.0f}%'
        seg = ' · '.join(p(h[len(h) - 100 * (i + 1):len(h) - 100 * i]) for i in range(3))
        nx = f(N); print(f'| {nm} | ' + ' | '.join(p(h[-W:]) for W in (10, 20, 50, 100, 200)) + f' | {seg} | {p(h)} | {nx * w + 1}–{nx * w + w} |')
for K in (3, 4, 6): run(K)
print('\nNgẫu nhiên: khung 100 kỳ dao động ±5 (3 khoảng) · ±4 (4 khoảng) · ±4 (6 khoảng) điểm; 10 kỳ ±15 điểm.')
