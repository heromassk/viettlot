"""Nghiên cứu sâu pool 25 (anh, 10/10/2026): tăng tỉ lệ kỳ trúng ≥4, ≥5 số trong pool 25.
Học trên 100 kỳ cũ (T-200..T-101), kiểm trên 100 kỳ mới (T-100..T-1) — chỉ dùng ≤200 kỳ.
Dùng: python3 build/pool25_sau.py mega|power"""
import json, sys, os, datetime as dt
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
g = sys.argv[1]
KEY, NB = {'mega': ('mega645', 45), 'power': ('power655', 55)}[g]
OTH = {'mega': 'power655', 'power': 'mega645'}[g]
A = json.load(open(os.path.join(HERE, 'all_data.json')))
D = A[KEY]; R = [set(r) for r in D['res']]; T = len(R)
dd = lambda s: dt.datetime.strptime(s[:10], '%d/%m/%Y')
OD = [(dd(d), set(r)) for d, r in zip(A[OTH]['dates'], A[OTH]['res'])]
DT = [dd(d) for d in D['dates']]
REC = json.load(open(f'/tmp/claude-0/r25_{g}.json'))   # thứ hạng cách hiện tại 200 kỳ
lon = lambda n: int(f'{n:02d}'[::-1])

def feats(t):
    X = []
    last = R[t - 1]
    oth = [s for e, s in OD if e < DT[t]]; oth = oth[-1] if oth else set()
    rk = REC[t - (T - 200)]['rk'] if t >= T - 200 else []
    for n in range(1, NB + 1):
        g_ = 0
        while g_ < 150 and n not in R[t - 1 - g_]: g_ += 1
        c = lambda w: sum(n in R[t - j] for j in range(1, w + 1))
        k1 = sum((n - 1 in R[t - j]) + (n + 1 in R[t - j]) for j in range(1, 4))
        k13 = sum(sum((n + s * k) in R[t - j] for s in (1, -1) for k in (13, 14)) for j in range(1, 4))
        ln = sum(lon(x) == n and lon(x) != x for j in range(1, 4) for x in R[t - j])
        f = [g_ == 0, g_ == 1, g_ == 2, 3 <= g_ <= 5, 6 <= g_ <= 10, 11 <= g_ <= 15, 16 <= g_ <= 25, g_ > 25,
             c(5) / 1, c(10) / 2, c(20) / 3, c(50) / 7, c(100) / 13, c(10) / 2 - c(50) / 7,
             n in last and n in R[t - 2], n in last and n in R[t - 3], n == max(last), n == min(last),
             any(abs(n - x) == 1 for x in last), k1 / 3, k13 / 3, ln, n in oth,
             n % 10 in {x % 10 for x in last} and n not in last, n % 11 == 0,
             (25 - rk.index(n)) / 25 if n in rk else 0, n in rk[:12]]
        f += [n // 10 == d for d in range(NB // 10 + 1)]
        X.append(f)
    return np.array(X, float)

ts = list(range(T - 200, T))
X = {t: feats(t) for t in ts}
Y = {t: np.array([n in R[t] for n in range(1, NB + 1)], float) for t in ts}
def fit(tr, l2=1.0, it=300, lr=0.1):
    Xa = np.vstack([X[t] for t in tr]); ya = np.concatenate([Y[t] for t in tr])
    mu, sd = Xa.mean(0), Xa.std(0) + 1e-9; Z = (Xa - mu) / sd
    w = np.zeros(Z.shape[1]); b = 0.0
    for _ in range(it):
        p = 1 / (1 + np.exp(-(Z @ w + b))); e = p - ya
        w -= lr * (Z.T @ e / len(ya) + l2 * w / len(ya)); b -= lr * e.mean()
    return w, b, mu, sd
def hits(model, tt, K=25):
    w, b, mu, sd = model; out = []
    for t in tt:
        s = ((X[t] - mu) / sd) @ w + b; top = np.argsort(-s)[:K]
        out.append(int(Y[t][top].sum()))
    return out
def rep(name, h):
    h = np.array(h); return f'{name}: TB {h.mean():.2f} ≥3 {np.mean(h>=3)*100:.0f}% ≥4 {np.mean(h>=4)*100:.0f}% ≥5 {np.mean(h>=5)*100:.0f}%'
tr, te = ts[:100], ts[100:]
base = [len(set(REC[t - (T - 200)]['rk'][:25]) & R[t]) for t in ts]
print(f'## {g.upper()} pool 25 — học 100 kỳ cũ, kiểm 100 kỳ mới\n')
print(rep('Cách hiện tại, 100 kỳ cũ', base[:100])); print(rep('Cách hiện tại, 100 kỳ mới', base[100:]))
for l2 in (1, 30, 300):
    m = fit(tr, l2=l2)
    print(f'l2={l2}: ' + rep('đã học', hits(m, tr)) + ' | ' + rep('chưa học', hits(m, te)))
# học cuốn chiếu: mỗi kỳ mới học lại trên 100 kỳ ngay trước
wf = []
for i, t in enumerate(te):
    if i % 10 == 0: m = fit(ts[i:i + 100], l2=30)
    wf += hits(m, [t])
print(rep('Cuốn chiếu (học lại mỗi 10 kỳ)', wf))
m = fit(ts[100:], l2=30)
names = ['g0','g1','g2','g3-5','g6-10','g11-15','g16-25','g26+','c5','c10','c20','c50','c100','đà10-50','lien2','lt3','maxPrev','minPrev','kề±1','±1·3kỳ','±13/14·3kỳ','lộn3kỳ','chéo game','cùng đuôi','kép','hạng app','top12 app'] + [f'chục{d}' for d in range(NB // 10 + 1)]
print('\nTrọng số (học 100 kỳ mới):', ', '.join(f'{a} {b:+.2f}' for a, b in sorted(zip(names, m[0]), key=lambda x: -abs(x[1]))[:12]))
