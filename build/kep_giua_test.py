#!/usr/bin/env python3
"""Dấu vết "kẹp giữa" (anh 18/10/2026): kỳ trước có 2 số cách nhau 2 (a, a+2) thì kỳ sau có a+1 không. 100 kỳ gần nhất, 5/6 số chính."""
import csv, sys
NB = dict(mega=45, power=55, loto=35); N = dict(mega=6, power=6, loto=5)
for g, f in (('mega', 'mega645'), ('power', 'power655'), ('loto', 'loto535')):
    R = [set(map(int, r[1:1 + N[g]])) for r in csv.reader(open(f'{f}_history.csv'))][::-1]   # cũ → mới
    T = len(R); ev = []
    for t in range(T - 100, T):
        P = R[t - 1]; mids = {a + 1 for a in P if a + 2 in P and a + 1 not in P}
        if mids:
            rest = set(range(1, NB[g] + 1)) - mids
            ev.append((len(mids), len(mids & R[t]), len(rest), len(rest & R[t]) - 0))
    print(f'## {g}')
    for W in (10, 50, 100):
        e = [x for x in ev[-1:] ] if False else None
    # theo khung kỳ: tính lại theo chỉ số kỳ
    for W in (10, 50, 100):
        sel = []
        for t in range(T - W, T):
            P = R[t - 1]; mids = {a + 1 for a in P if a + 2 in P and a + 1 not in P}
            if mids: sel.append((mids, R[t], R[t - 1]))
        if not sel: print(W, 'không có'); continue
        m = sum(len(s[0]) for s in sel); mh = sum(len(s[0] & s[1]) for s in sel)
        k1 = sum(bool(s[0] & s[1]) for s in sel)
        rn = sum(NB[g] - len(s[0]) for s in sel); rh = sum(len(s[1] - s[0]) for s in sel)
        print(f'{W} kỳ: {len(sel)} kỳ có kẹp · số giữa ra {mh}/{m} = {mh*100/m:.0f}% · ≥1 số giữa ra {k1}/{len(sel)} = {k1*100/len(sel):.0f}% · các số khác ra {rh*100/rn:.1f}%')
