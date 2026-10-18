#!/usr/bin/env python3
"""Thử dấu vết SỐ THÁNG cho pool (anh 17/10/2026: "bên loto ngày tháng đang mạnh"). Luật cố định, không dò tham số:
  A. cộng điểm cho số tháng (w = +1, và +0.5 để xem độ nhạy)
  B. số tháng KHÔNG bị luật "ra 3 lần trong 5 kỳ" (nong35) loại
  C. cả A (+1) và B
  D. ngày + tháng cộng +1
So với pool hiện tại: số kỳ pool trúng ≥3 / ≥4 số ở khung 10 / 50 / 100 kỳ, mỗi kỳ chỉ dùng dữ liệu trước nó.
  python build/thang_test.py loto"""
import io, os, sys, contextlib
B = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, B)
GAME = sys.argv[1]
os.environ['HOLD'] = '1'
src = open(os.path.join(B, 'pool_chon.py'), encoding='utf-8').read(); src = src[:src.index('CHON = {}; STAT = {}')]
sys.argv = ['pool_chon.py', GAME]; G = {'__file__': os.path.join(B, 'pool_chon.py'), '__name__': 'x'}
with contextlib.redirect_stdout(io.StringIO()): exec(compile(src, 'pool_chon.py', 'exec'), G)
import pool_app as PA
GY, R, T, NUMS, SIG, DS = G['GY'], G['R'], G['T'], G['NUMS'], G['SIG'], G['DS']
NB = GY['NB']; C, _ = PA.chon(GAME); KC = PA.kepcap(GAME)
TT = list(range(T - 100, T))
dm = lambda t: tuple(int(x) for x in DS[t][:10].split('/')[:2])   # (ngày, tháng) của kỳ t

def run(mode):
    out = {}
    for t in TT:
        f, s = SIG[t]; d, m = dm(t); e = {}
        if mode in ('A1', 'C') and 1 <= m <= NB: e[m] = 1.0
        if mode == 'A05' and 1 <= m <= NB: e[m] = 0.5
        if mode == 'D' and 1 <= d + m <= NB: e[d + m] = 1.0
        if mode == 'E' and 'nong35' in s: s = dict(s); s['nong35'] = set()
        if mode in ('B', 'C') and 'nong35' in s: s = dict(s); s['nong35'] = set(s['nong35']) - {m}
        out[t] = PA.make(GY, R, t, f, s, NUMS[t], GAME, extra0=e, C=C, KC=KC)
    return out

def st(P, K):
    r = []
    for W in (10, 50, 100):
        hs = [len(set(P[t][K]) & set(R[t])) for t in TT[-W:]]
        r.append((sum(h >= 3 for h in hs), sum(h >= 4 for h in hs)))
    return r

modes = [('goc', 'Pool hiện tại'), ('E', 'E. bỏ hẳn luật 3 lần/5 kỳ'),] if os.environ.get('ONLYE') else [('goc', 'Pool hiện tại'), ('A1', 'A. số tháng +1'), ('A05', 'A. số tháng +0.5'), ('B', 'B. số tháng không bị loại "3 lần/5 kỳ"'),
         ('C', 'C. A(+1) + B'), ('D', 'D. ngày+tháng +1')]
P = {k: run(k) for k, _ in modes}
print(f'## {GAME} — dấu vết số tháng, 100 kỳ đến {DS[-1]} (ô: kỳ ≥3 · ≥4 số ở 10 / 50 / 100 kỳ)\n')
print('| Cách | ' + ' | '.join(f'Pool {K}' for K in PA.ks_of(GAME)) + ' |\n|---|' + '---|' * len(PA.ks_of(GAME)))
for k, lab in modes:
    print(f'| {lab} | ' + ' | '.join(' / '.join(f'{a}·{b}' for a, b in st(P[k], K)) for K in PA.ks_of(GAME)) + ' |')
