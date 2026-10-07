#!/usr/bin/env python3
"""Kiểm 1 bộ số anh tự chọn trong quá khứ (anh, 07/10/2026): đã từng ra trọn bộ chưa, trúng 3/4/5 số kỳ nào,
TB số trúng ở 4 khung 10/20/50/100 kỳ + 3 đoạn 100 kỳ + cả lịch sử (chấm bằng chính bộ đó).
  python3 build/kiem_bo.py power|mega|loto 01 05 07 08 16 18"""
import json, os, sys
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
g = sys.argv[1]; S = {int(x) for x in sys.argv[2:]}
key = {'power': 'power655', 'mega': 'mega645', 'loto': 'loto535'}[g]
A = json.load(open(os.path.join(HERE, 'all_data.json')))[key]; D, R = A['dates'], [set(r) for r in A['res']]; N = len(R)
h = [len(R[t] & S) for t in range(N)]; c = Counter(h); K = len(S)
print(f'Bộ {" ".join(f"{x:02d}" for x in sorted(S))} — {g.upper()} {N} kỳ ({D[0]} → {D[-1]})\n')
print('| Trúng | ' + ' | '.join(f'{j} số' for j in range(K + 1)) + ' |\n|' + '---|' * (K + 2))
print('| Số kỳ | ' + ' | '.join(str(c[j]) for j in range(K + 1)) + ' |\n')
f = lambda a: f'{sum(a) / len(a):.2f}'
print('TB số trúng mỗi kỳ: 10 kỳ ' + f(h[-10:]) + ' · 20 kỳ ' + f(h[-20:]) + ' · 50 kỳ ' + f(h[-50:]) + ' · 100 kỳ ' + f(h[-100:])
      + ' · 3 đoạn 100 kỳ ' + ' / '.join(f(h[N - 100 * (i + 1):N - 100 * i]) for i in range(3)) + ' · cả lịch sử ' + f(h))
top = sorted(range(N), key=lambda t: -h[t])
print('\nCác kỳ trúng nhiều nhất:')
for t in [t for t in top if h[t] >= max(3, max(h) - 1)][:15]:
    print(f'- {D[t]}: {" ".join(f"{x:02d}" for x in sorted(R[t]))} → trúng {h[t]} ({" ".join(f"{x:02d}" for x in sorted(R[t] & S))})')
print('\nTừng số trong bộ ra bao nhiêu lần — 10 / 20 / 50 / 100 kỳ / cả LS:')
for x in sorted(S):
    print(f'- {x:02d}: ' + ' / '.join(str(sum(x in r for r in R[-W:])) for W in (10, 20, 50, 100)) + f' / {sum(x in r for r in R)}')
