#!/usr/bin/env python3
"""Tâm linh / thần số học có giúp pool không (anh, 14/10/2026). Chạy tiến 100 kỳ gần, 4 khung 10/20/50/100.
  python build/kiemtra_app.py 200     # lấy 20 PP tâm linh từng kỳ từ app (khi dữ liệu đổi)
  python build/kiemtra_tamlinh.py power|mega|loto
1) Từng phương pháp: số nó chọn ra mỗi kỳ so với TB của game; % kỳ có ≥1 số trúng.
2) Lên pool: pool đang dùng KHÔNG cộng tâm linh vs CÓ cộng (như app: top 12 phiếu +1, tâm linh mạnh +0,5);
   và gắn RIÊNG từng phương pháp (+1 cho số nó chọn)."""
import json, os, sys
B = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, B)
GAME = sys.argv[1]
_src = open(os.path.join(B, 'goiy.py'), encoding='utf-8').read(); _argv = sys.argv; sys.argv = ['goiy.py', GAME]
GY = {'__file__': os.path.join(B, 'goiy.py'), '__name__': 'goiy_head'}
exec(compile(_src[:_src.index('# ---------- Đà tổng')], 'goiy.py', 'exec'), GY); sys.argv = _argv; GY['CUR'] = None
R, T, NB, KB = GY['R'], GY['T'], GY['NB'], GY['KB']; TB = KB / NB * 100
APP = json.load(open(os.path.join(B, 'kiemtra_app.json'), encoding='utf-8'))[GAME]
assert APP['L'] == T, 'chạy lại kiemtra_app.py'
W0 = len(APP['dates']); T0 = T - W0; TS = range(T - 100, T)
KX = APP['kx']
def nums(x, t): v = x['nums'][t - T0]; return set(n for n in (v or []) if 1 <= n <= NB)
def votes(t):
    v = {n: 0 for n in range(1, NB + 1)}
    for x in KX:
        for n in nums(x, t): v[n] += 1
    return v
def extra_app(t):
    v = votes(t); top = sorted(v, key=lambda n: (-v[n], n))[:12]; v5 = sorted(v.values(), reverse=True)[4]
    e = {n: 1.0 for n in top}
    for n in top:
        if v[n] >= v5: e[n] += 0.5
    return e
def pool(t, extra=None):
    f, s = GY['signals'](t); return GY['pool_of'](GY['score'](f, s, extra), s, 20)
def st(OD, K):
    out = []
    for W in (10, 20, 50, 100):
        hs = [len(set(OD[t][:K]) & R[t]) for t in range(T - W, T)]
        out.append(f'{sum(h >= 3 for h in hs) / W * 100:.0f}·{sum(h >= 4 for h in hs) / W * 100:.0f}')
    return ' / '.join(out)
SIG = {t: GY['signals'](t) for t in TS}
def poolS(t, extra=None):
    f, s = SIG[t]; return GY['pool_of'](GY['score'](f, s, extra), s, 20)
BASE = {t: poolS(t) for t in TS}
TL = {t: poolS(t, extra_app(t)) for t in TS}
print(f'## {GAME} — tâm linh có giúp pool không (chạy tiến 100 kỳ gần, đến {GY["D"]["dates"][-1]}). TB mỗi số ra {TB:.1f}%/kỳ\n')
print('### 1) Từng phương pháp tâm linh: số nó chọn ra mỗi kỳ (10 / 20 / 50 / 100 kỳ) — so TB của game\n')
print('| Phương pháp | Chọn TB (số/kỳ) | Ra mỗi số 10 / 20 / 50 / 100 kỳ | Kỳ có ≥1 số trúng (100 kỳ) | Nghiêng (50 & 100) |\n|---|---|---|---|---|')
rows = []
for x in KX + [dict(id='phieu', nm='Tổng phiếu 20 phương pháp, top 12', g='')]:
    def S(t): return nums(x, t) if x['id'] != 'phieu' else set(sorted(votes(t), key=lambda n: (-votes(t)[n], n))[:12])
    sz = sum(len(S(t)) for t in TS) / 100
    r = []
    for W in (10, 20, 50, 100):
        z = sum(len(S(t)) for t in range(T - W, T)); h = sum(len(S(t) & R[t]) for t in range(T - W, T)); r.append(h / z * 100 if z else None)
    any1 = sum(bool(S(t) & R[t]) for t in TS)
    ok = r[2] is not None and r[3] is not None and r[2] > TB and r[3] > TB
    rows.append((ok, r[3] or 0, f"| {x['nm']} | {sz:.1f} | {' / '.join('—' if v is None else f'{v:.1f}%' for v in r)} | {any1}% | {'✔ ra nhiều hơn TB' if ok else ('✘ ra ít hơn TB' if r[2] is not None and r[3] is not None and r[2] < TB and r[3] < TB else '~')} |"))
for _, _, l in sorted(rows, key=lambda x: (-x[0], -x[1])): print(l)
print('\n### 2) Lên pool đang dùng: % kỳ ≥3 số · ≥4 số (10 / 20 / 50 / 100 kỳ)\n')
print('| Pool | Không cộng tâm linh | Có cộng tâm linh (như app) |\n|---|---|---|')
for K in (10, 15, 18): print(f'| {K} | {st(BASE, K)} | {st(TL, K)} |')
print('\n**Gắn riêng từng phương pháp (+1 cho số nó chọn) — chỉ liệt kê cái làm pool 15 hoặc 18 tăng ≥3 hoặc ≥4 số ở cả khung 50 & 100:**\n')
def num(OD, K):
    o = {}
    for W in (50, 100):
        hs = [len(set(OD[t][:K]) & R[t]) for t in range(T - W, T)]; o[W] = (sum(h >= 3 for h in hs), sum(h >= 4 for h in hs))
    return o
B15, B18 = num(BASE, 15), num(BASE, 18); found = 0
for x in KX:
    OD = {t: poolS(t, {n: 1.0 for n in nums(x, t)}) for t in TS}
    o15, o18 = num(OD, 15), num(OD, 18); good = []
    for K, o, b in ((15, o15, B15), (18, o18, B18)):
        for j, lab in ((0, '≥3'), (1, '≥4')):
            if o[50][j] > b[50][j] and o[100][j] > b[100][j]: good.append(f'P{K} {lab}')
    if good:
        found += 1; print(f"- {x['nm']}: {', '.join(good)} · pool 15 {st(OD, 15)} · pool 18 {st(OD, 18)}")
if not found: print('- Không phương pháp nào.')

# ---- kiểm bộ kết hợp trước khi đưa vào app ----
COMBO = {'loto': [['Thái Ất (thời kế, rút gọn)'], ['Tử vi (Mệnh, Cục, sao Tử Vi)'], ['Thái Ất (thời kế, rút gọn)', 'Tử vi (Mệnh, Cục, sao Tử Vi)']],
         'mega': [['Thần số học'], ['Thần số học', 'Chạm đầu đuôi'], ['Thần số học', 'Lộn + kép']],
         'power': [['Tử vi (Mệnh, Cục, sao Tử Vi)'], ['Bát trạch (cung mệnh)'], ['Tử vi (Mệnh, Cục, sao Tử Vi)', 'Bát trạch (cung mệnh)']]}[GAME]
BYN = {x['nm']: x for x in KX}
print('\n### Bộ kết hợp (+1 cho số mỗi phương pháp chọn) — % kỳ ≥3 · ≥4 số (10 / 20 / 50 / 100 kỳ)\n')
print(f'| Bộ | Pool 10 | Pool 15 | Pool 18 |\n|---|---|---|---|\n| Không tâm linh | {st(BASE, 10)} | {st(BASE, 15)} | {st(BASE, 18)} |')
for cb in COMBO:
    def ex(t):
        e = {}
        for nm in cb:
            for n in nums(BYN[nm], t): e[n] = e.get(n, 0) + 1.0
        return e
    OD = {t: poolS(t, ex(t)) for t in TS}
    print(f"| {' + '.join(cb)} | {st(OD, 10)} | {st(OD, 15)} | {st(OD, 18)} |")
