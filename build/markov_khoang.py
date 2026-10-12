"""Máy học chuyển khoảng (anh 12/10/2026): kỳ trước có số trong khoảng 1–5 thì kỳ sau / kỳ sau nữa ra khoảng nào.
Khoảng 5 số (01–05, 06–10, …). Học bảng chuyển trên 200 kỳ trước kỳ cần đoán (kỳ t−1 → t: bậc 1; kỳ t−2 → t: cách 1 kỳ;
cặp (t−2, t−1) → t: xét 2 kỳ). Chọn các khoảng điểm cao nhất làm pool. Chấm 100 kỳ gần.
python3 build/markov_khoang.py mega|power"""
import json, sys, os
from collections import defaultdict
B = os.path.dirname(os.path.abspath(__file__)); g = sys.argv[1] if len(sys.argv) > 1 else 'mega'
KEY, NB = {'mega': ('mega645', 45), 'power': ('power655', 55)}[g]
R = [set(r[:6]) for r in json.load(open(os.path.join(B, 'all_data.json')))[KEY]['res']]; T = len(R)
NK = (NB + 4) // 5; kh = lambda n: (n - 1) // 5
KS = [set(kh(n) for n in r) for r in R]
def nums(k): return [n for n in range(1, NB + 1) if kh(n) == k]
def learn(t, W=200):
    c1 = defaultdict(lambda: [0] * NK); c2 = defaultdict(lambda: [0] * NK); cc = defaultdict(lambda: [0] * NK); n1 = defaultdict(int); n2 = defaultdict(int); nc = defaultdict(int)
    for u in range(t - W, t):
        for a in KS[u - 1]:
            n1[a] += 1
            for b in KS[u]: c1[a][b] += 1
        for a in KS[u - 2]:
            n2[a] += 1
            for b in KS[u]: c2[a][b] += 1
        for a in KS[u - 2]:
            for a2 in KS[u - 1]:
                nc[(a, a2)] += 1
                for b in KS[u]: cc[(a, a2)][b] += 1
    return c1, n1, c2, n2, cc, nc
def score(t, mode):
    c1, n1, c2, n2, cc, nc = learn(t); s = [0.0] * NK
    for b in range(NK):
        if mode in ('1', 'all'): s[b] += sum(c1[a][b] / n1[a] for a in KS[t - 1] if n1[a])
        if mode in ('2', 'all'): s[b] += sum(c2[a][b] / n2[a] for a in KS[t - 2] if n2[a])
        if mode in ('cap',): s[b] += sum(cc[(a, a2)][b] / nc[(a, a2)] for a in KS[t - 2] for a2 in KS[t - 1] if nc[(a, a2)] >= 3)
    return s
ts = range(T - 100, T)
print(f'## Máy học chuyển khoảng 5 số — {g.upper()}, chấm 100 kỳ (học 200 kỳ trước mỗi kỳ)\n')
print('| Cách | Pool | Trúng TB | Trúng/số | ≥3 số | ≥4 số | Hai nửa ≥4 |\n|---|---|---|---|---|---|---|')
for mode, lab in (('1', 'Kỳ trước → kỳ sau'), ('2', 'Kỳ t−2 → kỳ sau nữa'), ('all', 'Cộng cả 2 kỳ'), ('cap', 'Cặp (t−2, t−1) → kỳ sau')):
    for nk in (4, 5):
        H = []
        for t in ts:
            s = score(t, mode); top = sorted(range(NK), key=lambda b: -s[b])[:nk]
            H.append(len({n for b in top for n in nums(b)} & R[t]))
        sz = nk * 5
        print(f'| {lab}, {nk} khoảng | {sz} | {sum(H)/100:.2f} | {sum(H)/100/sz*100:.1f}% | {sum(h>=3 for h in H)}% | {sum(h>=4 for h in H)}% | {sum(h>=4 for h in H[:50])*2}·{sum(h>=4 for h in H[50:])*2}% |')
s = score(T, 'all'); top = sorted(range(NK), key=lambda b: -s[b])
print('\nKỳ tới — xếp khoảng (cộng 2 kỳ):', ' > '.join(f'{nums(b)[0]:02d}–{nums(b)[-1]:02d}' for b in top))
