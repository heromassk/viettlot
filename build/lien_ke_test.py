#!/usr/bin/env python3
"""Dấu vết ±1 kỳ trước (anh 18/10/2026): số n ra kỳ trước → n-1, n+1 (không nằm trong kỳ trước) có ra kỳ sau không. 100 kỳ gần nhất."""
import csv
NB = dict(mega=45, power=55, loto=35); N = dict(mega=6, power=6, loto=5)
for g, f in (('loto', 'loto535'), ('mega', 'mega645'), ('power', 'power655')):
    R = [set(map(int, r[1:1 + N[g]])) for r in csv.reader(open(f'{f}_history.csv'))][::-1]
    MM = [int(r[6]) for r in csv.reader(open(f'{f}_history.csv'))][::-1] if g == 'loto' else None
    T = len(R); print(f'## {g}')
    for W in (10, 20, 50, 100):
        cnt = []; nh = nn = oh = on = 0
        for t in range(T - W, T):
            P = R[t - 1]; S = {x for n in P for x in (n - 1, n + 1) if 1 <= x <= NB[g]} - P
            h = len(S & R[t]); cnt.append(h); nh += h; nn += len(S); oh += len(R[t] - S - P); on += NB[g] - len(S) - len(P)
        d = {k: cnt.count(k) for k in range(max(cnt) + 1)}
        print(f'{W} kỳ: số kề ra TB {sum(cnt)/W:.2f}/kỳ · mỗi số kề ra {nh*100/nn:.1f}% · các số khác {oh*100/on:.1f}% · kỳ có ≥1: {sum(c>=1 for c in cnt)*100//W}% ≥2: {sum(c>=2 for c in cnt)*100//W}% · phân bố {d}')
