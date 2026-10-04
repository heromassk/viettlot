#!/usr/bin/env python3
"""Nghiên cứu Số May Mắn Loto (1–12). Chạy tiến, chấm theo từng kỳ, 3 đoạn 150 kỳ (gần → xa).
  python3 build/somayman.py"""
import json, os
D = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'all_data.json')))['loto535']
L = D['lk']; R = [set(r) for r in D['res']]; S = ['13' if '13h' in x else '21' for x in D['dates']]; T = len(L); S.append('13' if S[-1] == '21' else '21')
segs = [(T - 150, T), (T - 300, T - 150), (T - 450, T - 300)]
def gap(t, k):
    g = 0
    while g < t and L[t - 1 - g] != k: g += 1
    return g
def cnt(t, k, w, ses=None):
    us = [u for u in range(max(0, t - w * (2 if ses else 1)), t) if ses is None or S[u] == ses][-w:]
    return sum(L[u] == k for u in us)
top = lambda d, n, rev=True: set(sorted(d, key=lambda k: ((-d[k]) if rev else d[k], k))[:n])
PICK = {   # chọn 3 số MM
    '3 MM vắng lâu nhất (đang dùng)': lambda t: top({k: gap(t, k) for k in range(1, 13)}, 3),
    '3 MM ít ra nhất 60 kỳ': lambda t: top({k: cnt(t, k, 60) for k in range(1, 13)}, 3, False),
    '3 MM ít ra nhất 120 kỳ': lambda t: top({k: cnt(t, k, 120) for k in range(1, 13)}, 3, False),
    '3 MM ít ra nhất CÙNG PHIÊN 60 kỳ': lambda t: top({k: cnt(t, k, 60, S[t]) for k in range(1, 13)}, 3, False),
    '3 MM vắng lâu nhất CÙNG PHIÊN': lambda t: top({k: next((i for i, u in enumerate([u for u in range(t - 1, -1, -1) if S[u] == S[t]]) if L[u] == k), 99) for k in range(1, 13)}, 3),
    '3 MM nóng nhất 30 kỳ': lambda t: top({k: cnt(t, k, 30) for k in range(1, 13)}, 3),
    'MM kỳ trước ±1 (3 số)': lambda t: {((L[t - 1] - 1 + d) % 12) + 1 for d in (-1, 0, 1)},
    'Số chính kỳ trước (≤12) làm MM': lambda t: {n for n in R[t - 1] if n <= 12} or {0},
    'Tổng kỳ trước mod 12 ±1': lambda t: {((sum(R[t - 1]) - 1 + d) % 12) + 1 for d in (-1, 0, 1)},
}
LOAI = {   # loại MM
    'Loại MM vừa ra kỳ trước': lambda t: {L[t - 1]},
    'Loại MM ra ≥2 lần trong 5 kỳ': lambda t: {k for k in range(1, 13) if sum(L[u] == k for u in range(t - 5, t)) >= 2},
    'Loại MM ra ≥3 lần trong 10 kỳ': lambda t: {k for k in range(1, 13) if sum(L[u] == k for u in range(t - 10, t)) >= 3},
    'Loại MM của kỳ cùng phiên hôm trước': lambda t: {L[t - 2]},
    'Loại 2 MM nóng nhất 20 kỳ': lambda t: top({k: cnt(t, k, 20) for k in range(1, 13)}, 2),
}
print('## Số May Mắn Loto — chọn 3 số: % kỳ trúng (3 đoạn 150 kỳ gần → xa). 3/12 số ⇒ phần "vé giữ lại" = 25%\n')
print('| Cách chọn 3 MM | Trúng: đoạn 1 | đoạn 2 | đoạn 3 | Kỳ tới |\n|---|---|---|---|---|')
for k, f in PICK.items():
    r = [sum(L[t] in f(t) for t in range(a, b)) / (b - a) * 100 for a, b in segs]
    sz = sum(len(f(t)) for t in range(T - 150, T)) / 150
    print(f"| {k}{'' if abs(sz - 3) < .05 else f' (TB {sz:.1f} số)'} | **{r[0]:.0f}%** | {r[1]:.0f}% | {r[2]:.0f}% | {' '.join(f'{x:02d}' for x in sorted(f(T)) if x)} |")
print('\n## Loại MM — % kỳ loại đúng (3 đoạn) · số bị loại TB\n')
print('| Luật | Đúng: đoạn 1 | đoạn 2 | đoạn 3 | Loại TB | Vé giữ lại | Kỳ tới loại |\n|---|---|---|---|---|---|---|')
for k, f in LOAI.items():
    r = [sum(L[t] not in f(t) for t in range(a, b)) / (b - a) * 100 for a, b in segs]
    sz = sum(len(f(t)) for t in range(T - 150, T)) / 150
    print(f"| {k} | **{r[0]:.0f}%** | {r[1]:.0f}% | {r[2]:.0f}% | {sz:.1f} | {(12 - sz) / 12 * 100:.0f}% | {' '.join(f'{x:02d}' for x in sorted(f(T)))} |")
# hiện trạng
print('\nHiện trạng MM: vắng ' + ', '.join(f'{k:02d}:{gap(T, k)}' for k in sorted(range(1, 13), key=lambda k: -gap(T, k))))
print('Ra 60 kỳ: ' + ', '.join(f'{k:02d}:{cnt(T, k, 60)}' for k in sorted(range(1, 13), key=lambda k: cnt(T, k, 60))))
print('10 kỳ gần: ' + ' '.join(f'{L[u]:02d}' for u in range(T - 10, T)))
