"""Quét hàng trăm phương pháp chọn pool 25 (anh, 10/10/2026). Mỗi phương pháp cố định cách tính,
chấm ≥4 số trên 2 đoạn: 100 kỳ cũ (200→101) và 100 kỳ gần. Xếp theo đoạn KÉM hơn (ổn định mới tính).
python3 build/pool25_quet.py power|mega"""
import json, sys, os, itertools, datetime as dt
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
g = sys.argv[1]; KEY, NB = {'mega': ('mega645', 45), 'power': ('power655', 55)}[g]
OTH = {'mega': 'power655', 'power': 'mega645'}[g]; K = 25
A = json.load(open(os.path.join(HERE, 'all_data.json')))
res = A[KEY]['res']; T = len(res)
P = np.zeros((T, NB + 1)); [P.__setitem__((i, r), 1) for i, rr in enumerate(res) for r in [rr]]
P = P[:, 1:]                                   # P[t, n-1]
dd = lambda s: dt.datetime.strptime(s[:10], '%d/%m/%Y')
od = [(dd(d), r) for d, r in zip(A[OTH]['dates'], A[OTH]['res'])]
O = np.zeros((T, NB))                          # O[t] = kỳ game kia gần nhất trước kỳ t (j=1), lưu theo thứ tự
OL = []
for d in A[KEY]['dates']:
    prev = [r for e, r in od if e < dd(d)]; OL.append(prev[-10:])
REC = json.load(open(f'/tmp/claude-0/r25_{g}.json'))
ts = np.arange(T - 200, T); A1, A2 = ts[:100], ts[100:]
nums = np.arange(1, NB + 1); lon = np.array([int(f'{n:02d}'[::-1]) for n in nums])
def shift(v, d):                               # v[n] -> điểm cho n+d và n-d
    o = np.zeros(NB)
    if d == 0: return v.copy()
    o[d:] += v[:-d]; o[:-d] += v[d:]; return o
GAP = np.zeros((T, NB))
for t in range(1, T):
    GAP[t] = np.where(P[t - 1] > 0, 0, GAP[t - 1] + 1)
CS = np.vstack([np.zeros(NB), np.cumsum(P, 0)])   # CS[t] = tổng P[0..t-1]
hot = lambda t, w: CS[t] - CS[t - w]
M = {}
def add(name, f): M[name] = f
for w in (3, 5, 8, 10, 15, 20, 25, 30, 40, 50, 75, 100, 150, 200):
    add(f'Nóng {w} kỳ', lambda t, w=w: hot(t, w) + 1e-3 * hot(t, 200)); add(f'Nguội {w} kỳ', lambda t, w=w: -hot(t, w) - 1e-3 * hot(t, 200))
for h in (2, 3, 5, 8, 13, 20, 30, 50, 80):
    wts = 0.5 ** (np.arange(1, 201) / h)
    add(f'Nóng giảm dần (nửa {h} kỳ)', lambda t, wts=wts: wts @ P[t - 200:t][::-1]); add(f'Nguội giảm dần (nửa {h})', lambda t, wts=wts: -(wts @ P[t - 200:t][::-1]))
for c in range(0, 31): add(f'Vắng ≈ {c} kỳ', lambda t, c=c: -abs(GAP[t] - c) + 1e-3 * hot(t, 100))
for c in (5, 10, 15, 20, 25, 30): add(f'Vắng ≥{c} trước', lambda t, c=c: (GAP[t] >= c) + 1e-3 * GAP[t])
for d in range(0, 21):
    for k in (1, 2, 3, 4, 5, 7, 10):
        add(f'±{d} qua {k} kỳ', lambda t, d=d, k=k: sum(shift(P[t - j], d) for j in range(1, k + 1)) + 1e-3 * hot(t, 100))
for k in (1, 2, 3, 5, 7, 10):
    def lo(t, k=k):
        v = np.zeros(NB)
        for j in range(1, k + 1):
            for n in np.nonzero(P[t - j])[0] + 1:
                m = lon[n - 1]
                if m != n and 1 <= m <= NB: v[m - 1] += 1
        return v + 1e-3 * hot(t, 100)
    add(f'Lộn qua {k} kỳ', lo)
    def ch(t, k=k):
        v = np.zeros(NB)
        for r in OL[t][-k:]:
            for n in r:
                if n <= NB: v[n - 1] += 1
        return v + 1e-3 * hot(t, 100)
    add(f'Chéo game qua {k} kỳ', ch)
    add(f'Cùng đuôi qua {k} kỳ', lambda t, k=k: sum((nums % 10)[:, None] == (np.nonzero(P[t - j])[0] + 1) % 10 for j in range(1, k + 1)).sum(1) + 1e-3 * hot(t, 100))
    add(f'Khác đuôi qua {k} kỳ', lambda t, k=k: -sum(((nums % 10)[:, None] == (np.nonzero(P[t - j])[0] + 1) % 10).sum(1) for j in range(1, k + 1)) + 1e-3 * hot(t, 100))
    add(f'Hàng chục nóng qua {k} kỳ', lambda t, k=k: sum(((nums // 10)[:, None] == (np.nonzero(P[t - j])[0] + 1) // 10).sum(1) for j in range(1, k + 1)) + 1e-3 * hot(t, 100))
for m in range(2, 10):
    for w in (10, 30):
        add(f'Lớp chia {m} nóng {w} kỳ', lambda t, m=m, w=w: np.array([hot(t, w)[(nums % m) == (n % m)].sum() for n in nums]) + 1e-3 * hot(t, 100))
for w in (50, 100, 200):
    for lag in (1, 2, 3):
        def fo(t, w=w, lag=lag):
            last = P[t - lag]; return sum(P[u] * (P[u - lag] @ last) for u in range(t - w, t)) + 1e-3 * hot(t, 100)
        add(f'Theo sau kỳ t−{lag} ({w} kỳ)', fo)
    add(f'Cặp đi cùng kỳ trước ({w} kỳ)', lambda t, w=w: sum(P[u] * (P[u] @ P[t - 1]) for u in range(t - w, t)) + 1e-3 * hot(t, 100))
for w in (100, 200):
    def due(t, w=w):
        v = np.zeros(NB)
        for i in range(NB):
            idx = np.nonzero(P[t - w:t, i])[0]; gl = np.diff(idx) - 1; gg = GAP[t, i]
            v[i] = (gl == gg).sum() / max(1, (gl >= gg).sum())
        return v
    add(f'Xác suất ra ở mức vắng ({w} kỳ)', due)
add('Cách app hiện tại', lambda t: np.array([(25 - REC[t - (T - 200)]['rk'].index(n)) if n in REC[t - (T - 200)]['rk'] else -1 for n in nums], float))
Y = P[ts]
def hits(S):   # S: 200×NB
    top = np.argsort(-S + 1e-9 * nums, 1)[:, :K]; return np.take_along_axis(Y, top, 1).sum(1)
SC = {k: np.array([f(t) for t in ts]) for k, f in M.items()}
rows = []
for k, S in SC.items():
    h = hits(S); rows.append((k, h[:100], h[100:]))
# ghép: cộng hạng 2–3 phương pháp, chọn 25 phương pháp tốt nhất đoạn cũ để ghép, chấm đoạn mới
RK = {k: np.argsort(np.argsort(S, 1), 1) for k, S in SC.items()}
top_old = [k for k, a, b in sorted(rows, key=lambda x: -np.mean(x[1] >= 4))[:25]]
for r in (2, 3):
    for c in itertools.combinations(top_old, r):
        h = hits(sum(RK[k] for k in c)); rows.append(('Ghép ' + ' + '.join(c), h[:100], h[100:]))
f4 = lambda h: np.mean(h >= 4) * 100; f5 = lambda h: np.mean(h >= 5) * 100
print(f'## {g.upper()} — quét {len(rows)} phương pháp chọn pool 25 (≥4 số)\n')
a = np.array([[f4(x[1]), f4(x[2])] for x in rows])
print(f'- Đơn lẻ: {len(M)} cách; ghép 2–3 cách: {len(rows) - len(M)}.')
print(f'- ≥4 số, 100 kỳ cũ: cao nhất {a[:,0].max():.0f}%, trung vị {np.median(a[:,0]):.0f}% · 100 kỳ gần: cao nhất {a[:,1].max():.0f}%, trung vị {np.median(a[:,1]):.0f}%')
best_old = max(rows, key=lambda x: f4(x[1]))
print(f'- Cách tốt nhất ở đoạn cũ ({best_old[0]}: {f4(best_old[1]):.0f}%) sang đoạn gần: {f4(best_old[2]):.0f}%')
print(f'- Số cách đạt ≥40% ở CẢ hai đoạn: {sum(min(x) >= 40 for x in a)} · ≥35%: {sum(min(x) >= 35 for x in a)}\n')
print('| Phương pháp (xếp theo đoạn kém hơn) | Cũ ≥4 · ≥5 | Gần ≥4 · ≥5 |\n|---|---|---|')
for k, h1, h2 in sorted(rows, key=lambda x: -min(f4(x[1]), f4(x[2])))[:25]:
    print(f'| {k} | {f4(h1):.0f}% · {f5(h1):.0f}% | {f4(h2):.0f}% · {f5(h2):.0f}% |')
