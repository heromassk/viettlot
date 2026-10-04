#!/usr/bin/env python3
"""Thử thêm suy luận: (1) tính cách theo THỨ quay (bộ bi/máy theo ngày?), (2) nhịp riêng từng số "đến hạn",
(3) cặp số hay đi cùng, (4) số ra cùng thứ tuần trước. Chấm qua 3 khúc, chạy tiến.
  python3 build/thu_them.py power|mega|loto"""
import json, os, sys, math, random, datetime
from itertools import combinations
G = {'power': ('power655', 55, 6), 'mega': ('mega645', 45, 6), 'loto': ('loto535', 35, 5)}
key, NB, KB = G[sys.argv[1]]
D = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'all_data.json')))[key]
R = [set(r) for r in D['res']]; T = len(R)
wd = [datetime.datetime.strptime(x[:10], '%d/%m/%Y').weekday() for x in D['dates']]
def corr(a, b):
    ma, mb = sum(a) / len(a), sum(b) / len(b); n = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    q = math.sqrt(sum((x - ma) ** 2 for x in a) * sum((y - mb) ** 2 for y in b)); return n / q if q else 0
fq = lambda ix: [sum(n in R[t] for t in ix) for n in range(1, NB + 1)]
S0 = max(100, T - 600); blocks = [(S0 + i * (T - S0) // 3, S0 + (i + 1) * (T - S0) // 3) for i in range(3)]
out = []
# (1) theo thứ: tần suất nửa đầu ↔ nửa sau cùng thứ, so với khác thứ
days = sorted(set(wd))
if len(days) > 1:
    rows = []
    for d in days:
        ix = [t for t in range(T) if wd[t] == d]; h = len(ix) // 2
        rows.append((d, len(ix), corr(fq(ix[:h]), fq(ix[h:]))))
    random.seed(1); base = []
    for _ in range(200):
        RR = [set(random.sample(range(1, NB + 1), KB)) for _ in range(len(rows and ix))]
        g = lambda a: [sum(n in RR[t] for t in a) for n in range(1, NB + 1)]; h = len(RR) // 2
        base.append(corr(g(range(h)), g(range(h, len(RR)))))
    base.sort()
    out.append('(1) Tính cách theo thứ (corr tần suất nửa đầu↔nửa sau, cùng thứ): ' + ', '.join(f"T{d + 2 if d < 6 else 'CN'}:{c:+.2f} ({n} kỳ)" for d, n, c in rows)
               + f' · mức thường gặp 95%: ±{base[int(.975 * len(base))]:.2f}')
    # walk-forward: pool 15 nóng cùng thứ 60 kỳ vs nóng mọi thứ 60 kỳ
    def wf(same):
        res = []
        for a, b in blocks:
            h = 0
            for t in range(a, b):
                ix = [u for u in range(t - 1, -1, -1) if (wd[u] == wd[t] if same else True)][:60]
                c = {n: sum(n in R[u] for u in ix) for n in range(1, NB + 1)}
                h += len(set(sorted(c, key=lambda n: (-c[n], n))[:15]) & R[t])
            res.append(h / (b - a))
        return res
    out.append('    Pool 15 nóng CÙNG THỨ 60 kỳ: ' + ' / '.join(f'{x:.2f}' for x in wf(True)) + '  ·  nóng MỌI THỨ 60 kỳ: ' + ' / '.join(f'{x:.2f}' for x in wf(False)) + ' (số trúng TB/kỳ, 3 khúc)')
# (2) đến hạn: gap hiện tại trong [0.8,1.3] × median gap riêng của số
def gaps_hist(t, n):
    gs, last = [], None
    for u in range(t):
        if n in R[u]:
            if last is not None: gs.append(u - last)
            last = u
    return gs, (t - 1 - last if last is not None else t)
res = []
for a, b in blocks:
    h1 = n1 = h0 = n0 = 0
    for t in range(a, b, 2):
        for n in range(1, NB + 1):
            gs, g = gaps_hist(t, n)
            if len(gs) < 10: continue
            md = sorted(gs)[len(gs) // 2]
            due = 0.8 * md <= g + 1 <= 1.3 * md
            hit = n in R[t]
            if due: h1 += hit; n1 += 1
            else: h0 += hit; n0 += 1
    res.append((h1 / n1 * 100, h0 / n0 * 100, n1 / ((b - a) / 2)))
out.append('(2) Số "đến hạn" (vắng ≈ nhịp riêng 0.8–1.3× trung vị): ra ' + ' / '.join(f'{x[0]:.1f}%' for x in res) + ' · số khác ' + ' / '.join(f'{x[1]:.1f}%' for x in res) + f' · ~{res[0][2]:.0f} số/kỳ')
# (3) cặp: số đếm cặp nửa đầu ↔ nửa sau
def pc(ix):
    c = {}
    for t in ix:
        for p in combinations(sorted(R[t]), 2): c[p] = c.get(p, 0) + 1
    return [c.get(p, 0) for p in combinations(range(1, NB + 1), 2)]
h = T // 2
out.append(f'(3) Cặp số hay đi cùng: corr nửa đầu↔nửa sau = {corr(pc(range(h)), pc(range(h, T))):+.3f}')
# (4) số cùng thứ tuần trước
if len(days) > 1:
    res = []
    for a, b in blocks:
        hh = nn = 0
        for t in range(a, b):
            u = next((u for u in range(t - 1, -1, -1) if wd[u] == wd[t]), None)
            if u is None: continue
            hh += len(R[u] & R[t]); nn += KB
        res.append(hh / nn * 100)
    out.append('(4) Số của kỳ CÙNG THỨ tuần trước ra lại: ' + ' / '.join(f'{x:.1f}%' for x in res) + f' mỗi số (mỗi số bình quân {KB / NB * 100:.1f}%)')
print('\n'.join(out))
