#!/usr/bin/env python3
"""Dấu vết máy (Loto): khung 100 / 200 kỳ gần nhất, so với khung liền trước cùng cỡ. Chạy tiến.
  python3 build/dauvet_may.py"""
import json, os, datetime
D = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'all_data.json')))['loto535']
R = [set(r) for r in D['res']]; S = [sorted(r) for r in D['res']]; T = len(R); NB, KB = 35, 5; P = KB / NB * 100
ses = ['13' if '13h' in x else '21' for x in D['dates']]
wd = [datetime.datetime.strptime(x[:10], '%d/%m/%Y').weekday() for x in D['dates']]
def rate(sets_fn, a, b):
    h = n = 0
    for t in range(a, b):
        g = sets_fn(t); h += len(g & R[t]); n += len(g)
    return h / max(n, 1) * 100
for W in (100, 200):
    A, B = (T - W, T), (T - 2 * W, T - W)
    print(f'\n## Khung {W} kỳ gần (so với {W} kỳ trước đó). Bình quân mỗi số {P:.1f}%\n')
    # 1. lặp theo độ trễ
    rows = []
    for lag in range(1, 15):
        r1 = rate(lambda t: R[t - lag], *A); r0 = rate(lambda t: R[t - lag], *B); rows.append((lag, r1, r0))
    print('**1. Số của kỳ cách k kỳ ra lại (k=1 kỳ trước, 2 = cùng phiên hôm trước, 14 = cùng phiên tuần trước)**')
    print(' '.join(f'k{l}:{a:.0f}/{b:.0f}' for l, a, b in rows) + '  (gần/trước)')
    good = [(l, a, b) for l, a, b in rows if (a - P) * (b - P) > 0 and abs(a - P) >= 1.5 and abs(b - P) >= 1.0]
    print('→ cùng chiều ở cả 2 khung: ' + (', '.join(f"k={l} {'NHIỀU' if a > P else 'ÍT'} ({a:.1f}/{b:.1f}%)" for l, a, b in good) or 'không có'))
    # 2. số nóng/lạnh trong khung trước có giữ ở kỳ sau không
    def hotset(t, w, top=True, n=8):
        c = {x: sum(x in R[u] for u in range(t - w, t)) for x in range(1, NB + 1)}
        return set(sorted(c, key=lambda x: ((-c[x]) if top else c[x], x))[:n])
    for w in (W // 2, W):
        h1, h0 = rate(lambda t: hotset(t, w), *A), rate(lambda t: hotset(t, w), *B)
        c1, c0 = rate(lambda t: hotset(t, w, False), *A), rate(lambda t: hotset(t, w, False), *B)
        print(f'**2. 8 số ra nhiều nhất {w} kỳ trước đó** → kỳ kế ra {h1:.1f}% / {h0:.1f}% · **8 số ra ít nhất** → {c1:.1f}% / {c0:.1f}%')
    # 3. vị trí: giá trị u..y so với kỳ trước cùng vị trí (cùng phía so với trung vị?)
    out = []
    for p in range(KB):
        for a, b in (A, B):
            med = sorted(S[u][p] for u in range(a - 200, a))[100]
            same = sum((S[t][p] > med) == (S[t - 1][p] > med) for t in range(a, b)) / (b - a) * 100
            out.append(same)
    print('**3. Vị trí u..y cùng phía trung vị với kỳ trước (50% = không dính)**: ' + ' · '.join(f"{'uvwxy'[p]} {out[2 * p]:.0f}/{out[2 * p + 1]:.0f}%" for p in range(KB)))
    # 4. phiên × thứ: tần suất từng số theo (phiên, thứ) có lặp lại sang khung sau?
    def prof(a, b, key):
        c = {}
        for t in range(a, b):
            k = key(t); c.setdefault(k, [0] * (NB + 1))
            for x in R[t]: c[k][x] += 1
        return c
    import math
    def corr(x, y):
        mx, my = sum(x) / len(x), sum(y) / len(y); n = sum((a - mx) * (b - my) for a, b in zip(x, y)); q = math.sqrt(sum((a - mx) ** 2 for a in x) * sum((b - my) ** 2 for b in y)); return n / q if q else 0
    for lab, key in (('phiên', lambda t: ses[t]), ('phiên×thứ', lambda t: (ses[t], wd[t]))):
        p1, p0 = prof(*A, key), prof(*B, key)
        cs = [corr(p1[k][1:], p0[k][1:]) for k in p1 if k in p0]
        print(f'**4. Tính cách theo {lab}** (tần suất từng số khung này ↔ khung trước, cùng nhóm): TB corr {sum(cs) / len(cs):+.2f} ({len(cs)} nhóm; ~0 = không có tính cách)')
