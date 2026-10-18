#!/usr/bin/env python3
"""Thử cộng / trừ điểm vào pool từng dấu vết (anh 14/10/2026): số theo thứ-ngày-tháng (dương + âm lịch),
số kỳ trước, liền kề ±1 kỳ trước, số kép, kép liền kề kép kỳ trước. Mỗi dấu vết thử RIÊNG (±1 điểm cho số nó chọn),
pool gốc = pool app đang dùng (có tâm linh đã duyệt). Chạy tiến 100 kỳ, chấm % kỳ ≥3 · ≥4 số khung 10/20/50/100.
  python build/kiemtra_app.py 200      # (khi dữ liệu đổi)
  python build/pool_ngay.py power|mega|loto"""
import json, os, sys, subprocess, datetime as dt
B = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, B)
GAME = sys.argv[1]
_src = open(os.path.join(B, 'goiy.py'), encoding='utf-8').read(); _argv = sys.argv; sys.argv = ['goiy.py', GAME]
GY = {'__file__': os.path.join(B, 'goiy.py'), '__name__': 'goiy_head'}
exec(compile(_src[:_src.index('# ---------- Đà tổng')], 'goiy.py', 'exec'), GY); sys.argv = _argv; GY['CUR'] = None
R, T, NB = GY['R'], GY['T'], GY['NB']
DS = GY['D']['dates']
TS = range(T - 100, T)
# âm lịch các ngày quay (lunar.js của app, 1 lần gọi node)
_days = sorted({d[:10] for d in DS[T - 101:]})
_js = open(os.path.join(B, 'lunar.js'), encoding='utf-8').read() + ';console.log(JSON.stringify(' + json.dumps(_days) + '.map(s=>{const [d,m,y]=s.split("/").map(Number);const L=solar2lunar(d,m,y);return [L.d,L.m];})));'
LUN = dict(zip(_days, json.loads(subprocess.run(['node', '-e', _js], capture_output=True, text=True, check=True).stdout)))
# tâm linh đã duyệt (như app) — từ kiemtra_app.json
APP = json.load(open(os.path.join(B, 'kiemtra_app.json'), encoding='utf-8'))[GAME]; T0 = T - len(APP['dates'])
TLDUNG = {'loto': ['Tử vi (Mệnh, Cục, sao Tử Vi)'], 'mega': ['Thần số học', 'Lộn + kép'], 'power': ['Tử vi (Mệnh, Cục, sao Tử Vi)']}[GAME]
def tl(t):
    e = {}
    for x in APP['kx']:
        if x['nm'] in TLDUNG:
            for n in (x['nums'][t - T0] or []):
                if 1 <= n <= NB: e[n] = e.get(n, 0) + 1.0
    return e
lon = lambda n: int(f'{n:02d}'[::-1])
def d_(t): return dt.datetime.strptime(DS[t][:10], '%d/%m/%Y')
def am(t): return LUN[DS[t][:10]]
K11 = set(range(11, NB + 1, 11))
SIGS = {
    'Ngày': lambda t: {d_(t).day},
    'Tháng': lambda t: {d_(t).month},
    'Ngày lộn': lambda t: {lon(d_(t).day)},
    'Ngày + tháng': lambda t: {d_(t).day + d_(t).month},
    'Ghép tháng–ngày': lambda t: {int(f'{d_(t).month % 10}{d_(t).day // 10}'), int(f'{d_(t).day % 10}{d_(t).month // 10}')},
    'Ngày ±1': lambda t: {d_(t).day - 1, d_(t).day + 1},
    'Thứ': lambda t: {d_(t).weekday() + 2},
    'Tổng chữ số ngày tháng năm': lambda t: {sum(int(c) for c in d_(t).strftime('%d%m%Y'))},
    'Ngày âm': lambda t: {am(t)[0]},
    'Tháng âm': lambda t: {am(t)[1]},
    'Ngày âm lộn': lambda t: {lon(am(t)[0])},
    'Ngày âm + tháng âm': lambda t: {am(t)[0] + am(t)[1]},
    'Ngày âm ±1': lambda t: {am(t)[0] - 1, am(t)[0] + 1},
    'Số ra kỳ trước': lambda t: set(R[t - 1]),
    'Liền kề ±1 số kỳ trước': lambda t: {m for n in R[t - 1] for m in (n - 1, n + 1)} - set(R[t - 1]),
    'Số kép': lambda t: K11,
    'Kép liền kề kép kỳ trước': lambda t: {m for k in R[t - 1] if k % 11 == 0 for m in (k - 11, k + 11)},
}
SIG = {t: GY['signals'](t) for t in TS}
TLX = {t: tl(t) for t in TS}
def pool(t, add=None, w=0.0):
    e = dict(TLX[t])
    for n in (add or ()):
        if 1 <= n <= NB: e[n] = e.get(n, 0) + w
    f, s = SIG[t]; return GY['pool_of'](GY['score'](f, s, e), s, 20)
def cnt(OD, K, W): hs = [len(set(OD[t][:K]) & R[t]) for t in range(T - W, T)]; return sum(h >= 3 for h in hs), sum(h >= 4 for h in hs)
def st(OD, K): return ' / '.join(f'{a * 100 // W}·{b * 100 // W}' for W in (10, 20, 50, 100) for a, b in [cnt(OD, K, W)])
BASE = {t: pool(t) for t in TS}
print(f'## {GAME} — cộng/trừ điểm dấu vết vào pool (100 kỳ, đến {DS[-1]}). Ô = % kỳ ≥3 số · ≥4 số, khung 10 / 20 / 50 / 100\n')
print(f'| Dấu vết | Điểm | Pool 15 | Pool 18 | Tăng ≥4 (50 & 100) |\n|---|---|---|---|---|')
print(f'| **Pool đang dùng** | — | {st(BASE, 15)} | {st(BASE, 18)} | |')
OUT = []
for nm, f in SIGS.items():
    for w in (1.0, -1.0):
        OD = {t: pool(t, f(t), w) for t in TS}
        tag = []
        for K in (15, 18):
            up = all(cnt(OD, K, W)[1] > cnt(BASE, K, W)[1] for W in (50, 100))
            dn3 = any(cnt(OD, K, W)[0] < cnt(BASE, K, W)[0] for W in (50, 100))
            if up: tag.append(f'P{K}' + (' (≥3 giảm)' if dn3 else ''))
        same = all(OD[t][:18] == BASE[t][:18] for t in TS)
        print(f"| {nm} | {'+1' if w > 0 else '−1'} | {st(OD, 15)} | {st(OD, 18)} | {', '.join(tag) or ('pool không đổi' if same else '')} |")
        if tag: OUT.append((nm, w, tag))
print('\nTăng ≥4 ở cả 50 & 100 kỳ:', OUT or 'không có')

