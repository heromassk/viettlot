#!/usr/bin/env python3
"""Rải vé bao phủ trên pool (kiểu bảng Đại học Manchester 2023 — vé rải sao cho chắc chắn trúng khi đủ số về nằm trong pool).
  python build/rai_ve.py power|mega|loto [--pool 10,12,15,18]
Mỗi mức đảm bảo "m nếu k": nếu ≥k số về nằm trong pool thì CHẮC CHẮN có ≥1 vé trúng ≥m số.
Dựng bằng tham lam (greedy): số vé gần mức ít nhất, chưa phải tối ưu tuyệt đối.
Chạy tiến 100 / 200 kỳ gần với pool app đang dùng (goiy.py, chưa cộng tâm linh): % kỳ trúng, tiền vé, tiền thưởng."""
import argparse, json, os, sys
B = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, B)
ap = argparse.ArgumentParser(); ap.add_argument('game', choices=('power', 'mega', 'loto'))
ap.add_argument('--pool', default='10,12,15,18'); A = ap.parse_args(); GAME = A.game
_src = open(os.path.join(B, 'goiy.py'), encoding='utf-8').read(); _argv = sys.argv; sys.argv = ['goiy.py', GAME]
GY = {'__file__': os.path.join(B, 'goiy.py'), '__name__': 'goiy_head'}
exec(compile(_src[:_src.index('# ---------- Đà tổng')], 'goiy.py', 'exec'), GY); sys.argv = _argv; GY['CUR'] = None
R, T, KB = GY['R'], GY['T'], GY['KB']
GIA = 10000
# giải cố định (jackpot tính mức tối thiểu); Loto 5/35 chưa có bảng giải trong app → chỉ báo % trúng
THUONG = {'power': {3: 50000, 4: 500000, 5: 40e6, 6: 30e9}, 'mega': {3: 30000, 4: 300000, 5: 10e6, 6: 12e9}}.get(GAME)
MUC = [(2, 2), (3, 3), (3, 4), (4, 4)] if KB == 5 else [(3, 3), (3, 4), (4, 4), (4, 5)]   # (m, k): trúng ≥m nếu ≥k số về trong pool

from bao_phu import bao_phu as _bp
def bao_phu(v, m, k): return _bp(v, KB, m, k)

POOLS = [int(x) for x in A.pool.split(',')]
RK = {t: GY['pool_of'](GY['score'](*GY['signals'](t)), GY['signals'](t)[1], max(POOLS)) for t in range(T - 200, T)}
print(f'## Rải vé bao phủ trên pool app đang dùng — {GAME}, chạy tiến 100 / 200 kỳ gần (đến {GY["D"]["dates"][-1]})\n')
print('"m nếu k" = nếu ≥k số về nằm trong pool thì chắc chắn có vé trúng ≥m số. Tiền: vé 10.000đ' + (', giải 3 số ' + f"{THUONG[3]:,.0f}đ, 4 số {THUONG[4]:,.0f}đ, 5 số {THUONG[5]:,.0f}đ".replace(',', '.') if THUONG else ' (Loto: chưa tính tiền)') + '.\n')
print('| Pool | Mức đảm bảo | Số vé | Tiền vé/kỳ | Kỳ đủ điều kiện (100 / 200) | Kỳ có vé ≥3 số (100 / 200) | Kỳ có vé ≥4 số (100 / 200) | Kỳ có vé ≥5 số (200) |' + (' Thưởng TB/kỳ (200) | Lãi/lỗ TB/kỳ |' if THUONG else ''))
print('|---|---|---|---|---|---|---|---|' + ('---|---|' if THUONG else ''))
for v in POOLS:
    for m, k in MUC:
        if k > KB or m > k: continue
        tk = bao_phu(v, m, k)
        st = {}
        for w, ts in (('100', range(T - 100, T)), ('200', range(T - 200, T))):
            dk = g3 = g4 = g5 = 0; tien = 0.0
            for t in ts:
                pool = RK[t][:v]; ve = [{pool[i] for i in b} for b in tk]
                h = len(set(pool) & R[t]); best = max(len(x & R[t]) for x in ve)
                dk += h >= k; g3 += best >= 3; g4 += best >= 4; g5 += best >= 5
                if THUONG: tien += sum(THUONG.get(len(x & R[t]), 0) for x in ve)
            n = len(ts); st[w] = (dk / n * 100, g3 / n * 100, g4 / n * 100, g5 / n * 100, tien / n)
        a, b = st['100'], st['200']; chi = len(tk) * GIA
        row = f'| {v} | {m} nếu {k} | {len(tk)} | {chi:,.0f}đ'.replace(',', '.') + f' | {a[0]:.0f}% / {b[0]:.0f}% | {a[1]:.0f}% / {b[1]:.0f}% | {a[2]:.0f}% / {b[2]:.0f}% | {b[3]:.1f}% |'
        if THUONG: row += f' {b[4]:,.0f}đ | {b[4] - chi:+,.0f}đ |'.replace(',', '.')
        print(row)
