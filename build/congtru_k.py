"""Cộng/trừ qua NHIỀU kỳ trước (anh, 08/10/2026): mỗi số n được 1 phiếu cho mỗi lần n = x±d với x ra trong k kỳ gần
(kỳ gần nặng hơn nếu --nang). Pool = top K số nhiều phiếu (bỏ số vừa ra kỳ trước). Chấm TB số trúng/kỳ ở 10/20/50/100 kỳ + 3 đoạn.
Dùng: python3 build/congtru_k.py mega|power"""
import json, sys, os
g = sys.argv[1]; key, N = {'mega': ('mega645', 45), 'power': ('power655', 55)}[g]
D = json.load(open(os.path.join(os.path.dirname(__file__), 'all_data.json')))[key]
R = [set(sorted(r)[:6]) for r in D['res']]; T = len(R)
DS = {'±1': (1,), '±10': (10,), '±1,±10': (1, 10), '±3': (3,), '±1,3,10': (1, 3, 10), 'trùng': (0,), 'trùng,±1,±10': (0, 1, 10)}
def pool(t, k, ds, K):
    v = {}
    for j in range(1, k + 1):
        for x in R[t - j]:
            for d in ds:
                for n in ({x} if d == 0 else (x - d, x + d)):
                    if 1 <= n <= N: v[n] = v.get(n, 0) + 1
    return sorted((n for n in v if n not in R[t - 1]), key=lambda n: (-v[n], n))[:K]
def tb(ts, k, ds, K): return sum(len(set(pool(t, k, ds, K)) & R[t]) for t in ts) / len(ts)
K = int(sys.argv[2]) if len(sys.argv) > 2 else 12
print(f'{g.upper()} — pool {K} số nhiều phiếu nhất, TB số trúng/kỳ (pool {K} số: mỗi kỳ kỳ vọng chia đều {6 * K / N:.2f})\n')
print('| Cộng/trừ | Số kỳ trước (k) | 10 | 20 | 50 | 100 | 3 đoạn 100 kỳ | 500 kỳ |\n|---|---|---|---|---|---|---|---|')
res = []
for lab, ds in DS.items():
    for k in (1, 2, 3, 5, 7, 10, 15, 20):
        r = [tb(range(T - W, T), k, ds, K) for W in (10, 20, 50, 100)]
        dd = [tb(range(T - 100 * i - 100, T - 100 * i), k, ds, K) for i in (2, 1, 0)]
        r5 = tb(range(T - 500, T), k, ds, K)
        res.append((lab, k, r, dd, r5))
        print(f'| {lab} | {k} | ' + ' | '.join(f'{x:.2f}' for x in r) + ' | ' + '/'.join(f'{x:.2f}' for x in dd) + f' | {r5:.2f} |')
