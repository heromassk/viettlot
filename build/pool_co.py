#!/usr/bin/env python3
"""Cần pool bao nhiêu số để chứa ≥5/6 (≥4/5 Loto) số trúng ở ≥70% kỳ? (anh 15/10/2026). Thứ hạng = cách app chấm (tín hiệu + bộ cộng
điểm của pool 25), số bị loại hẳn xếp cuối. Chạy tiến 100 kỳ, mỗi kỳ chỉ dùng dữ liệu trước nó. Riêng từng game.
  python build/pool_co.py power|mega|loto"""
import io, os, sys, contextlib
B = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, B)
GAME = sys.argv[1]
src = open(os.path.join(B, 'pool_chon.py'), encoding='utf-8').read(); src = src[:src.index('CHON = {}; STAT = {}')]
sys.argv = ['pool_chon.py', GAME]; G = {'__file__': os.path.join(B, 'pool_chon.py'), '__name__': 'x'}
with contextlib.redirect_stdout(io.StringIO()): exec(compile(src, 'pool_chon.py', 'exec'), G)
import pool_app as PA
GY, TS, R, T, NB, NUMS, SIG, DS = G['GY'], G['TS'], G['R'], G['T'], G['NB'], G['NUMS'], G['SIG'], G['DS']
KB = GY['KB']; C, _ = PA.chon(GAME)
def order(t, items):
    e = {}
    for nm, w in items:
        for n in NUMS[t].get(nm, ()): e[n] = e.get(n, 0) + w
    f, s = SIG[t]; sc = GY['score'](f, s, e); o = GY['pool_of'](sc, s, NB)
    return o + sorted((n for n in range(1, NB + 1) if n not in o), key=lambda n: -sc[n])
for lab, items in (('Thứ hạng app (bộ cộng điểm pool 25)', C.get('25', [])), ('Tín hiệu thô (không cộng)', [])):
    O = {t: order(t, items) for t in TS}
    nloai = sum(NB - len(GY['pool_of'](GY['score'](*SIG[t], {}), SIG[t][1], NB)) for t in TS) / len(TS)
    print(f'## {GAME} — {lab}, 100 kỳ đến {DS[-1]} (TB loại hẳn {nloai:.1f} số/kỳ, xếp cuối)\n')
    print(f'| Pool | ≥{KB - 1} số (50 / 100 kỳ) | đủ {KB} số (50 / 100 kỳ) |\n|---|---|---|')
    first = {}
    for K in range(15, NB + 1, 1 if NB <= 35 else 2):
        r = [sum(len(set(O[t][:K]) & R[t]) >= j for t in range(T - W, T)) * 100 // W for j in (KB - 1, KB) for W in (50, 100)]
        if K % 5 == 0 or K == NB or K >= NB - 20 or (r[0] >= 70 and r[1] >= 70 and 'a' not in first):
            print(f'| {K} | {r[0]}% / {r[1]}% | {r[2]}% / {r[3]}% |')
        if r[0] >= 70 and r[1] >= 70 and 'a' not in first: first['a'] = K
        if r[2] >= 70 and r[3] >= 70 and 'b' not in first: first['b'] = K
    print(f"\n→ ≥{KB - 1}/{KB} số ở ≥70% kỳ (cả 50 & 100 kỳ): pool **{first.get('a', '—')}** · đủ {KB}/{KB}: pool **{first.get('b', '—')}**\n")
