#!/usr/bin/env python3
"""Dấu vết W kỳ gần nhất (mặc định 100) cho power|mega|loto.
  python3 build/suyluan.py mega [--W 100]
 Mỗi luật LOẠI chấm theo từng kỳ: kỳ đó luật đúng (không số bị loại nào về) hay sai.
So 2 đoạn: 100 kỳ gần nhất và 100 kỳ trước đó (độ ổn định). Cột 'vé giữ lại' = phần vé 6 số còn lại sau khi loại."""
import json, os, math, sys
from math import comb
GM = {'power': ('power655', 55, 6), 'mega': ('mega645', 45, 6), 'loto': ('loto535', 35, 5)}
key, NB, KB = GM[sys.argv[1]]
WW = int(sys.argv[sys.argv.index('--W') + 1]) if '--W' in sys.argv else 100
D = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'all_data.json')))[key]
R = [set(r) for r in D['res']]; T = len(R)
def feat(t, W=100):
    gap = {}; 
    for n in range(1, NB + 1):
        g = 0
        while g < t and n not in R[t - 1 - g]: g += 1
        gap[n] = g
    c = {w: {n: sum(n in R[u] for u in range(t - w, t)) for n in range(1, NB + 1)} for w in sorted({10, 20, 50, 100, 200, WW})}
    return gap, c
P = KB / NB
def z(cnt, w): return (cnt - w * P) / math.sqrt(w * P * (1 - P))
RULES = {}
for G in (10, 15, 20, 25, 30):
    RULES[f'Bỏ số vắng ≥{G} kỳ'] = (lambda G: lambda t, g, c: {n for n in g if g[n] >= G})(G)
RULES['Bỏ số khó ra 100 kỳ (z<−1.5)'] = lambda t, g, c: {n for n in g if z(c[WW][n], 100) < -1.5}
RULES['Bỏ số khó ra 200 kỳ (z<−1.5)'] = lambda t, g, c: {n for n in g if z(c[200][n], 200) < -1.5}
for k in (3, 5):
    RULES[f'Bỏ {k} số ra ít nhất 100 kỳ'] = (lambda k: lambda t, g, c: set(sorted(c[100], key=lambda n: (c[WW][n], -g[n]))[:k]))(k)
    RULES[f'Bỏ {k} số ra ít nhất 50 kỳ'] = (lambda k: lambda t, g, c: set(sorted(c[50], key=lambda n: (c[50][n], -g[n]))[:k]))(k)
RULES['Bỏ số ra 2 kỳ liền'] = lambda t, g, c: R[t - 1] & R[t - 2]
RULES['Bỏ số quá nóng (≥4 lần/10 kỳ)'] = lambda t, g, c: {n for n in g if c[10][n] >= 4}
RULES['Bỏ số vắng 21–30 kỳ'] = lambda t, g, c: {n for n in g if 21 <= g[n] <= 30}
RULES['Bỏ số vừa vắng 0 lần ở 20 kỳ & vắng ≥10'] = lambda t, g, c: {n for n in g if c[20][n] == 0 and g[n] >= 10}
def ben(t, lowside=True):
    e = 25 * P; q = [{n: sum(n in R[u] for u in range(t - 100 + 25 * i, t - 75 + 25 * i)) for n in range(1, NB + 1)} for i in range(4)]
    return {n for n in range(1, NB + 1) if all((x[n] < e) if lowside else (x[n] > e) for x in q)}
RULES['Bỏ số ít ra cả 4 đoạn 25 kỳ (lệch bền)'] = lambda t, g, c: ben(t)
RULES['GỘP: vắng ≥25 + ra 2 kỳ liền + quá nóng'] = lambda t, g, c: RULES['Bỏ số vắng ≥25 kỳ'](t, g, c) | RULES['Bỏ số ra 2 kỳ liền'](t, g, c) | RULES['Bỏ số quá nóng (≥4 lần/10 kỳ)'](t, g, c)
RULES['GỘP: vắng ≥30 + ra 2 kỳ liền'] = lambda t, g, c: RULES['Bỏ số vắng ≥30 kỳ'](t, g, c) | RULES['Bỏ số ra 2 kỳ liền'](t, g, c)
RULES['GỘP: vắng ≥20 + lệch bền ít'] = lambda t, g, c: RULES['Bỏ số vắng ≥20 kỳ'](t, g, c) | ben(t)
INC = {'Có ≥1 số nhiều ra cả 4 đoạn 25 kỳ': lambda t: ben(t, False)}
segs = [(f'{WW} kỳ gần nhất', T - WW, T), (f'{WW} kỳ trước đó', T - 2 * WW, T - WW)]
res = {k: [] for k in RULES}
for name, a, b in segs:
    acc = {k: [0, 0, 0.0] for k in RULES}
    for t in range(a, b):
        g, c = feat(t)
        for k, f in RULES.items():
            ex = f(t, g, c); ok = not (ex & R[t])
            acc[k][0] += ok; acc[k][1] += len(ex); acc[k][2] += comb(NB - len(ex), KB) / comb(NB, KB)
    for k in RULES: res[k].append((acc[k][0], acc[k][1] / (b - a), acc[k][2] / (b - a) * 100))
print(f'## {key} — luật loại chấm theo từng kỳ\n\n| Luật loại | Đúng: {WW} kỳ gần | {WW} kỳ trước | Bỏ TB (số) | Vé giữ lại | Đánh giá |\n|---|---|---|---|---|---|')
for k, v in res.items():
    r1 = v[0][0] / WW * 100; r2 = v[1][0] / WW * 100; kp = v[0][2]
    tag = '✔ mạnh' if r1 >= 85 and r2 >= 80 and r1 >= kp else ('~ theo dõi' if r1 >= 70 and r1 >= kp - 2 else '✘')
    print(f'| {k} | **{r1:.0f}%** | {r2:.0f}% | {v[0][1]:.1f} | {kp:.0f}% | {tag} |')
# hiện trạng 100 kỳ
g, c = feat(T)
exp = 100 * P
print(f'\nHiện tại ({WW} kỳ, kỳ vọng {exp:.1f} lần/số):')
srt = sorted(range(1, NB + 1), key=lambda n: c[WW][n])
g_now = g
print('Ra ít nhất:', ', '.join(f'{n:02d}({c[WW][n]}, vắng {g[n]})' for n in srt[:8]))
print('Ra nhiều nhất:', ', '.join(f'{n:02d}({c[WW][n]})' for n in srt[::-1][:8]))
print('Vắng lâu nhất:', ', '.join(f'{n:02d}({g[n]})' for n in sorted(g, key=lambda n: -g[n])[:8]))
# 4 đoạn 25 kỳ: số lệch bền
q = [{n: sum(n in R[u] for u in range(T - 100 + 25 * i, T - 75 + 25 * i)) for n in range(1, NB + 1)} for i in range(4)]
e25 = 25 * P
lo = [n for n in range(1, NB + 1) if all(x[n] < e25 for x in q)]; hi = [n for n in range(1, NB + 1) if all(x[n] > e25 for x in q)]
print('Ít ra ở cả 4 đoạn 25 kỳ:', ' '.join(f'{n:02d}' for n in lo) or '—', '· Nhiều ở cả 4 đoạn:', ' '.join(f'{n:02d}' for n in hi) or '—')

for k, f in INC.items():
    for name, a, b in segs:
        ok = n = sz = 0
        for t in range(a, b):
            st = f(t)
            if not st: continue
            n += 1; ok += bool(st & R[t]); sz += len(st)
        print(f'{k} — {name}: đúng {ok}/{n} kỳ, nhóm TB {sz / max(n, 1):.1f} số, vé giữ lại ≈ {(1 - comb(NB - round(sz / max(n, 1)), KB) / comb(NB, KB)) * 100:.0f}%')

print('\nÁp vào kỳ tới:')
for k, f in RULES.items():
    ex = f(T, g, c)
    if ex: print(f'- {k}: {" ".join(f"{n:02d}" for n in sorted(ex))}')
