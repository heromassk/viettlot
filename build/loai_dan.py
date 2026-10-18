#!/usr/bin/env python3
"""Bỏ DẦN từng 5 số từ pool đầy đủ (anh 15/10/2026): mỗi cách xếp 35 số từ "đáng bỏ" đến "đáng giữ"; mỗi bước bỏ 5 số xấu nhất
của cách đó trong pool hiện có. Chấm: % số THẬT RA còn giữ lại (so với bước trước) và % kỳ không mất số nào, khung 50/100/200 kỳ
+ độ ổn định (4 khối 50 kỳ). Chọn tham lam: mỗi bước lấy cách giữ nhiều nhất, rồi đi tiếp từ pool đó.
Mỗi kỳ chỉ dùng dữ liệu trước nó. Riêng từng game.
  python build/loai_dan.py loto|mega|power [số bước bỏ=5]"""
import json, os, sys
from collections import Counter
B = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, B)
GAME = sys.argv[1]; STEP = int(sys.argv[2]) if len(sys.argv) > 2 else 5
key, NB, KB = {'power': ('power655', 55, 6), 'mega': ('mega645', 45, 6), 'loto': ('loto535', 35, 5)}[GAME]
_src = open(os.path.join(B, 'goiy.py'), encoding='utf-8').read(); _argv = sys.argv; sys.argv = ['goiy.py', GAME]
GY = {'__file__': os.path.join(B, 'goiy.py'), '__name__': 'goiy_head'}
exec(compile(_src[:_src.index('# ---------- Đà tổng')], 'goiy.py', 'exec'), GY); sys.argv = _argv; GY['CUR'] = None
R, T, DATES = [set(r) for r in GY['R']], GY['T'], GY['D']['dates']
SES = ['13' if '13h' in d else '21' for d in DATES] if GAME == 'loto' else None
N = range(1, NB + 1); TS = list(range(T - 200, T))
# đếm cộng dồn
PRE = [[0] * (NB + 1)]
for r in R: PRE.append([PRE[-1][n] + (n in r) for n in range(NB + 1)])
cW = lambda t, W: [PRE[t][n] - PRE[max(0, t - W)][n] for n in range(NB + 1)]
def gapv(t):
    g = [0] * (NB + 1)
    for n in N:
        k = 0
        while k < t and n not in R[t - 1 - k]: k += 1
        g[n] = k
    return g
def gap_ph(t):
    g = [0] * (NB + 1)
    us = [u for u in range(t - 1, -1, -1) if SES[u] == SES[t]]
    for n in N:
        k = 0
        for u in us:
            if n in R[u]: break
            k += 1
        g[n] = k
    return g
def cph(t, W):
    c = [0] * (NB + 1); us = [u for u in range(t - 1, max(-1, t - 3 * W), -1) if SES[u] == SES[t]][:W]
    for u in us:
        for n in R[u]: c[n] += 1
    return c
HNUM = lambda n: n // 10
def hang_c(t, W):
    c = Counter()
    for u in range(max(0, t - W), t):
        for n in R[u]: c[HNUM(n)] += 1
    return c
M = {}   # tên -> hàm t -> list điểm (cao = giữ, thấp = bỏ trước)
M['Vắng lâu nhất → bỏ'] = lambda t: [-v for v in gapv(t)]
M['Ra ít nhất 100 kỳ → bỏ'] = lambda t: cW(t, 100)
M['Ra ít nhất 50 kỳ → bỏ'] = lambda t: cW(t, 50)
M['Ra ít nhất 20 kỳ → bỏ'] = lambda t: cW(t, 20)
M['Ra nhiều nhất 5 kỳ → bỏ'] = lambda t: [-v for v in cW(t, 5)]
M['Ra nhiều nhất 10 kỳ → bỏ'] = lambda t: [-v for v in cW(t, 10)]
M['Ra nhiều nhất 20 kỳ → bỏ'] = lambda t: [-v for v in cW(t, 20)]
M['Vừa ra kỳ trước → bỏ'] = lambda t: [-(n in R[t - 1]) for n in range(NB + 1)]
M['Cùng đuôi kỳ trước → bỏ'] = lambda t: [-((n % 10) in {v % 10 for v in R[t - 1]}) for n in range(NB + 1)]
M['Vắng 6–10 kỳ → bỏ'] = lambda t: [-(6 <= g <= 10) for g in gapv(t)]
M['Vắng 11–15 kỳ → giữ (bỏ số khác)'] = lambda t: [(11 <= g <= 15) for g in gapv(t)]
M['Kề ±1 số kỳ trước → giữ'] = lambda t: [any(abs(n - v) == 1 for v in R[t - 1]) for n in range(NB + 1)]
M['Hàng ra nhiều 10 kỳ → bỏ'] = lambda t: (lambda hc: [-hc[HNUM(n)] for n in range(NB + 1)])(hang_c(t, 10))
M['Hàng ra ít 20 kỳ → bỏ'] = lambda t: (lambda hc: [hc[HNUM(n)] for n in range(NB + 1)])(hang_c(t, 20))
M['Số chẵn/lẻ ngược kỳ trước → giữ'] = lambda t: [(n % 2) != (sum(v % 2 for v in R[t - 1]) > len(R[t - 1]) / 2) for n in range(NB + 1)]
if SES:
    M['Vắng lâu cùng phiên → bỏ'] = lambda t: [-v for v in gap_ph(t)]
    M['Ra ít 30 kỳ cùng phiên → bỏ'] = lambda t: cph(t, 30)
    M['Ra nhiều 10 kỳ cùng phiên → bỏ'] = lambda t: [-v for v in cph(t, 10)]
    M['Vừa ra kỳ cùng giờ trước → bỏ'] = lambda t: (lambda us: [-(n in R[us[0]]) for n in range(NB + 1)])([u for u in range(t - 1, -1, -1) if SES[u] == SES[t]])
SIG = {t: GY['signals'](t) for t in TS}
def app_score(t):
    f, s = SIG[t]; sc = GY['score'](f, s, {}); return [sc.get(n, 0) for n in range(NB + 1)]
M['Điểm tổng hợp của app (chưa tâm linh)'] = app_score
# Markov (anh 15/10/2026: "markov không dùng à"): bộ số bậc 1–4, chuỗi ra/vắng bậc 1–10 (chung mọi số), Markov bậc 2 của app
def _vec(d): return [d.get(n, 0) for n in range(NB + 1)]
for k in (1, 2, 3, 4):
    M[f'Markov bộ số bậc {k} (học 50 kỳ)'] = (lambda t, k=k: _vec(GY['mkbac_rank'](t, k, 50)))
for k in (1, 2, 3, 5, 7, 10):
    M[f'Markov chuỗi ra/vắng bậc {k} (chung, 100 kỳ)'] = (lambda t, k=k: _vec(GY['chuoi_rank'](t, k, 100)))
if 'mk_rank' in GY: M['Markov bậc 2 của app (mk_rank)'] = lambda t: _vec(GY['mk_rank'](t))
APP = json.load(open(os.path.join(B, 'kiemtra_app.json'), encoding='utf-8')).get(GAME)
if APP and APP['L'] == T:
    T0 = T - len(APP['dates'])
    for x in APP['kx']:
        nm = x['nm']
        M[f'TL: {nm} (có trong PP → giữ)'] = (lambda t, x=x: [(n in set(x['nums'][t - T0] or [])) for n in range(NB + 1)])
    def votes(t):
        v = [0] * (NB + 1)
        for x in APP['kx']:
            for n in (x['nums'][t - T0] or []):
                if 1 <= n <= NB: v[n] += 1
        return v
    M['TL: Tổng phiếu 20 phương pháp'] = votes
CACHE = {nm: {t: f(t) for t in TS} for nm, f in M.items()}
C100 = {t: cW(t, 100) for t in TS}
def bo(P, nm, t, k):
    sc = CACHE[nm][t]; c = C100[t]
    order = sorted(P, key=lambda n: (sc[n], c[n], n))
    return set(order[k:])
STAGES = []
P = {t: set(N) for t in TS}
size = NB
path = []
print(f'## {GAME} — bỏ dần mỗi lần {STEP} số, đến {DATES[-1]} (số thật ra giữ lại; ổn định = 4 khối 50 kỳ)\n')
while size - STEP >= KB + 2 + (10 if GAME != 'loto' else 5) - 5 and size - STEP >= 10:
    rows = []
    for nm in M:
        Q = {t: bo(P[t], nm, t, STEP) for t in TS}
        blk = []
        for b in range(4):
            ts = TS[b * 50:(b + 1) * 50]
            h0 = sum(len(P[t] & R[t]) for t in ts); h1 = sum(len(Q[t] & R[t]) for t in ts)
            blk.append(h1 / h0 * 100 if h0 else 100.0)
        win = []
        for W in (50, 100, 200):
            ts = TS[-W:]; h0 = sum(len(P[t] & R[t]) for t in ts); h1 = sum(len(Q[t] & R[t]) for t in ts)
            nl = sum(len(Q[t] & R[t]) == len(P[t] & R[t]) for t in ts) / W * 100
            win.append((h1 / h0 * 100 if h0 else 100.0, nl))
        rows.append((nm, win, blk, Q))
    rows.sort(key=lambda r: (-(r[1][0][0] + r[1][1][0] + r[1][2][0]) / 3, -min(r[2])))
    size -= STEP; best = rows[0]
    print(f'### Bỏ {STEP} số: {size + STEP} → **{size}** số\n')
    print('| # | Cách bỏ | % số trúng giữ lại (50 / 100 / 200 kỳ) | % kỳ không mất số nào | Thấp nhất – cao nhất 4 khối 50 kỳ |\n|---|---|---|---|---|')
    for i, (nm, win, blk, _) in enumerate(rows[:10], 1):
        print(f"| {i} | {nm} | {' / '.join(f'{w[0]:.0f}%' for w in win)} | {' / '.join(f'{w[1]:.0f}%' for w in win)} | {min(blk):.0f}% – {max(blk):.0f}% |")
    h200 = sum(len(best[3][t] & R[t]) for t in TS) / 200
    P = best[3]; path.append((size, best[0], best[1], best[2], h200))
    print(f'\n→ Chọn: **{best[0]}**. Pool {size} số giữ TB {h200:.2f}/{KB} số trúng mỗi kỳ ({h200 / KB * 100:.0f}%).\n')
print('### Đường đi đã chọn\n')
print('| Pool | Cách bỏ ở bước này | % giữ bước này (50 / 100 / 200) | Khối thấp nhất | Giữ so với ban đầu (200 kỳ) |\n|---|---|---|---|---|')
for size, nm, win, blk, h in path:
    print(f"| {size} | {nm} | {' / '.join(f'{w[0]:.0f}%' for w in win)} | {min(blk):.0f}% | {h / KB * 100:.0f}% |")
