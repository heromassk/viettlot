#!/usr/bin/env python3
"""Bỏ dần từ cả dãy số, mục tiêu giữ ≥KB−1 số trúng (Power/Mega ≥5/6, Loto ≥4/5) ở ≥70% kỳ (anh 15/10/2026: "để đạt 5/6 trên 70% cần
pool bao nhiêu" → tìm luật bỏ thêm ở đuôi). Mỗi bước bỏ STEP số theo cách (loai_dan.py) giữ được nhiều kỳ ≥KB−1 nhất (khung 50 & 100 kỳ),
đi tiếp từ pool đó; dừng khi cả 50 và 100 kỳ không còn ≥70%. Chạy tiến, mỗi kỳ chỉ dùng dữ liệu trước nó. Riêng từng game.
  python build/bo_duoi.py power|mega|loto [STEP=2]"""
import io, os, sys, contextlib
B = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, B)
GAME = sys.argv[1]; STEPN = int(sys.argv[2]) if len(sys.argv) > 2 else 2
src = open(os.path.join(B, 'loai_dan.py'), encoding='utf-8').read(); src = src[:src.index('STAGES = []')]
sys.argv = ['loai_dan.py', GAME]; G = {'__file__': os.path.join(B, 'loai_dan.py'), '__name__': 'x'}
with contextlib.redirect_stdout(io.StringIO()): exec(compile(src, 'loai_dan.py', 'exec'), G)
R, T, TS, NB, KB, M, bo, N, DATES = G['R'], G['T'], G['TS'], G['NB'], G['KB'], G['M'], G['bo'], G['N'], G['DATES']
NEED = KB - 1
pct = lambda Q, W, j=NEED: sum(len(Q[t] & R[t]) >= j for t in range(T - W, T)) * 100 // W
P = {t: set(N) for t in TS}; size = NB; path = []
print(f'## {GAME} — bỏ dần {STEPN} số mỗi bước, giữ ≥{NEED}/{KB} số trúng, đến {DATES[-1]}\n')
print(f'| Pool | Cách bỏ ở bước này | ≥{NEED} số 50 / 100 / 200 kỳ | đủ {KB} số 50 / 100 kỳ |\n|---|---|---|---|')
while size - STEPN >= KB:
    best = None
    for nm in M:
        Q = {t: bo(P[t], nm, t, STEPN) for t in TS}
        a, b = pct(Q, 50), pct(Q, 100)
        key = (min(a, b), a + b, pct(Q, 200))
        if best is None or key > best[0]: best = (key, nm, Q)
    (mn, _, c200), nm, Q = best
    if mn < 70: print(f'\n→ Bỏ thêm {STEPN} số nữa (về {size - STEPN}) thì cách tốt nhất ({nm}) chỉ còn {pct(Q, 50)}% / {pct(Q, 100)}% → dừng.'); break
    P = Q; size -= STEPN
    print(f'| {size} | {nm} | {pct(P, 50)}% / {pct(P, 100)}% / {pct(P, 200)}% | {pct(P, 50, KB)}% / {pct(P, 100, KB)}% |')
print(f'\n**Pool nhỏ nhất giữ ≥{NEED}/{KB} ở ≥70% kỳ (cả 50 & 100 kỳ): {size} số.**')
