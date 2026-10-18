#!/usr/bin/env python3
"""Bảng chuyển theo HÀNG (anh 14/10/2026): kỳ trước hàng X ra c số → kỳ này hàng X ra mấy số (% kỳ), khung 50 / 100 / 200 kỳ.
Đánh dấu dấu vết: kết quả hay gặp nhất sau trạng thái đó và nó ổn định cả 3 khung. Kèm bảng theo 2 kỳ trước.
  python build/hang_chuyen.py power|mega|loto"""
import json, os, sys
from collections import Counter
B = os.path.dirname(os.path.abspath(__file__))
GAME = sys.argv[1]
key, NB, KB = {'power': ('power655', 55, 6), 'mega': ('mega645', 45, 6), 'loto': ('loto535', 35, 5)}[GAME]
D = json.load(open(os.path.join(B, 'all_data.json'), encoding='utf-8'))[key]
R = [sorted(r) for r in D['res']]; DT = D['dates']; T = len(R)
H = list(range(NB // 10 + 1))
C = [tuple(min(sum(1 for n in r if n // 10 == h), 3) for h in H) for r in R]
LB = {0: '0', 1: '1', 2: '2', 3: '≥3'}
WS = (50, 100, 200)
print(f'## {GAME} — kỳ trước hàng ra c số → kỳ này ra mấy số, đến {DT[-1]}\n')
print('Mỗi ô: % kỳ (khung 50 / 100 / 200 kỳ). ★ = kết quả hay gặp nhất sau trạng thái đó ở cả 3 khung và ≥50% ở cả 3 khung.\n')
STAR = []
for i, h in enumerate(H):
    print(f'### Hàng {h}x — kỳ trước hiện tại ra {LB[C[-1][i]]} số\n')
    print('| Kỳ trước ra | Số lần (200) | Kỳ này 0 số | 1 số | 2 số | ≥3 số |\n|---|---|---|---|---|---|')
    for c in range(4):
        cols = {k: [] for k in range(4)}; ns = []
        for W in WS:
            ts = [t for t in range(T - W, T) if C[t - 1][i] == c]; ns.append(len(ts)); cc = Counter(C[t][i] for t in ts)
            for k in range(4): cols[k].append(cc.get(k, 0) / len(ts) * 100 if ts else None)
        if not ns[-1]: continue
        best = [max(range(4), key=lambda k: cols[k][j] or 0) for j in range(3)]
        star = len(set(best)) == 1 and all((cols[best[0]][j] or 0) >= 50 for j in range(3)) and ns[0] >= 5
        if star: STAR.append((h, c, best[0], cols[best[0]]))
        cell = lambda k: ' / '.join('—' if v is None else f'{v:.0f}' for v in cols[k]) + ('% ★' if star and k == best[0] else '%')
        mark = ' ← hiện tại' if C[-1][i] == c else ''
        print(f'| {LB[c]} số{mark} | {ns[-1]} | ' + ' | '.join(cell(k) for k in range(4)) + ' |')
    print()
# gộp: kỳ này ra ≤1 / ≥1
print('### Gộp gọn: sau trạng thái kỳ trước → kỳ này "≤1 số" / "≥1 số" (% kỳ, 50 / 100 / 200) — dấu vết ≥70% cả 3 khung\n')
print('| Hàng | Kỳ trước ra | ≤1 số | ≥1 số | Số lần (200) |\n|---|---|---|---|---|')
for i, h in enumerate(H):
    for c in range(4):
        r1, r2, n = [], [], 0
        for W in WS:
            ts = [t for t in range(T - W, T) if C[t - 1][i] == c]; n = len(ts)
            r1.append(sum(C[t][i] <= 1 for t in ts) / n * 100 if ts else None); r2.append(sum(C[t][i] >= 1 for t in ts) / n * 100 if ts else None)
        if n < 10: continue
        f = lambda r: ' / '.join('—' if v is None else f'{v:.0f}' for v in r) + ('% ✔' if all(v is not None and v >= 70 for v in r) else '%')
        print(f'| {h}x | {LB[c]} số{" ← hiện tại" if C[-1][i] == c else ""} | {f(r1)} | {f(r2)} | {n} |')
# 2 kỳ trước
print('\n### Theo 2 kỳ trước (kỳ t−2, kỳ t−1) → kỳ này: kết quả hay gặp nhất, chỉ liệt kê trạng thái có ≥15 lần trong 200 kỳ\n')
print('| Hàng | 2 kỳ trước | Số lần (200) | Hay gặp nhất kỳ này | % (50 / 100 / 200) |\n|---|---|---|---|---|')
for i, h in enumerate(H):
    for a in range(4):
        for b in range(4):
            ts200 = [t for t in range(T - 200, T) if C[t - 2][i] == a and C[t - 1][i] == b]
            if len(ts200) < 15: continue
            k = Counter(C[t][i] for t in ts200).most_common(1)[0][0]
            r = []
            for W in WS:
                ts = [t for t in range(T - W, T) if C[t - 2][i] == a and C[t - 1][i] == b]; r.append(sum(C[t][i] == k for t in ts) / len(ts) * 100 if ts else None)
            cur = ' ← hiện tại' if (C[-2][i], C[-1][i]) == (a, b) else ''
            print(f"| {h}x | {LB[a]} → {LB[b]}{cur} | {len(ts200)} | {LB[k]} số | {' / '.join('—' if v is None else f'{v:.0f}' for v in r)}% |")
print('\nDấu vết ★ (cùng kết quả hay gặp nhất ở cả 3 khung, ≥50%): ' + (' · '.join(f'{h}x ra {LB[c]} → kỳ sau {LB[k]} số ({" / ".join(f"{v:.0f}" for v in vs)}%)' for h, c, k, vs in STAR) or 'không có'))
