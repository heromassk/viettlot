#!/usr/bin/env python3
"""Markov nhiều bậc (anh, 14/10/2026): bậc nào giúp LOẠI bớt số, bậc nào giúp TĂNG số tiềm năng.
  python build/markov_bac.py power|mega|loto
Bậc k: bộ (một số ở kỳ t−k, …, một số ở kỳ t−1) → số ở kỳ t, học W kỳ gần; điểm mỗi số = tổng xác suất theo mọi bộ khớp hiện tại.
Trễ k: một số ở kỳ t−k → số ở kỳ t.
Chấm bằng chính nó ở 4 khung 10/20/50/100 kỳ gần (chạy tiến, mỗi kỳ chỉ dùng dữ liệu trước nó):
  LOẠI  — nhóm điểm 0 (chưa từng theo sau tình huống hiện tại) và 5 số điểm thấp nhất: % kỳ đúng (không số nào trong nhóm về),
          số bị loại ra mỗi kỳ (so TB). Đạt khi đúng ≥70% ở khung 50 và 100, và số bị loại ra ≤ TB.
  TIỀM NĂNG — top 10 / top 15: số ra mỗi kỳ (so TB), % kỳ có ≥2 / ≥3 số. Đạt khi ra > TB ở cả khung 50 và 100."""
import json, os, sys
from itertools import product
B = os.path.dirname(os.path.abspath(__file__))
G = {'power': ('power655', 55, 6, (50, 100)), 'mega': ('mega645', 45, 6, (50, 100)), 'loto': ('loto535', 35, 5, (50, 100, 200))}
g = sys.argv[1]; key, NB, KB, WS = G[g]
D = json.load(open(os.path.join(B, 'all_data.json'), encoding='utf-8'))[key]
R = [sorted(r) for r in D['res']]; RS = [set(r) for r in R]; T = len(R); TB = KB / NB * 100

def bac(t, k, W):
    cur = set(product(*[R[t - k + i] for i in range(k)])); c = {}; tn = {}
    for u in range(max(k, t - W), t):
        for tup in product(*[R[u - k + i] for i in range(k)]):
            if tup in cur:
                c[tup] = c.get(tup, 0) + 1
                for n in R[u]: tn[(tup, n)] = tn.get((tup, n), 0) + 1
    sc = [0.0] * (NB + 1)
    for (tup, n), v in tn.items(): sc[n] += v / c[tup]
    return sc

def tre(t, k, W):
    sc = [0.0] * (NB + 1); cx = [0] * (NB + 1); M = {}
    for u in range(max(k, t - W), t):
        for x in R[u - k]:
            cx[x] += 1
            for n in R[u]: M[(x, n)] = M.get((x, n), 0) + 1
    for x in R[t - k]:
        if cx[x]:
            for n in range(1, NB + 1): sc[n] += M.get((x, n), 0) / cx[x]
    return sc

# Markov trên CHUỖI RA/VẮNG của từng số (anh 14/10: Markov có tới bậc 10): bậc k = trạng thái k kỳ gần nhất của chính số đó
# (ra/vắng), học xem sau đúng trạng thái ấy số ra bao nhiêu %. "chung": gộp mọi số (nhiều mẫu); "riêng": chỉ lịch sử của số đó.
HB = [[0] * (T + 1) for _ in range(NB + 1)]          # HB[n][t] = bit i là (n ra ở kỳ t−1−i), 10 bit
for n in range(1, NB + 1):
    h = 0
    for t in range(T + 1):
        HB[n][t] = h
        if t < T: h = ((h << 1) | (n in RS[t])) & 1023
def chuoi(t, k, W, rieng):
    m = (1 << k) - 1; P0 = KB / NB; a = 3.0
    if not rieng:
        c = {}; h = {}
        for u in range(max(k, t - W), t):
            for n in range(1, NB + 1):
                st = HB[n][u] & m; c[st] = c.get(st, 0) + 1; h[st] = h.get(st, 0) + (n in RS[u])
        sc = [0.0] + [(h.get(HB[n][t] & m, 0) + a * P0) / (c.get(HB[n][t] & m, 0) + a) for n in range(1, NB + 1)]
    else:
        sc = [0.0]
        for n in range(1, NB + 1):
            st0 = HB[n][t] & m; c = h = 0
            for u in range(max(k, t - W), t):
                if HB[n][u] & m == st0: c += 1; h += n in RS[u]
            sc.append((h + a * P0) / (c + a))
    return sc
VAR_CHUOI = [(f'Chuỗi ra/vắng bậc {k}, {"riêng từng số" if r else "chung mọi số"}, học {W} kỳ', (lambda t, k=k, W=W, r=r: chuoi(t, k, W, r)))
             for r in (False, True) for k in range(1, 11) for W in WS]
VAR = [(f'Bậc {k}, học {W} kỳ', (lambda t, k=k, W=W: bac(t, k, W))) for k in (1, 2, 3, 4) for W in WS] + \
      [(f'Trễ {k} kỳ, học {W} kỳ', (lambda t, k=k, W=W: tre(t, k, W))) for k in (2, 3) for W in WS]
if '--chuoi' in sys.argv: VAR = VAR_CHUOI
TS = range(T - 100, T)
out = []
for nm, f in VAR:
    rec = []
    for t in TS:
        sc = f(t); od = sorted(range(1, NB + 1), key=lambda n: (-sc[n], n))
        zero = {n for n in range(1, NB + 1) if sc[n] == 0} if '--chuoi' not in sys.argv else {n for n in range(1, NB + 1) if sc[n] <= 0.6 * KB / NB}
        low5 = set(od[-5:]); res = RS[t]
        rec.append(dict(z=(len(zero), len(zero & res)), l5=len(low5 & res), t10=len(set(od[:10]) & res), t15=len(set(od[:15]) & res)))
    def w(W, fn): x = rec[-W:]; return fn(x)
    row = dict(nm=nm)
    for W in (10, 20, 50, 100):
        x = rec[-W:]
        zn = sum(a for a, b in (r['z'] for r in x)); zh = sum(b for a, b in (r['z'] for r in x))
        row[W] = dict(z_ok=sum(r['z'][1] == 0 for r in x) / W * 100, z_sz=zn / W, z_ra=zh / zn * 100 if zn else None,
                      l5_ok=sum(r['l5'] == 0 for r in x) / W * 100, l5_ra=sum(r['l5'] for r in x) / (5 * W) * 100,
                      t10=sum(r['t10'] for r in x) / (10 * W) * 100, t15=sum(r['t15'] for r in x) / (15 * W) * 100,
                      t15g3=sum(r['t15'] >= 3 for r in x) / W * 100, t10g2=sum(r['t10'] >= 2 for r in x) / W * 100)
    out.append(row)
pc = lambda v: '—' if v is None else f'{v:.0f}%'
print(f'## {key} — Markov nhiều bậc, 4 khung 10/20/50/100 kỳ gần (đến {D["dates"][-1]}). TB mỗi số ra {TB:.1f}%/kỳ\n')
print('### Dùng để LOẠI số\n')
print('| Biến thể | ' + ('Nhóm điểm ≤60% TB' if '--chuoi' in sys.argv else 'Nhóm điểm 0') + ': cỡ TB · kỳ đúng 10/20/50/100 · số bị loại ra | 5 số điểm thấp nhất: kỳ đúng 10/20/50/100 · ra | Đạt |\n|---|---|---|---|')
for r in out:
    z = r; okz = r[50]['z_ok'] >= 70 and r[100]['z_ok'] >= 70 and r[100]['z_sz'] > 0.3 and (r[100]['z_ra'] or 0) <= TB
    okl = r[50]['l5_ok'] >= 70 and r[100]['l5_ok'] >= 70 and r[100]['l5_ra'] <= TB
    print(f"| {r['nm']} | {r[100]['z_sz']:.1f} số · {' / '.join(pc(r[W]['z_ok']) for W in (10, 20, 50, 100))} · {pc(r[100]['z_ra'])} | "
          f"{' / '.join(pc(r[W]['l5_ok']) for W in (10, 20, 50, 100))} · {r[100]['l5_ra']:.1f}% | {'✔ nhóm 0' if okz else ''}{' ✔ 5 thấp' if okl else ''}{'' if okz or okl else '✘'} |")
print('\n### Dùng làm SỐ TIỀM NĂNG\n')
print('| Biến thể | Top 10: ra mỗi số 10/20/50/100 | Top 15: ra mỗi số 10/20/50/100 | Top 15 kỳ ≥3 số (50 / 100) | Đạt |\n|---|---|---|---|---|')
for r in out:
    ok = r[50]['t15'] > TB and r[100]['t15'] > TB
    ok10 = r[50]['t10'] > TB and r[100]['t10'] > TB
    print(f"| {r['nm']} | {' / '.join(f'{r[W][chr(116)+chr(49)+chr(48)]:.1f}%' for W in (10, 20, 50, 100))} | {' / '.join(f'{r[W][chr(116)+chr(49)+chr(53)]:.1f}%' for W in (10, 20, 50, 100))} | {r[50]['t15g3']:.0f}% / {r[100]['t15g3']:.0f}% | {'✔ top 15' if ok else ''}{' ✔ top 10' if ok10 else ''}{'' if ok or ok10 else '✘'} |")
