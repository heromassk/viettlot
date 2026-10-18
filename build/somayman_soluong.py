#!/usr/bin/env python3
"""Số May Mắn Loto — tìm cách chọn tốt và số lượng hợp lý (anh 14/10/2026: "cho 2 số mà tỉ lệ thấp quá").
  python build/somayman_soluong.py
Mỗi cách là một luật CỐ ĐỊNH, chạy tiến (mỗi kỳ chỉ dùng số may mắn các kỳ trước), chọn K = 2..6 số / 12.
Chấm bằng chính nó: % kỳ đoán đúng ở 10 / 20 / 50 / 100 / 200 / 500 kỳ gần nhất, độ ổn định = khung thấp nhất.
So các cách với NHAU; không so với bốc ngẫu nhiên."""
import json, os
from collections import Counter
B = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(B, 'all_data.json'), encoding='utf-8'))['loto535']
LK = D['lk']; DT = D['dates']; T = len(LK)
SES = ['13' if '13h' in d else '21' for d in DT] + ['13' if '21h' in DT[-1] else '21']
K12 = range(1, 13)
WS = (10, 20, 50, 100, 200, 500)
START = T - 500


def gap(t): return {k: next((g for g in range(t) if LK[t - 1 - g] == k), t) for k in K12}
def freq(t, W): c = Counter(LK[max(0, t - W):t]); return {k: c[k] for k in K12}
def phien(t, W=200):
    c = Counter(LK[u] for u in range(max(0, t - W), t) if SES[u] == SES[t]); return {k: c[k] for k in K12}
def markov(t, W=200):
    c = {k: 0 for k in K12}; p = LK[t - 1]
    for u in range(max(1, t - W), t):
        if LK[u - 1] == p: c[LK[u]] += 1
    return c


def rank(score, tie=None):
    """Xếp 12 số theo điểm (cao trước), hòa thì xét tie rồi số nhỏ."""
    tie = tie or {k: 0 for k in K12}
    return sorted(K12, key=lambda k: (-score[k], -tie[k], k))


def can_bang(t):
    """Cân bằng 4 khung: số ra ít ở 20/50/100/200 kỳ (MM có xu hướng cân bằng — ghi-chu 04/10)."""
    s = {k: 0.0 for k in K12}
    for W in (20, 50, 100, 200):
        f = freq(t, W)
        for i, k in enumerate(rank({k: -v for k, v in f.items()})): s[k] += 12 - i
    return s


# mỗi cách trả về THỨ TỰ 12 số (đứng đầu = nên chọn nhất); chọn K số đầu
M = {
    'Vắng lâu nhất': lambda t: rank(gap(t)),
    'Nóng 10 kỳ': lambda t: rank(freq(t, 10), freq(t, 50)),
    'Nóng 10 kỳ trong ±3 quanh MM kỳ trước (đang dùng)':
        lambda t: (lambda f10, f50: sorted(K12, key=lambda k: (abs(k - LK[t - 1]) > 3, -f10[k], -f50[k], k)))(freq(t, 10), freq(t, 50)),
    'Nóng 20 kỳ': lambda t: rank(freq(t, 20), freq(t, 100)),
    'Nóng 50 kỳ': lambda t: rank(freq(t, 50), freq(t, 200)),
    'Ít ra nhất 100 kỳ': lambda t: rank({k: -v for k, v in freq(t, 100).items()}),
    'Ít ra nhất 200 kỳ': lambda t: rank({k: -v for k, v in freq(t, 200).items()}),
    'Cân bằng 4 khung (ít ra ở 20/50/100/200)': lambda t: rank(can_bang(t)),
    'Nóng cùng phiên 200 kỳ': lambda t: rank(phien(t), freq(t, 50)),
    'Ít ra cùng phiên 200 kỳ': lambda t: rank({k: -v for k, v in phien(t).items()}, gap(t)),
    'Theo sau MM kỳ trước (200 kỳ)': lambda t: rank(markov(t), freq(t, 50)),
    'Sát MM kỳ trước': lambda t: sorted(K12, key=lambda k: (abs(k - LK[t - 1]), k)),
    'MM kỳ trước + vắng lâu nhất': lambda t: [LK[t - 1]] + [k for k in rank(gap(t)) if k != LK[t - 1]],
}


BASE = dict(M)


def vote(t):
    """Gộp phiếu: mỗi cách gốc cho điểm theo thứ hạng (Borda), cộng lại."""
    s = {k: 0 for k in K12}
    for nm, f in BASE.items():
        for i, k in enumerate(f(t)): s[k] += 12 - i
    return rank(s, gap(t))


M['Gộp phiếu mọi cách (Borda)'] = vote

ORD = {nm: {t: f(t) for t in range(START, T + 1)} for nm, f in M.items()}


def rate(nm, K, W):
    ts = range(T - W, T)
    return sum(LK[t] in ORD[nm][t][:K] for t in ts) / W * 100


print(f'## Số May Mắn Loto — % kỳ đoán đúng theo số lượng chọn, chạy tiến, đến {DT[-1]} ({T} kỳ)\n')
best = {}
for K in (2, 3, 4, 5, 6):
    rows = []
    for nm in M:
        r = [rate(nm, K, W) for W in WS]
        rows.append((min(r), sum(r) / len(r), nm, r))
    rows.sort(key=lambda x: (-x[0], -x[1]))
    best[K] = rows[0]
    print(f'### Chọn {K} số\n')
    print('| Cách | 10 | 20 | 50 | 100 | 200 | 500 | Thấp nhất | Kỳ tới |\n|---|---|---|---|---|---|---|---|---|')
    for mn, av, nm, r in rows:
        nxt = ' '.join(f'{k:02d}' for k in sorted(ORD[nm][T][:K]))
        print(f'| {nm} | ' + ' | '.join(f'{v:.0f}%' for v in r) + f' | **{mn:.0f}%** | {nxt} |')
    print()
print('### Tóm tắt: cách ổn định nhất ở từng số lượng\n')
print('| Số lượng | Cách | 100 kỳ | 200 kỳ | 500 kỳ | Thấp nhất (6 khung) |\n|---|---|---|---|---|---|')
for K, (mn, av, nm, r) in best.items():
    print(f'| {K} | {nm} | {r[3]:.0f}% | {r[4]:.0f}% | {r[5]:.0f}% | {mn:.0f}% |')
