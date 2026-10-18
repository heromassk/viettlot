#!/usr/bin/env python3
"""Trong MỘT hàng, số nào ra? (anh 15/10/2026: "cứ đứng đầu hàng là được chọn à, phải xem tín hiệu").
Mỗi kỳ t (200 kỳ gần), mỗi hàng h có ≥1 số ra: mỗi cách (trong loai_dan.py) xếp các số của hàng; chấm số đứng đầu có ra không (top1)
và 2 số đầu có ≥1 ra (top2). So các cách với nhau (không so ngẫu nhiên). Riêng từng game.
  python build/hang_trong.py loto|mega|power"""
import os, sys
B = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, B)
GAME = sys.argv[1]
src = open(os.path.join(B, 'loai_dan.py'), encoding='utf-8').read(); src = src[:src.index('STAGES = []')]
sys.argv = ['loai_dan.py', GAME]; G = {'__file__': os.path.join(B, 'loai_dan.py'), '__name__': 'x'}
exec(compile(src, 'loai_dan.py', 'exec'), G)
R, T, TS, NB, M, CACHE = G['R'], G['T'], G['TS'], G['NB'], G['M'], G['CACHE']
PH = os.environ.get('PHIEN')   # '21' hoặc '13': chỉ chấm các kỳ cùng phiên (Loto)
if PH: TS = [t for t in TS if G['SES'][t] == PH]
C100 = G['C100']
H = NB // 10 + 1
print(f'## {GAME} — chọn số TRONG hàng, 200 kỳ gần đến {G["DATES"][-1]} (chỉ tính kỳ hàng đó có ≥1 số ra)\n')
for h in range(H):
    nums = [n for n in range(max(h * 10, 1), min(h * 10 + 9, NB) + 1)]
    ts = [t for t in TS if any(n in R[t] for n in nums)]
    if len(ts) < (15 if PH else 30): continue
    rows = []
    for nm in M:
        r = []
        for W in (50, 100, 200):
            tt = [t for t in ts if t >= T - W]
            if not tt: r.append((0, 0, 0)); continue
            t1 = t2 = 0
            for t in tt:
                o = sorted(nums, key=lambda n: (-CACHE[nm][t][n], -C100[t][n], n))
                t1 += o[0] in R[t]; t2 += bool(set(o[:2]) & R[t])
            r.append((t1 / len(tt) * 100, t2 / len(tt) * 100, len(tt)))
        blk = []
        for b in range(4):
            tb = [t for t in ts if T - 200 + b * 50 <= t < T - 200 + (b + 1) * 50]
            if not tb: continue
            c = 0
            for t in tb:
                o = sorted(nums, key=lambda n: (-CACHE[nm][t][n], -C100[t][n], n)); c += o[0] in R[t]
            blk.append(c / len(tb) * 100)
        rows.append((nm, r, min(blk) if blk else 0))
    rows.sort(key=lambda x: -(x[1][0][0] + x[1][1][0] + x[1][2][0]))
    print(f'### Hàng {h}x ({nums[0]:02d}–{nums[-1]:02d}) — {len(ts)} kỳ có số ra\n')
    print('| # | Cách chọn số đứng đầu hàng | Top1 ra 50 / 100 / 200 kỳ | Top2 ≥1 ra 50 / 100 / 200 | Khối 50 kỳ thấp nhất |\n|---|---|---|---|---|')
    for i, (nm, r, mn) in enumerate(rows[:6], 1):
        print(f"| {i} | {nm} | {' / '.join(f'{x[0]:.0f}%' for x in r)} | {' / '.join(f'{x[1]:.0f}%' for x in r)} | {mn:.0f}% |")
    print()
