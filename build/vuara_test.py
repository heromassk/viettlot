#!/usr/bin/env python3
"""Trừ điểm SỐ VỪA RA kỳ trước trong pool (anh 15/10/2026: Power vé có 50 — vừa ra, 200 kỳ sau khi ra chỉ ra lại 1/16).
Ghép "Số ra kỳ trước" −0,5 … −4 vào bộ cộng điểm đang dùng của từng cỡ pool; áp khi ≥3 · ≥4 số ở 50 & 100 kỳ không giảm và có tăng.
  python build/vuara_test.py power|mega|loto  [--save: ghi vào pool_chon.json bộ của cỡ tăng]"""
import io, json, os, sys, contextlib
B = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, B)
GAME = sys.argv[1]; SAVE = '--save' in sys.argv
CAN = os.environ.get('CAN', 'Số ra kỳ trước')
src = open(os.path.join(B, 'pool_chon.py'), encoding='utf-8').read(); src = src[:src.index('CHON = {}; STAT = {}')]
sys.argv = ['pool_chon.py', GAME]; G = {'__file__': os.path.join(B, 'pool_chon.py'), '__name__': 'x'}
with contextlib.redirect_stdout(io.StringIO()): exec(compile(src, 'pool_chon.py', 'exec'), G)
import pool_app as PA
GY, TS, R, T, NUMS, SIG, DS = G['GY'], G['TS'], G['R'], G['T'], G['NUMS'], G['SIG'], G['DS']
C, theo = PA.chon(GAME); KC = PA.kepcap(GAME)
def stat(K, items):
    CC = dict(C); CC[str(K)] = items
    P = {t: PA.make(GY, R, t, SIG[t][0], SIG[t][1], NUMS[t], GAME, C=CC, KC=KC)[K] for t in TS}
    return {W: (sum(len(set(P[t]) & R[t]) >= 3 for t in range(T - W, T)), sum(len(set(P[t]) & R[t]) >= 4 for t in range(T - W, T))) for W in (50, 100)}
f = lambda s: f"{s[50][0]}·{s[50][1]} / {s[100][0]}·{s[100][1]}"
print(f'## {GAME} — trừ điểm "{CAN}" (−20 = loại hẳn), đến {DS[-1]} (ô: số kỳ ≥3 · ≥4 số ở 50 / 100 kỳ)\n\n| Pool | Đang dùng | Tốt nhất | Kết quả | Áp |\n|---|---|---|---|---|')
PCJ = json.load(open(os.path.join(B, 'pool_chon.json'), encoding='utf-8')); key = {}
for K in PA.KS:
    cur = C.get(str(K), []); b = stat(K, cur); best = None
    if any(nm == CAN for nm, _ in cur): print(f'| {K} | {f(b)} | đã có | | |'); continue
    for w in (2.0, 1.0, 0.5, -0.5, -1.0, -2.0, -3.0, -4.0, -20.0):
        s = stat(K, cur + [[CAN, w]])
        if any(s[W][j] < b[W][j] for W in (50, 100) for j in (0, 1)): continue
        g = (sum(s[W][1] - b[W][1] for W in (50, 100)), sum(s[W][0] - b[W][0] for W in (50, 100)))
        if g > (0, 0) and (best is None or g > best[0]): best = (g, w, s)
    print(f"| {K} | {f(b)} | {(CAN + ' ' + format(best[1], '+g')) if best else '—'} | {f(best[2]) if best else 'không tăng'} | {'có' if best else 'không'} |")
    if best and SAVE:
        sel = 'chon50' if theo.get(str(K)) == '50 kỳ' else 'chon'
        PCJ[GAME][sel][str(K)] = cur + [[CAN, best[1]]]
if SAVE: json.dump(PCJ, open(os.path.join(B, 'pool_chon.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1); print('\nĐã ghi pool_chon.json')
