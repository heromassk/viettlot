#!/usr/bin/env python3
"""Số May Mắn Loto (anh 14/10/2026: cách "3 số vắng lâu nhất" đang trượt liên tục → tìm cách tốt hơn).
  python build/somayman_moi.py
Mỗi cách chọn 2 số / 12, chạy tiến (mỗi kỳ chỉ dùng số may mắn + kết quả các kỳ trước), chấm % kỳ đoán đúng ở
10 / 20 / 50 / 100 / 200 / 500 kỳ. Xếp theo độ đều qua các khung."""
import json, os
from collections import Counter
B = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(B, 'all_data.json'), encoding='utf-8'))['loto535']
LK = D['lk']; R = [set(r) for r in D['res']]; DT = D['dates']; T = len(LK)
SES = ['13' if '13h' in d else '21' for d in DT] + ['13' if '21h' in DT[-1] else '21']   # + phiên kỳ tới
KM = 2   # anh 14/10: pool số may mắn chỉ 2 số
K12 = range(1, 13)
def gap(t):
    return {k: next((g for g in range(t) if LK[t - 1 - g] == k), t) for k in K12}
def top3(sc, tie=None):
    tie = tie or {k: 0 for k in K12}
    return set(sorted(K12, key=lambda k: (-sc[k], -tie[k], k))[:KM])
def freq(t, W): c = Counter(LK[max(0, t - W):t]); return {k: c[k] for k in K12}
def markov(t, lag=1, W=200, same=False):
    c = {k: 0 for k in K12}; prev = LK[t - lag]
    for u in range(max(lag, t - W), t):
        if LK[u - lag] == prev and (not same or SES[u] == SES[t]): c[LK[u]] += 1
    return c
def markov2(t, W=300):
    c = {k: 0 for k in K12}
    for u in range(max(2, t - W), t):
        if LK[u - 1] == LK[t - 1] and LK[u - 2] == LK[t - 2]: c[LK[u]] += 1
    return c
def lienhuu(t, W=300):        # 連休回数 cho số may mắn: số đang vắng đúng g kỳ → lịch sử ra ngay kỳ kế bao nhiêu %
    g = gap(t); c = {}; h = {}
    for u in range(max(50, t - W), t):
        gu = gap(u)
        for k in K12: c[gu[k]] = c.get(gu[k], 0) + 1; h[gu[k]] = h.get(gu[k], 0) + (LK[u] == k)
    return {k: (h.get(g[k], 0) + 1 / 12 * 3) / (c.get(g[k], 0) + 3) for k in K12}
def chuoi(t, k=3, W=200):     # chuỗi ra/vắng bậc k (chung 12 số)
    st = lambda n, u: tuple(LK[u - 1 - i] == n for i in range(k))
    c = {}; h = {}
    for u in range(max(k, t - W), t):
        for n in K12: s = st(n, u); c[s] = c.get(s, 0) + 1; h[s] = h.get(s, 0) + (LK[u] == n)
    return {n: (h.get(st(n, t), 0) + 0.25) / (c.get(st(n, t), 0) + 3) for n in K12}
def phien(t, W=200):          # cùng phiên (13h/21h) nhiều nhất
    c = Counter(LK[u] for u in range(max(0, t - W), t) if SES[u] == SES[t]); return {k: c[k] for k in K12}
def so_chinh(t, W=300):       # MM theo số chính nhỏ nhất kỳ trước (mod 12)
    key = lambda u: min(R[u - 1]) % 12
    c = {k: 0 for k in K12}
    for u in range(max(1, t - W), t):
        if key(u) == key(t): c[LK[u]] += 1
    return c
def tong(t, W=300):           # MM theo tổng 5 số chính kỳ trước (mod 12)
    key = lambda u: sum(R[u - 1]) % 12
    c = {k: 0 for k in K12}
    for u in range(max(1, t - W), t):
        if key(u) == key(t): c[LK[u]] += 1
    return c

M = {
    'Vắng lâu nhất (cách đang dùng)': lambda t: top3(gap(t)),
    'Sát số may mắn kỳ trước': lambda t: set(sorted([k for k in K12 if k != LK[t - 1]], key=lambda k: (abs(k - LK[t - 1]), k))[:KM]),
    'Nóng 10 kỳ': lambda t: top3(freq(t, 10), freq(t, 50)),
    'Nóng 20 kỳ': lambda t: top3(freq(t, 20), freq(t, 100)),
    'Nóng 50 kỳ': lambda t: top3(freq(t, 50), freq(t, 200)),
    'Nóng 100 kỳ': lambda t: top3(freq(t, 100)),
    'Ít ra nhất 100 kỳ': lambda t: top3({k: -v for k, v in freq(t, 100).items()}),
    'Markov: sau số may mắn kỳ trước (200 kỳ)': lambda t: top3(markov(t, 1, 200), freq(t, 50)),
    'Markov: sau số may mắn kỳ trước (cả lịch sử)': lambda t: top3(markov(t, 1, 10**6), freq(t, 50)),
    'Markov trễ 2 kỳ (200 kỳ)': lambda t: top3(markov(t, 2, 200), freq(t, 50)),
    'Markov bậc 2: cặp 2 kỳ trước (300 kỳ)': lambda t: top3(markov2(t), freq(t, 50)),
    'Markov cùng phiên (200 kỳ)': lambda t: top3(markov(t, 1, 200, True), freq(t, 50)),
    'Nóng cùng phiên 200 kỳ': lambda t: top3(phien(t), freq(t, 50)),
    '連休回数: vắng đúng g kỳ → hay ra': lambda t: top3(lienhuu(t)),
    'Chuỗi ra/vắng bậc 3 (200 kỳ)': lambda t: top3(chuoi(t, 3)),
    'Chuỗi ra/vắng bậc 5 (300 kỳ)': lambda t: top3(chuoi(t, 5, 300)),
    'Theo số chính nhỏ nhất kỳ trước': lambda t: top3(so_chinh(t), freq(t, 50)),
    'Theo tổng 5 số chính kỳ trước': lambda t: top3(tong(t), freq(t, 50)),
}
TS = range(T - 500, T)
HIT = {nm: {t: LK[t] in f(t) for t in TS} for nm, f in M.items()}
# tự chọn: mỗi kỳ dùng cách đúng nhiều nhất 50 / 100 kỳ trước
def dyn(t, L):
    best = max((nm for nm in M), key=lambda nm: sum(HIT[nm][u] for u in range(t - L, t)) if t - L >= T - 500 else 0)
    return HIT[best][t]
for L in (50, 100):
    HIT[f'Tự chọn cách đúng nhiều nhất {L} kỳ trước'] = {t: dyn(t, L) for t in range(T - 500 + L, T)}
WS = (10, 20, 50, 100, 200, 500)
rows = []
for nm, h in HIT.items():
    r = [sum(h[t] for t in range(T - W, T) if t in h) / max(1, sum(1 for t in range(T - W, T) if t in h)) * 100 for W in WS]
    rows.append((min(r[:5]), sum(r[:5]) / 5, nm, r))
print('## Số May Mắn Loto — 2 số / 12, % kỳ đoán đúng (chạy tiến), đến ' + DT[-1] + '\n')
print('| Cách | 10 kỳ | 20 kỳ | 50 kỳ | 100 kỳ | 200 kỳ | 500 kỳ | Thấp nhất (10–200) |\n|---|---|---|---|---|---|---|---|')
for mn, av, nm, r in sorted(rows, key=lambda x: (-x[0], -x[1])):
    print(f'| {nm} | ' + ' | '.join(f'{v:.0f}%' for v in r) + f' | {mn:.0f}% |')
print('\nKỳ tới:')
for nm, f in M.items(): print(f'- {nm}: ' + ' '.join(f'{k:02d}' for k in sorted(f(T))))
