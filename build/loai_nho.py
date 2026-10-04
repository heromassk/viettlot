#!/usr/bin/env python3
"""Luật LOẠI kiểu "bỏ số vắng lâu": mỗi kỳ chỉ bỏ vài số, có lý do, chấm theo từng kỳ (kỳ đúng = không số bị bỏ nào về).
  python3 build/loai_nho.py power|mega|loto [--W 100]"""
import json, os, sys
from math import comb
GM = {'power': ('power655', 55, 6), 'mega': ('mega645', 45, 6), 'loto': ('loto535', 35, 5)}
key, NB, KB = GM[sys.argv[1]]
W = int(sys.argv[sys.argv.index('--W') + 1]) if '--W' in sys.argv else 100
D = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'all_data.json')))[key]
R = [set(r) for r in D['res']]; T = len(R)
def ctx(t):
    gap = {}
    for n in range(1, NB + 1):
        g = 0
        while g < t and n not in R[t - 1 - g]: g += 1
        gap[n] = g
    cnt = lambda w: {n: sum(n in R[u] for u in range(t - w, t)) for n in range(1, NB + 1)}
    return gap, cnt(5), cnt(10), cnt(100)
def topk(d, k, rev=False): return set(sorted(d, key=lambda n: ((-d[n]) if rev else d[n], n))[:k])
RULES = {
    'Số vắng lâu nhất (1 số)': lambda t, g, c5, c10, c100: topk(g, 1, True),
    'Số vắng lâu nhì (1 số)': lambda t, g, c5, c10, c100: topk(g, 2, True) - topk(g, 1, True),
    '2 số vắng lâu nhất': lambda t, g, c5, c10, c100: topk(g, 2, True),
    'Ra 2 kỳ liền': lambda t, g, c5, c10, c100: R[t - 1] & R[t - 2],
    'Ra 3 lần trong 5 kỳ': lambda t, g, c5, c10, c100: {n for n in c5 if c5[n] >= 3},
    'Ra kỳ trước VÀ kỳ t−3': lambda t, g, c5, c10, c100: R[t - 1] & R[t - 3],
    'Ra cả t−3 và t−6 (2 tuần liền cùng thứ)': lambda t, g, c5, c10, c100: R[t - 3] & R[t - 6] - R[t - 1],
    'Số "tái xuất" (kỳ trước, sau vắng ≥10)': lambda t, g, c5, c10, c100: {n for n in R[t - 1] if all(n not in R[u] for u in range(t - 11, t - 1))},
    'Số "tái xuất" sau vắng ≥15': lambda t, g, c5, c10, c100: {n for n in R[t - 1] if all(n not in R[u] for u in range(t - 16, t - 1))},
    'Nóng nhất 10 kỳ (1 số, ≥4 lần)': lambda t, g, c5, c10, c100: {n for n in topk(c10, 1, True) if c10[n] >= 4},
    'Ra ít nhất 100 kỳ (1 số)': lambda t, g, c5, c10, c100: topk(c100, 1),
    'Ra nhiều nhất 100 kỳ (1 số)': lambda t, g, c5, c10, c100: topk(c100, 1, True),
    'Kỳ trước: số nhỏ nhất (u)': lambda t, g, c5, c10, c100: {min(R[t - 1])},
    'Kỳ trước: số lớn nhất (z)': lambda t, g, c5, c10, c100: {max(R[t - 1])},
    'Kỳ trước: cặp liền nhau (cả 2 số)': lambda t, g, c5, c10, c100: {n for n in R[t - 1] if n + 1 in R[t - 1] or n - 1 in R[t - 1]},
    'Vắng ≥2×nhịp TB riêng & ≥20': lambda t, g, c5, c10, c100: {n for n in g if g[n] >= 20 and c100[n] and g[n] >= 2 * 100 / c100[n]},
}
segs = [(f'{W} kỳ gần', T - W, T), (f'{W} kỳ trước', T - 2 * W, T - W), (f'{W} kỳ xa hơn', T - 3 * W, T - 2 * W)]
print(f'## {key} — luật loại nhỏ (kỳ đúng = không số bị bỏ nào về)\n')
print('| Luật | Đúng: ' + ' | '.join(s[0] for s in segs) + ' | Bỏ TB/kỳ | Vé giữ lại | Đánh giá |\n|---|---|---|---|---|---|---|')
C = {t: ctx(t) for t in range(T - 3 * W, T + 1)}
for k, f in RULES.items():
    rs, bo, kp = [], 0, 0
    for i, (_, a, b) in enumerate(segs):
        ok = 0
        for t in range(a, b):
            ex = f(t, *C[t]); ok += not (ex & R[t])
            if i == 0: bo += len(ex); kp += comb(NB - len(ex), KB) / comb(NB, KB)
        rs.append(ok / (b - a) * 100)
    kp = kp / W * 100
    tag = '✔ mạnh' if min(rs) >= 85 and min(rs) >= kp - 1 and sum(rs) / 3 > kp else ('~ theo dõi' if min(rs) >= 80 and sum(rs) / 3 >= kp else '✘')
    ex = f(T, *C[T])
    print(f'| {k} | ' + ' | '.join(f'**{r:.0f}%**' if j == 0 else f'{r:.0f}%' for j, r in enumerate(rs)) + f' | {bo / W:.1f} | {kp:.0f}% | {tag} · kỳ tới: {" ".join(f"{n:02d}" for n in sorted(ex)) or "—"} |')
