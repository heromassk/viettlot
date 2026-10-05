#!/usr/bin/env python3
"""Số May Mắn Loto (1–12): chấm mọi cách chọn 3 số trên 4 khung gần 10/20/50/100 kỳ (+ đoạn 100 kỳ trước đó).
Trung bình chọn 3/12 số = 25%. Chọn 1 số = 8,3%.
  python3 build/somayman2.py"""
import json, os
D = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'all_data.json')))['loto535']
L = D['lk']; R = [set(r) for r in D['res']]; DT = D['dates']; T = len(L)
S = ['13' if '13h' in d else '21' for d in DT]
K = range(1, 13)
SNEXT = lambda t: S[t] if t < T else ('13' if S[-1] == '21' else '21')
def gap(t, k, same=False):
    g = 0
    for u in range(t - 1, -1, -1):
        if same and S[u] != SNEXT(t): continue
        if L[u] == k: return g
        g += 1
    return g
def cnt(t, W): return {k: sum(L[u] == k for u in range(max(0, t - W), t)) for k in K}
def top(sc, n=3): return sorted(K, key=lambda k: (-sc[k], k))[:n]
M = {
    'Vắng lâu nhất (đang dùng)': lambda t: top({k: gap(t, k) for k in K}),
    'Vắng ngắn nhất (vừa ra)': lambda t: top({k: -gap(t, k) for k in K}),
    'MM kỳ trước + 2 vắng lâu nhất': lambda t: [L[t - 1]] + [k for k in top({k: gap(t, k) for k in K}, 4) if k != L[t - 1]][:2],
    'Nóng 10 kỳ': lambda t: top(cnt(t, 10)),
    'Nóng 20 kỳ': lambda t: top(cnt(t, 20)),
    'Nóng 50 kỳ': lambda t: top(cnt(t, 50)),
    'Nóng 100 kỳ': lambda t: top(cnt(t, 100)),
    'Lạnh 20 kỳ': lambda t: top({k: -c for k, c in cnt(t, 20).items()}),
    'Lạnh 50 kỳ': lambda t: top({k: -c for k, c in cnt(t, 50).items()}),
    'Lạnh 100 kỳ': lambda t: top({k: -c for k, c in cnt(t, 100).items()}),
    'Vắng lâu nhất cùng phiên (13h/21h)': lambda t: top({k: gap(t, k, True) for k in K}),
    'Nóng 20 kỳ cùng phiên': lambda t: top({k: sum(L[u] == k for u in [u for u in range(t) if S[u] == SNEXT(t)][-20:]) for k in K}),
    'MM kỳ trước ±1 (3 số)': lambda t: [((L[t - 1] + d - 1) % 12) + 1 for d in (-1, 0, 1)],
    'MM trùng số chính kỳ trước (≤12)': lambda t: (sorted(n for n in R[t - 1] if n <= 12) + top({k: gap(t, k) for k in K}, 12))[:3],
    'Đuôi số chính kỳ trước (n mod 12)': lambda t: list(dict.fromkeys([((n - 1) % 12) + 1 for n in sorted(R[t - 1])]))[:3],
    'Tổng kỳ trước mod 12 ±1': lambda t: [((sum(R[t - 1]) + d - 1) % 12) + 1 for d in (-1, 0, 1)],
}
segs = {'10 kỳ': (T - 10, T), '20 kỳ': (T - 20, T), '50 kỳ': (T - 50, T), '100 kỳ': (T - 100, T), '100 kỳ trước đó': (T - 200, T - 100)}
print('## Số May Mắn Loto — chọn 3 số, % kỳ trúng (trung bình 25%)\n')
print('| Cách chọn | ' + ' | '.join(segs) + ' | Kỳ tới |\n|---|' + '---|' * (len(segs) + 1))
for k, f in M.items():
    row = [sum(L[t] in f(t) for t in range(a, b)) / (b - a) * 100 for a, b in segs.values()]
    print(f'| {k} | ' + ' | '.join(f'{x:.0f}%' for x in row) + f' | {" ".join(f"{x:02d}" for x in f(T))} |')
# lặp lại, khoảng cách lặp
rep = [L[t] == L[t - 1] for t in range(T - 100, T)]
print(f'\n- MM lặp lại kỳ trước: {sum(rep)}% ở 100 kỳ (ngẫu nhiên 8,3%)')
dist = {}
for t in range(T - 100, T): g = gap(t, L[t]); dist[min(g, 30)] = dist.get(min(g, 30), 0) + 1
print('- Số ra lúc đang vắng bao lâu (100 kỳ): ' + ', '.join(f'{a}–{b}: {sum(dist.get(g, 0) for g in range(a, b + 1))}%' for a, b in ((0, 2), (3, 5), (6, 11), (12, 20), (21, 30))))
print(f'  (ngẫu nhiên: 0–2: 23%, 3–5: 18%, 6–11: 24%, 12–20: 21%, ≥21: 14%)')
print('- Đang vắng: ' + ', '.join(f'{k:02d}: {gap(T, k)}' for k in sorted(K, key=lambda k: -gap(T, k))))
print('- 10 kỳ gần: ' + ' '.join(f'{L[t]:02d}' for t in range(T - 10, T)))
