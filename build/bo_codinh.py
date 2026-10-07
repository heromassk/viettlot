#!/usr/bin/env python3
"""Power / Mega — mua cố định 1 bộ suốt quá trình: thử các cách CHỌN bộ (anh, 07/10/2026).
Chọn bộ bằng dữ liệu "học" (các kỳ trước mốc), giữ nguyên, chấm trên các kỳ SAU mốc (không nhìn trước). Nhiều mốc trượt để ổn định.
So với phân bố của 3000 bộ chọn bừa. Đo: TB số trúng/kỳ, số kỳ trúng ≥3.
  python3 build/bo_codinh.py"""
import json, os, random, itertools
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
A = json.load(open(os.path.join(HERE, 'all_data.json')))
random.seed(7)
def greedy_pairs(R, NB):
    pc = Counter(p for r in R for p in itertools.combinations(sorted(r), 2)); f = Counter(x for r in R for x in r)
    best = None
    for (a, b), _ in pc.most_common(30):
        s = [a, b]
        while len(s) < 6:
            s.append(max((n for n in range(1, NB + 1) if n not in s), key=lambda n: sum(pc[tuple(sorted((n, m)))] for m in s)))
        sc = sum(pc[tuple(sorted(p))] for p in itertools.combinations(s, 2))
        if best is None or sc > best[0]: best = (sc, sorted(s))
    return best[1]
def greedy_triples(R, NB):          # bộ "trung tâm": hay trùng ≥3 số với các kỳ cũ
    s = []
    while len(s) < 6:
        s.append(max((n for n in range(1, NB + 1) if n not in s), key=lambda n: sum(len(r & set(s + [n])) ** 3 for r in R)))
    return sorted(s)
RULES = {
    'Ra nhiều nhất cả quá khứ': lambda R, NB: [n for n, _ in Counter(x for r in R for x in r).most_common(6)],
    'Ra nhiều nhất 100 kỳ gần': lambda R, NB: [n for n, _ in Counter(x for r in R[-100:] for x in r).most_common(6)],
    'Ra ít nhất 100 kỳ gần': lambda R, NB: sorted(range(1, NB + 1), key=lambda n: sum(n in r for r in R[-100:]))[:6],
    'Cặp hay đi cùng nhất (gắn kết)': greedy_pairs,
    'Bộ "trung tâm" (hay trùng ≥3 số với kỳ cũ)': greedy_triples,
}
for g, key, NB in (('POWER', 'power655', 55), ('MEGA', 'mega645', 45)):
    R = [set(r) for r in A[key]['res']]; N = len(R)
    cuts = [N - 300, N - 200, N - 100]       # 3 mốc, mỗi mốc chấm 100 kỳ sau
    def score(s, a, b): h = [len(R[t] & set(s)) for t in range(a, b)]; return sum(h) / len(h), sum(x >= 3 for x in h)
    rnd = []
    for _ in range(3000):
        s = random.sample(range(1, NB + 1), 6); rnd.append([score(s, c, c + 100) for c in cuts])
    m = sum(sum(x[0] for x in r) for r in rnd) / (3000 * 3); g3 = sum(sum(x[1] for x in r) for r in rnd) / 3000
    print(f'\n## {g} — chọn bộ ở mốc, chấm 100 kỳ sau mốc, 3 mốc (300 kỳ gần). Chọn bừa: TB {m:.2f} số/kỳ, ≥3 số {g3:.1f} lần/300 kỳ\n')
    print('| Cách chọn bộ cố định | 3 mốc: TB số trúng | ≥3 số (300 kỳ) | Hơn % bộ chọn bừa | Bộ hiện tại (theo toàn bộ dữ liệu) |\n|---|---|---|---|---|')
    for nm, f in RULES.items():
        sc = [score(f(R[:c], NB), c, c + 100) for c in cuts]; tot3 = sum(x[1] for x in sc); mm = sum(x[0] for x in sc) / 3
        pct = sum(sum(x[0] for x in r) / 3 < mm for r in rnd) / 3000 * 100
        now = sorted(f(R, NB))
        print(f'| {nm} | ' + ' · '.join(f'{x[0]:.2f}' for x in sc) + f' | {tot3} | {pct:.0f}% | {" ".join(f"{x:02d}" for x in now)} |')
