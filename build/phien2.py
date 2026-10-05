#!/usr/bin/env python3
"""Loto — tìm thêm dấu vết theo phiên: (1) 13h→21h cùng ngày và 21h→13h hôm sau; (2) luật loại tính TRONG phiên;
(3) hồi về trung vị theo phiên. Chấm theo từng kỳ, khung 100/200 kỳ của phiên đích, so với khung liền trước.
  python3 build/phien2.py"""
import json, os
D = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'all_data.json')))['loto535']
NB, KB = 35, 5; P = KB / NB * 100
dates = D['dates']; RA = [set(r) for r in D['res']]; N = len(RA)
ses = ['13' if '13h' in d else '21' for d in dates]
def rate_sets(pairs):
    h = n = 0
    for g, res in pairs: h += len(g & res); n += len(g)
    return h / max(n, 1) * 100
for tgt in ('13', '21'):
    idx = [i for i in range(N) if ses[i] == tgt and i >= 30]
    S = [i for i in range(N) if ses[i] == tgt]          # chỉ số các kỳ cùng phiên
    pos = {i: k for k, i in enumerate(S)}
    print(f'\n## Đích: phiên {tgt}h (bình quân mỗi số {P:.1f}%)')
    for W in (100, 200):
        A = idx[-W:]; B = idx[-2 * W:-W]
        def show(lab, fn, kind='rate'):
            if kind == 'rate':
                a = rate_sets([(fn(i), RA[i]) for i in A]); b = rate_sets([(fn(i), RA[i]) for i in B])
                sz = sum(len(fn(i)) for i in A) / W
                tag = '▲' if a > P + 1 and b > P + 0.5 else '▼' if a < P - 1 and b < P - 0.5 else ''
                print(f'  - {lab}: {a:.1f} / {b:.1f}% (TB {sz:.1f} số) {tag}')
            else:
                a = sum(fn(i) for i in A) / W * 100; b = sum(fn(i) for i in B) / W * 100
                print(f'  - {lab}: đúng {a:.0f} / {b:.0f}% kỳ')
        print(f'\n**Khung {W} kỳ {tgt}h** (gần / trước)')
        prev = lambda i: RA[i - 1]                       # kỳ ngay trước (phiên kia)
        ke = lambda s: {m for n in s for m in (n - 1, n + 1) if 1 <= m <= NB} - s
        show('Số của kỳ ngay trước (phiên kia)', prev)
        show('Kề ±1 của kỳ ngay trước', lambda i: ke(RA[i - 1]))
        show('Số của kỳ cùng phiên hôm trước', lambda i: RA[S[pos[i] - 1]] - RA[i - 1])
        show('Số ra ở CẢ 2 kỳ gần (phiên kia & cùng phiên hôm trước)', lambda i: RA[i - 1] & RA[S[pos[i] - 1]])
        def gp(i, n):   # vắng trong phiên
            g = 0; k = pos[i] - 1
            while k >= 0 and n not in RA[S[k]]: g += 1; k -= 1
            return g
        show('Số ra ≥2 lần trong 5 kỳ cùng phiên', lambda i: {n for n in range(1, NB + 1) if sum(n in RA[S[pos[i] - j]] for j in range(1, 6)) >= 2})
        show('Số tái xuất trong phiên (ra hôm trước sau vắng ≥10 kỳ phiên)', lambda i: {n for n in RA[S[pos[i] - 1]] if all(n not in RA[S[pos[i] - j]] for j in range(2, 12))})
        show('Số vắng 5–9 kỳ trong phiên', lambda i: {n for n in range(1, NB + 1) if 5 <= gp(i, n) <= 9})
        show('Số vắng 10–19 kỳ trong phiên', lambda i: {n for n in range(1, NB + 1) if 10 <= gp(i, n) <= 19})
        # hồi về trung vị tổng theo phiên
        def hoi(i):
            hist = sorted(sum(RA[S[pos[i] - j]]) for j in range(1, 101)); m = hist[50]; cur = sum(RA[S[pos[i] - 1]]); nx = sum(RA[i])
            return (nx < cur) if cur > m else (nx > cur) if cur < m else None
        a = [x for x in (hoi(i) for i in A) if x is not None]; b = [x for x in (hoi(i) for i in B) if x is not None]
        print(f'  - Tổng hồi về trung vị (so với cùng phiên hôm trước): đúng {sum(a) / len(a) * 100:.0f} / {sum(b) / len(b) * 100:.0f}% kỳ')
