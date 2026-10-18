#!/usr/bin/env python3
"""Kiểm lại các luật dạng (khuon.py) cho nhiều phép thử (anh 15/10/2026: "áp đi").
Mỗi luật ứng viên: đúng k/n kỳ ở khung 100 gần nhất (khung 50 nằm trong đó). Kiểm định nhị thức một phía H0: đúng ≤ 70%
(chính ngưỡng 70% anh đặt, KHÔNG so với ngẫu nhiên). Hiệu chỉnh Benjamini–Hochberg trên MỌI luật ứng viên của game
(q=0,10). Thêm cận dưới Wilson 95%. Luật 'vững' = qua BH; 'mong manh' = đạt 70% ở 50 & 100 kỳ nhưng không qua BH.
  python build/khuon_fdr.py loto|mega|power"""
import os, sys, math
from scipy.stats import binomtest
B = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, B)
GAME = sys.argv[1]
_src = open(os.path.join(B, 'goiy.py'), encoding='utf-8').read(); _argv = sys.argv; sys.argv = ['goiy.py', GAME]
GY = {'__file__': os.path.join(B, 'goiy.py'), '__name__': 'goiy_head'}
exec(compile(_src[:_src.index('# ---------- Đà tổng')], 'goiy.py', 'exec'), GY); sys.argv = _argv; GY['CUR'] = None
import khuon
R, T, NB, KB, D = GY['R'], GY['T'], GY['NB'], GY['KB'], GY['D']
LK = D['lk'] if GAME == 'loto' else None
res = khuon.build(R, LK, NB, KB, T, full=True)
def wil(k, n, z=1.96):
    if not n: return 0.0
    p = k / n; d = 1 + z * z / n
    return (p + z * z / (2 * n) - z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))) / d * 100
rows = [r for r in res['all'] if r['n100'] >= 8]
for r in rows: r['p'] = binomtest(r['k100'], r['n100'], 0.70, alternative='greater').pvalue
m = len(rows); order = sorted(rows, key=lambda r: r['p']); cut = 0
for i, r in enumerate(order, 1):
    if r['p'] <= 0.10 * i / m: cut = i
for i, r in enumerate(order, 1): r['bh'] = i <= cut
print(f'## {GAME} — kiểm lại luật dạng đến {D["dates"][-1]}: {m} luật ứng viên (n100 ≥ 8), BH q=0,10\n')
good = [r for r in rows if r['good']]
print(f'- Đạt ≥70% ở cả 50 & 100 kỳ (app đang coi là đạt): **{len(good)}** luật · qua BH: **{sum(r["bh"] for r in good)}** · mong manh: **{sum(not r["bh"] for r in good)}**')
print(f'- Đang dùng trong khuôn kỳ tới: {sum(r["sel"] for r in rows)} luật\n')
print('| Luật | Đúng 50 kỳ | Đúng 100 kỳ | Cận dưới Wilson 95% | p (≤70%) | Qua BH | Đang dùng |\n|---|---|---|---|---|---|---|')
for r in sorted(good, key=lambda r: r['p']):
    print(f"| {r['lab'] or r['id']} | {r['k50']}/{r['n50']} ({r['k50']/r['n50']*100:.0f}%) | {r['k100']}/{r['n100']} ({r['k100']/r['n100']*100:.0f}%) | {wil(r['k100'], r['n100']):.0f}% | {r['p']:.3f} | {'✔' if r['bh'] else '✘'} | {'có' if r['sel'] else ''} |")
b2 = khuon.build(R, LK, NB, KB, T, bh=True)
a, b = res, b2
print(f"\n### Khuôn kỳ tới: hiện tại vs chỉ giữ luật qua BH\n")
print('| | Số luật | Lọt khuôn 50 / 100 kỳ | Giữ lại % dãy ngẫu nhiên lọt khuôn |\n|---|---|---|---|')
for nm, x in (('Hiện tại', a), ('Chỉ luật qua BH', b)):
    print(f"| {nm} | {len(x['rules'])} | {x['pass50']}% / {x['pass100']}% | {x['keep']}% |")
print('\nLuật hiện tại: ' + ' · '.join(r['lab'] for r in a['rules']))
print('Luật sau BH: ' + ' · '.join(r['lab'] for r in b['rules']))
