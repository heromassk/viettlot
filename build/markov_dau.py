"""Markov theo đầu số (anh 12/10/2026, từ bài FB): mỗi đầu (0x..4x) mỗi kỳ ở trạng thái Câm / Thấp / Cao / Cả hai.
Bậc k: nhìn chuỗi k kỳ trước của đầu đó, đếm trong 200 kỳ trước kỳ cần đoán, chọn trạng thái hay ra nhất (thiếu dữ liệu → hạ bậc).
Pool = các nửa (thấp/cao) được đoán. Chấm 100 kỳ gần. python3 build/markov_dau.py [mega|power]"""
import json, sys, os
from collections import Counter
B = os.path.dirname(os.path.abspath(__file__)); g = sys.argv[1] if len(sys.argv) > 1 else 'mega'
KEY, NB = {'mega': ('mega645', 45), 'power': ('power655', 55)}[g]
R = [set(r[:6]) for r in json.load(open(os.path.join(B, 'all_data.json')))[KEY]['res']]; T = len(R)
DEC = {}
for n in range(1, NB + 1): DEC.setdefault(n // 10, []).append(n)
HALF = {d: (v[:len(v) // 2], v[len(v) // 2:]) for d, v in DEC.items()}   # thấp, cao
def st(t, d):
    lo, hi = HALF[d]; a, b = bool(R[t] & set(lo)), bool(R[t] & set(hi))
    return 'C' if not a and not b else 'T' if a and not b else 'H' if b and not a else 'TH'
S = {d: [st(t, d) for t in range(T)] for d in DEC}
def pred(t, d, k):
    seq = S[d]
    for kk in range(k, 0, -1):
        key = tuple(seq[t - kk:t]); c = Counter(seq[u] for u in range(max(kk, t - 200), t) if tuple(seq[u - kk:u]) == key)
        if sum(c.values()) >= 5: return c.most_common(1)[0][0]
    return Counter(seq[t - 200:t]).most_common(1)[0][0]
def pool(t, k):
    p = []
    for d in DEC:
        s = pred(t, d, k); lo, hi = HALF[d]
        if 'T' in s: p += lo
        if 'H' in s: p += hi
    return p
ts = range(T - 100, T)
print(f'## Markov theo đầu số — {g.upper()}, chấm 100 kỳ\n')
print('| Bậc | Đoán đúng trạng thái đầu | Pool TB | Trúng TB | Trúng/số | ≥3 số | ≥4 số |\n|---|---|---|---|---|---|---|')
for k in (1, 2, 3, 5):
    ok = sum(pred(t, d, k) == S[d][t] for t in ts for d in DEC) / (100 * len(DEC)) * 100
    P = [pool(t, k) for t in ts]; H = [len(set(p) & R[t]) for p, t in zip(P, ts)]
    sz = sum(map(len, P)) / 100
    print(f'| {k} | {ok:.0f}% | {sz:.1f} | {sum(H)/100:.2f} | {sum(H)/sum(map(len,P))*100:.1f}% | {sum(h>=3 for h in H)}% | {sum(h>=4 for h in H)}% |')
base = Counter(S[d][t] for t in ts for d in DEC); print('\nTrạng thái hay gặp nhất 100 kỳ:', dict(base))
print('Kỳ tới (bậc 2):', {d * 10: pred(T, d, 2) for d in DEC}, '→ pool', pool(T, 2))
