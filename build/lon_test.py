#!/usr/bin/env python3
"""Số LỘN (anh 15/10/2026: "các số lộn trong 1 kỳ hay lộn kỳ trước không có à"). lộn(ab) = ba (01↔10, 12↔21, 13↔31…), bỏ số kép.
A. Cặp lộn TRONG một kỳ: % kỳ có, theo kỳ trước có / không (50 / 100 / 200 kỳ).
B. Cộng / trừ điểm cho pool: "Lộn kỳ trước" (Loto thêm "Lộn kỳ cùng giờ trước") ghép vào bộ cộng điểm đang dùng của từng cỡ pool,
   ±0,5 / ±1 → ≥3 · ≥4 số ở 50 & 100 kỳ có tăng không (không khung nào giảm). Riêng từng game.
  python build/lon_test.py loto|mega|power"""
import io, os, sys, contextlib
B = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, B)
GAME = sys.argv[1]
src = open(os.path.join(B, 'pool_chon.py'), encoding='utf-8').read(); src = src[:src.index('CHON = {}; STAT = {}')]
sys.argv = ['pool_chon.py', GAME]; G = {'__file__': os.path.join(B, 'pool_chon.py'), '__name__': 'x'}
with contextlib.redirect_stdout(io.StringIO()): exec(compile(src, 'pool_chon.py', 'exec'), G)
import pool_app as PA
GY, TS, R, T, NB, NUMS, SIG, DS = G['GY'], G['TS'], G['R'], G['T'], G['NB'], G['NUMS'], G['SIG'], G['DS']
lon = lambda n: (n % 10) * 10 + n // 10
LON = lambda xs: {lon(n) for n in xs if lon(n) != n and 1 <= lon(n) <= NB}
SES = ['13' if '13h' in d else '21' for d in DS] if GAME == 'loto' else None
cap = lambda t: any(lon(n) in R[t] and lon(n) != n for n in R[t])
print(f'## {GAME} — số lộn, đến {DS[-1]}\n\n### A. Cặp lộn trong cùng một kỳ (% kỳ có · 50 / 100 / 200 kỳ)\n')
print('| Điều kiện | Kỳ có cặp lộn | Số lần (200) |\n|---|---|---|')
for lab, c in (('mọi kỳ', lambda t: True), ('kỳ trước có cặp lộn', lambda t: cap(t - 1)), ('kỳ trước không', lambda t: not cap(t - 1)),
               ('2 kỳ trước liền có', lambda t: cap(t - 1) and cap(t - 2)), ('2 kỳ trước liền không', lambda t: not cap(t - 1) and not cap(t - 2))):
    o = []; n2 = 0
    for W in (50, 100, 200):
        ts = [t for t in range(T - W, T) if c(t)]; n2 = len(ts); o.append(f'{sum(cap(t) for t in ts) * 100 // len(ts)}%' if ts else '—')
    print(f'| {lab} | {" / ".join(o)} | {n2} |')
print(f'\nKỳ gần nhất {DS[-1]}: {"có" if cap(T - 1) else "không có"} cặp lộn · kỳ trước nữa: {"có" if cap(T - 2) else "không"}\n')
# B. pool
def prev_ses(t):
    u = t - 1
    while u >= 0 and SES[u] != SES[t]: u -= 1
    return u
for t in TS:
    NUMS[t]['Lộn kỳ trước'] = LON(R[t - 1])
    if SES: NUMS[t]['Lộn kỳ cùng giờ trước'] = LON(R[prev_ses(t)])
print('### Số lộn kỳ trước tự nó ra bao nhiêu (50 / 100 kỳ): ' + ' · '.join(
    f"{nm}: {sum(len(NUMS[t][nm] & R[t]) for t in range(T - W, T))}/{sum(len(NUMS[t][nm]) for t in range(T - W, T))} số ra ({W} kỳ)"
    for nm in (['Lộn kỳ trước'] + (['Lộn kỳ cùng giờ trước'] if SES else [])) for W in (50, 100)) + '\n')
C, _ = PA.chon(GAME); KC = PA.kepcap(GAME)
def stat(CC):
    P = {t: PA.make(GY, R, t, SIG[t][0], SIG[t][1], NUMS[t], GAME, C=CC, KC=KC) for t in TS}
    return {K: {W: (sum(len(set(P[t][K]) & R[t]) >= 3 for t in range(T - W, T)), sum(len(set(P[t][K]) & R[t]) >= 4 for t in range(T - W, T))) for W in (50, 100)} for K in PA.KS}
base = stat(C)
print('### B. Cộng / trừ điểm "số lộn" vào pool (ô: số kỳ ≥3 · ≥4 số ở 50 / 100 kỳ)\n')
print('| Pool | Đang dùng | Thử tốt nhất | Kết quả | Áp? |\n|---|---|---|---|---|')
f = lambda s: f"{s[50][0]}·{s[50][1]} / {s[100][0]}·{s[100][1]}"
for K in PA.KS:
    best = None
    for nm in ['Lộn kỳ trước'] + (['Lộn kỳ cùng giờ trước'] if SES else []):
        for w in (1.0, 0.5, -0.5, -1.0):
            CC = {k: list(v) for k, v in C.items()}; CC[str(K)] = CC.get(str(K), []) + [[nm, w]]
            st = stat({str(K): CC[str(K)]} | {k: v for k, v in C.items() if k != str(K)})[K]
            if any(st[W][j] < base[K][W][j] for W in (50, 100) for j in (0, 1)): continue
            g = (sum(st[W][1] - base[K][W][1] for W in (50, 100)), sum(st[W][0] - base[K][W][0] for W in (50, 100)))
            if g > (0, 0) and (best is None or g > best[0]): best = (g, nm, w, st)
    print(f"| {K} | {f(base[K])} | {(best[1] + f' {best[2]:+g}') if best else '—'} | {f(best[3]) if best else 'không tăng'} | {'tăng' if best else 'không'} |")
