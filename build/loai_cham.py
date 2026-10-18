#!/usr/bin/env python3
"""Chấm TỪNG CÁCH LOẠI (anh 15/10/2026): mỗi cách loại bao nhiêu số/kỳ, trong đó bao nhiêu số THẬT RA (= điểm tụt),
và % kỳ có loại oan ≥1 số. Gộp lần lượt: tổng số loại, tổng điểm tụt. Khung 50 / 100 / 200 kỳ. Riêng từng game.
  python build/loai_cham.py power|mega|loto"""
import os, sys
B = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, B)
GAME = sys.argv[1]
_src = open(os.path.join(B, 'goiy.py'), encoding='utf-8').read(); _argv = sys.argv; sys.argv = ['goiy.py', GAME]
GY = {'__file__': os.path.join(B, 'goiy.py'), '__name__': 'goiy_head'}
exec(compile(_src[:_src.index('# ---------- Đà tổng')], 'goiy.py', 'exec'), GY); sys.argv = _argv; GY['CUR'] = None
R, T, NB, KB = GY['R'], GY['T'], GY['NB'], GY['KB']
NAME = {'vang': 'Vắng ≥20 kỳ', 'vang1': 'Vắng lâu nhất', 'nong35': 'Ra 3 lần / 5 kỳ', 'thua': 'Thưa & vắng ≥15 kỳ', 'vangph20': 'Vắng ≥20 kỳ cùng phiên',
        'it100': 'Ra ít nhất 100 kỳ', 'lien2': 'Ra 2 kỳ liền', 'lt3': 'Ra kỳ trước & kỳ t−3', 'zprev': 'Số lớn nhất kỳ trước', 'tx15': 'Tái xuất sau vắng ≥15',
        'duoi': 'Cùng đuôi kỳ trước', 'kho': 'Bóng khó ra'}
KEYS = ['vang'] + list(GY['LOAI'][GAME])
SIG = {t: GY['signals'](t)[1] for t in range(T - 200, T)}
def st(t, k): return set(SIG[t].get(k, ()) or ())
print(f'## {GAME} — chấm từng cách loại, đến {GY["D"]["dates"][-1]} (điểm tụt = số thật ra mà cách đó loại mất)\n')
print('| Cách loại | Loại TB số/kỳ | Điểm tụt TB/kỳ | % số loại thật ra (loại oan) | % kỳ có loại oan ≥1 số |')
print('|---|---|---|---|---|')
def row(lab, F):
    cells = []
    for W in (50, 100, 200):
        ts = range(T - W, T); n = sum(len(F(t)) for t in ts); h = sum(len(F(t) & set(R[t])) for t in ts); k = sum(bool(F(t) & set(R[t])) for t in ts)
        cells.append((n / W, h / W, h / n * 100 if n else None, k / W * 100))
    f = lambda i, fmt: ' / '.join('—' if c[i] is None else fmt.format(c[i]) for c in cells)
    print(f'| {lab} | {f(0, "{:.1f}")} | {f(1, "{:.2f}")} | {f(2, "{:.0f}%")} | {f(3, "{:.0f}%")} |')
for k in KEYS: row(NAME.get(k, k), lambda t, k=k: st(t, k))
acc = []
print('\n### Gộp dần theo thứ tự trên (số bị loại tính không trùng)\n')
print('| Sau khi thêm | Loại TB số/kỳ | Điểm tụt TB/kỳ | % kỳ có loại oan |\n|---|---|---|---|')
for i, k in enumerate(KEYS):
    ks = KEYS[:i + 1]; U = lambda t, ks=ks: set().union(*[st(t, x) for x in ks])
    cells = []
    for W in (50, 100, 200):
        ts = range(T - W, T); cells.append((sum(len(U(t)) for t in ts) / W, sum(len(U(t) & set(R[t])) for t in ts) / W, sum(bool(U(t) & set(R[t])) for t in ts) / W * 100))
    print(f"| + {NAME.get(k, k)} | {' / '.join(f'{c[0]:.1f}' for c in cells)} | {' / '.join(f'{c[1]:.2f}' for c in cells)} | {' / '.join(f'{c[2]:.0f}%' for c in cells)} |")
