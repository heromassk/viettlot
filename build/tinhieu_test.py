#!/usr/bin/env python3
"""Thử tín hiệu pool mới từ tra cứu 15 ngôn ngữ (anh 17/10/2026). Luật cố định, chỉ dùng 100 kỳ trước kỳ t:
  P. "cặp hay đi cùng": mỗi số vừa ra kỳ trước → bạn cùng kỳ nhiều nhất của nó (100 kỳ) được +1
  Q. "cặp cùng vắng": cặp đã ra cùng ≥3 lần trong 100 kỳ mà cả hai đang vắng ≥10 kỳ → cả hai −1
  M. "đối xứng": số (NB+1−n) của các số kỳ trước được +1
  G. "cách nửa dải": số n ± ⌊NB/2⌋ của các số kỳ trước được +1
So với pool hiện tại: kỳ trúng ≥3 · ≥4 số ở khung 10 / 50 / 100 kỳ.   python build/tinhieu_test.py mega"""
import io, os, sys, contextlib
from collections import Counter
B = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, B)
GAME = sys.argv[1]
os.environ['HOLD'] = '1'
src = open(os.path.join(B, 'pool_chon.py'), encoding='utf-8').read(); src = src[:src.index('CHON = {}; STAT = {}')]
sys.argv = ['pool_chon.py', GAME]; G = {'__file__': os.path.join(B, 'pool_chon.py'), '__name__': 'x'}
with contextlib.redirect_stdout(io.StringIO()): exec(compile(src, 'pool_chon.py', 'exec'), G)
import pool_app as PA
GY, R, T, NUMS, SIG, DS = G['GY'], G['R'], G['T'], G['NUMS'], G['SIG'], G['DS']
NB = GY['NB']; C, _ = PA.chon(GAME); KC = PA.kepcap(GAME); R = [set(r) for r in R]
TT = list(range(T - 100, T))

def extra(mode, t):
    e = {}; last = R[t - 1]
    if mode == 'P':
        co = Counter((a, b) for u in range(t - 100, t) for a in R[u] for b in R[u] if a != b)
        for n in last:
            best = max((m for m in range(1, NB + 1) if m != n), key=lambda m: (co[(n, m)], -m))
            if co[(n, best)] >= 3: e[best] = e.get(best, 0) + 1
    if mode == 'Q':
        co = Counter((a, b) for u in range(t - 100, t) for a in R[u] for b in R[u] if a < b)
        gap = {}
        for n in range(1, NB + 1):
            g = 0
            while g < t and n not in R[t - 1 - g]: g += 1
            gap[n] = g
        for (a, b), c in co.items():
            if c >= 3 and gap[a] >= 10 and gap[b] >= 10: e[a] = -1; e[b] = -1
    if mode == 'M':
        for n in last:
            m = NB + 1 - n
            if m not in last: e[m] = e.get(m, 0) + 1
    if mode == 'G':
        h = NB // 2
        for n in last:
            for m in (n - h, n + h):
                if 1 <= m <= NB and m not in last: e[m] = e.get(m, 0) + 1
    return e

def run(mode):
    out = {}
    for t in TT:
        f, s = SIG[t]
        out[t] = PA.make(GY, R, t, f, s, NUMS[t], GAME, extra0=(extra(mode, t) if mode != 'goc' else {}), C=C, KC=KC)
    return out

def st(P, K):
    return [(sum(len(set(P[t][K]) & R[t]) >= 3 for t in TT[-W:]), sum(len(set(P[t][K]) & R[t]) >= 4 for t in TT[-W:])) for W in (10, 50, 100)]

modes = [('goc', 'Pool hiện tại'), ('P', 'P. bạn đi cùng của số vừa ra +1'), ('Q', 'Q. cặp cùng vắng −1'), ('M', 'M. số đối xứng +1'), ('G', 'G. cách nửa dải +1')]
P = {k: run(k) for k, _ in modes}
KS = [K for K in PA.ks_of(GAME) if K <= 25]
print(f'## {GAME} — tín hiệu pool mới, 100 kỳ đến {DS[-1]} (ô: kỳ ≥3 · ≥4 số ở 10 / 50 / 100 kỳ)\n')
print('| Cách | ' + ' | '.join(f'Pool {K}' for K in KS) + ' |\n|---|' + '---|' * len(KS))
base = {K: st(P['goc'], K) for K in KS}
for k, lab in modes:
    cells = []
    for K in KS:
        s = st(P[k], K); b = base[K]
        mk = '' if k == 'goc' else (' ↑' if all(x[0] >= y[0] and x[1] >= y[1] for x, y in zip(s, b)) and s != b else (' ↓' if any(x[0] < y[0] or x[1] < y[1] for x, y in zip(s, b)) else ''))
        cells.append(' / '.join(f'{a}·{c}' for a, c in s) + mk)
    print(f'| {lab} | ' + ' | '.join(cells) + ' |')
