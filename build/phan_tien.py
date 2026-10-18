#!/usr/bin/env python3
"""CHẤM TIẾN từng phần cố định của pool (anh 15/10/2026: "làm kĩ"): mỗi phần (luật ghim, giới hạn kép, Markov…) được quyết định BẬT/TẮT
cứ mỗi 10 kỳ chỉ bằng 100 kỳ trước đó (bật khi không giảm kỳ ≥3/≥4 số ở 10/50/100 kỳ và có tăng), rồi chấm 10 kỳ sau.
So: luôn bật · luôn tắt · bật/tắt theo quyết định từng khối. Riêng từng game.
  python build/phan_tien.py loto|mega|power"""
import io, os, sys, contextlib, json
B = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, B)
GAME = sys.argv[1]
os.environ['HOLD'] = '1'
src = open(os.path.join(B, 'pool_chon.py'), encoding='utf-8').read(); src = src[:src.index('CHON = {}; STAT = {}')]
sys.argv = ['pool_chon.py', GAME]; G = {'__file__': os.path.join(B, 'pool_chon.py'), '__name__': 'x'}
with contextlib.redirect_stdout(io.StringIO()): exec(compile(src, 'pool_chon.py', 'exec'), G)
import pool_app as PA
GY, TS, R, T, NUMS, SIG, DS = G['GY'], G['TS'], G['R'], G['T'], G['NUMS'], G['SIG'], G['DS']
C, _ = PA.chon(GAME); KC0 = PA.kepcap(GAME); WMK0 = GY.get('WMK', 0)
GH0, KN0, MX0 = dict(PA.GHIM), dict(PA.KHO_NONG), dict(PA.MIXK)

def pools(tat):
    """pool mọi cỡ ở mọi kỳ TS khi TẮT phần `tat`"""
    PA.GHIM, PA.KHO_NONG, PA.MIXK = dict(GH0), dict(KN0), dict(MX0); KC = dict(KC0); GY['WMK'] = WMK0
    if tat == 'ghim': PA.GHIM = {}
    if tat == 'khonong': PA.KHO_NONG = {}
    if tat == 'mixk': PA.MIXK = {}
    if tat == 'kep': KC = {}
    out = {}
    for t in TS:
        f, s = SIG[t]
        if tat == 'markov': s = dict(s); s.pop('_mix', None); GY['WMK'] = 0
        out[t] = PA.make(GY, R, t, f, s, NUMS[t], GAME, C=C, KC=KC)
    return out

PHAN = []
if PA.GHIM.get(GAME): PHAN.append(('ghim', 'Loại số nhịp riêng hay nghỉ', sorted(PA.GHIM[GAME])))
if PA.KHO_NONG.get(GAME): PHAN.append(('khonong', 'Không trừ "khó ra" khi số nóng lại', sorted(PA.KHO_NONG[GAME])))
if PA.MIXK.get(GAME): PHAN.append(('mixk', 'Markov riêng theo cỡ pool', sorted(PA.MIXK[GAME])))
if KC0: PHAN.append(('kep', 'Giới hạn số kép trong pool', sorted(int(k) for k in KC0)))
if SIG[TS[-1]][1].get('_mix') or WMK0: PHAN.append(('markov', 'Markov chung (trộn thứ hạng)', list(PA.KS)))
ON = pools(None)
print(f'## {GAME} — CHẤM TIẾN từng phần cố định của pool, 100 kỳ đến {DS[-1]} (quyết định bật/tắt mỗi 10 kỳ bằng 100 kỳ trước)\n')
print('Ô: số kỳ ≥3 · ≥4 số ở 10 / 50 / 100 kỳ\n')
KQ = {}
for key, lab, KS in PHAN:
    OFF = pools(key)
    print(f'### {lab} (cỡ {", ".join(map(str, KS))})\n\n| Pool | Luôn bật | Luôn tắt | Quyết định từng khối | Số khối bật |\n|---|---|---|---|---|')
    for K in KS:
        h = lambda P, t: len(set(P[t][K]) & R[t])
        def st(P, ts): hs = [h(P, t) for t in ts]; return (sum(x >= 3 for x in hs), sum(x >= 4 for x in hs))
        TT = list(range(T - 100, T)); POL = {}; nb = 0
        for b in range(T - 100, T, 10):
            ok = True; gain = False
            for W in (10, 50, 100):
                a, z = st(ON, range(b - W, b)), st(OFF, range(b - W, b))
                if a[0] < z[0] or a[1] < z[1]: ok = False
                if a[0] > z[0] or a[1] > z[1]: gain = True
            bat = ok and gain; nb += bat
            for t in range(b, b + 10): POL[t] = ON[t] if bat else OFF[t]
        f = lambda P: ' / '.join(f'{st(P, TT[-W:])[0]}·{st(P, TT[-W:])[1]}' for W in (10, 50, 100))
        print(f'| {K} | {f(ON)} | {f(OFF)} | {f(POL)} | {nb}/10 |')
        KQ[f'{key}_{K}'] = dict(on=[st(ON, TT[-W:]) for W in (10, 50, 100)], off=[st(OFF, TT[-W:]) for W in (10, 50, 100)], pol=[st(POL, TT[-W:]) for W in (10, 50, 100)], nb=nb)
    print()
P = os.path.join(B, f'phan_tien_{GAME}.json'); allc = {}   # mỗi game 1 file (chạy song song không ghi đè nhau)
allc[GAME] = dict(den=DS[-1], kq=KQ); json.dump(allc, open(P, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
