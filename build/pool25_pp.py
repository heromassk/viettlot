"""Thử hàng loạt phương pháp chọn pool 25 (anh, 10/10/2026: muốn ≥4 số). Chấm 200 kỳ gần (2 đoạn 100).
python3 build/pool25_pp.py power|mega"""
import json, sys, os, itertools, datetime as dt
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
g = sys.argv[1]; KEY, NB = {'mega': ('mega645', 45), 'power': ('power655', 55)}[g]
OTH = {'mega': 'power655', 'power': 'mega645'}[g]
A = json.load(open(os.path.join(HERE, 'all_data.json')))
R = [set(r) for r in A[KEY]['res']]; T = len(R)
dd = lambda s: dt.datetime.strptime(s[:10], '%d/%m/%Y')
DT = [dd(d) for d in A[KEY]['dates']]; OD = [(dd(d), set(r)) for d, r in zip(A[OTH]['dates'], A[OTH]['res'])]
SR = [sorted(r) for r in A[KEY]['res']]
REC = json.load(open(f'/tmp/claude-0/r25_{g}.json'))
N = range(1, NB + 1); lon = lambda n: int(f'{n:02d}'[::-1])
def gap(t, n):
    k = 0
    while k < 300 and n not in R[t - 1 - k]: k += 1
    return k
def cnt(t, n, w): return sum(n in R[t - j] for j in range(1, w + 1))
def gaps_hist(t, n, w=200):
    idx = [u for u in range(t - w, t) if n in R[u]]; return [b - a - 1 for a, b in zip(idx, idx[1:])]
M = {}   # tên → hàm điểm (cao = chọn)
for w in (5, 10, 20, 30, 50, 100, 200): M[f'Nóng {w} kỳ'] = (lambda w: lambda t, n: cnt(t, n, w) + 1e-3 * cnt(t, n, 200))(w)
M['Nguội 100 kỳ'] = lambda t, n: -cnt(t, n, 100)
M['Vắng lâu nhất'] = lambda t, n: gap(t, n)
M['Vắng ngắn nhất'] = lambda t, n: -gap(t, n)
def cyc(t, n):
    h = gaps_hist(t, n); g_ = gap(t, n)
    if len(h) < 3: return -9
    return -abs(g_ - float(np.median(h)))
M['Đúng nhịp nghỉ (vắng ≈ trung vị)'] = cyc
def due(t, n):
    h = gaps_hist(t, n); g_ = gap(t, n)
    return sum(x == g_ for x in h) / max(1, sum(x >= g_ for x in h))   # xác suất ra đúng ở mức vắng này
M['Xác suất ra theo mức vắng (200 kỳ)'] = due
for d, k in itertools.product((1, 2), (1, 3, 5)):
    M[f'±{d} qua {k} kỳ'] = (lambda d, k: lambda t, n: sum((n - d in R[t - j]) + (n + d in R[t - j]) for j in range(1, k + 1)))(d, k)
M['±13/14 qua 3 kỳ'] = lambda t, n: sum((n + s * c) in R[t - j] for j in (1, 2, 3) for s in (1, -1) for c in (13, 14))
M['Lộn 3 kỳ'] = lambda t, n: sum(lon(x) == n != x for j in (1, 2, 3) for x in R[t - j])
def cheo(t, n):
    o = [s for e, s in OD if e < DT[t]]; return sum(n in s for s in o[-3:])
M['Chéo game 3 kỳ'] = cheo
def follow(t, n, w=200):   # số hay ra ngay sau các số của kỳ trước (200 kỳ)
    last = R[t - 1]; return sum(len(R[u - 1] & last) for u in range(t - w, t) if n in R[u])
M['Theo sau kỳ trước (200 kỳ)'] = follow
def pair(t, n, w=200):   # hay ra cùng kỳ với số của kỳ trước
    last = R[t - 1]; return sum(len((R[u] - {n}) & last) for u in range(t - w, t) if n in R[u])
M['Cặp đi cùng số kỳ trước'] = pair
def pos(t, n, w=100):    # tần suất theo vị trí sắp xếp, cộng xác suất ở các vị trí
    return sum(SR[u].count(n) for u in range(t - w, t))
def tail(t, n): return sum(x % 10 == n % 10 for j in (1, 2, 3) for x in R[t - j])
M['Cùng đuôi 3 kỳ'] = tail
M['Khác đuôi 3 kỳ'] = lambda t, n: -tail(t, n)
def dec(t, n): return sum(x // 10 == n // 10 for j in range(1, 11) for x in R[t - j])
M['Hàng chục nóng 10 kỳ'] = dec
M['Đà tăng (10 vs 50)'] = lambda t, n: cnt(t, n, 10) / 10 - cnt(t, n, 50) / 50
M['Cách app hiện tại'] = lambda t, n: (25 - REC[t - (T - 200)]['rk'].index(n)) if n in REC[t - (T - 200)]['rk'] else -1
ts = list(range(T - 200, T))
S = {k: {t: np.array([f(t, n) for n in N], float) for t in ts} for k, f in M.items()}
Y = {t: np.array([n in R[t] for n in N]) for t in ts}
def ev(sc, tt, K=25):
    h = np.array([Y[t][np.argsort(-sc[t] + 1e-9 * np.arange(NB))[:K]].sum() for t in tt]); return h
def line(h): return f'{h.mean():.2f} | {np.mean(h>=3)*100:.0f}% | {np.mean(h>=4)*100:.0f}% | {np.mean(h>=5)*100:.0f}%'
A1, A2 = ts[:100], ts[100:]
res = []
for k in M:
    h1, h2 = ev(S[k], A1), ev(S[k], A2); res.append((np.mean(h2 >= 4), k, h1, h2))
# kết hợp: cộng hạng của 2–3 phương pháp tốt nhất ở đoạn cũ (chọn trên đoạn cũ, kiểm đoạn mới)
def rank(sc): return {t: np.argsort(np.argsort(sc[t])) for t in sc}
RK = {k: rank(S[k]) for k in M}
old = sorted(M, key=lambda k: -np.mean(ev(S[k], A1) >= 4))
for r in (2, 3, 4):
    best = None
    for c in itertools.combinations(old[:8], r):
        sc = {t: sum(RK[k][t] for k in c) for t in ts}; v = np.mean(ev(sc, A1) >= 4)
        if best is None or v > best[0]: best = (v, c, sc)
    res.append((np.mean(ev(best[2], A2) >= 4), 'Ghép ' + ' + '.join(best[1]), ev(best[2], A1), ev(best[2], A2)))
print(f'## {g.upper()} — {len(res)} phương pháp chọn pool 25 (đoạn cũ = kỳ 200→101, đoạn mới = 100 kỳ gần)\n')
print('| Phương pháp | Đoạn cũ: TB · ≥3 · ≥4 · ≥5 | Đoạn mới: TB · ≥3 · ≥4 · ≥5 |\n|---|---|---|')
for _, k, h1, h2 in sorted(res, key=lambda x: -x[0]): print(f'| {k} | {line(h1)} | {line(h2)} |')
