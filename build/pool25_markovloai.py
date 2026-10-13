"""Dùng Markov / hồi quy (bài FB) làm phép LOẠI trong Pool 25 Power (anh 13/10/2026).
Mỗi kỳ: Pool 25 (cách đã duyệt) → mỗi phương pháp chấm 25 số → bỏ c số điểm thấp nhất.
Chấm 100 kỳ gần (2 nửa 50·50): ≥4 số còn lại, TB trúng, tỉ lệ ra của số bị loại vs số giữ.
python3 build/pool25_markovloai.py"""
import json, os, numpy as np
B = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(B, 'pool25_power.py')).read(); src = src[:src.index('def lab(')]
g = {'__file__': os.path.join(B, 'pool25_power.py')}; exec(src, g)
R, T, pool = g['R'], g['T'], g['pool']
NB, W = 55, 200
X = np.zeros((T, NB), int)
for i, r in enumerate(R):
    for n in r: X[i, n - 1] = 1

def mk_chung(t, k):
    H = X[t - W:t]; cnt = {}
    for j in range(k, W):
        for n in range(NB):
            s = H[j - k:j, n].tobytes(); a = cnt.setdefault(s, [0, 0]); a[0] += H[j, n]; a[1] += 1
    out = np.full(NB, 6 / 55)
    for n in range(NB):
        a = cnt.get(H[W - k:W, n].tobytes())
        if a and a[1] >= 3: out[n] = (a[0] + 0.11) / (a[1] + 1)
    return out
def mk_rieng(t, k):
    H = X[t - W:t]; out = np.full(NB, 6 / 55)
    for n in range(NB):
        col = H[:, n]; s = col[W - k:].tobytes(); hit = tot = 0
        for j in range(k, W):
            if col[j - k:j].tobytes() == s: hit += col[j]; tot += 1
        if tot: out[n] = (hit + 0.11) / (tot + 1)
    return out
def hq(t, w):
    H = X[t - w:t]; c = H.cumsum(0); x = np.arange(w) - (w - 1) / 2
    return (x[:, None] * (c - c.mean(0))).sum(0) / (x ** 2).sum()

M = {**{f'Markov chung bậc {k}': (lambda t, k=k: mk_chung(t, k)) for k in (1, 2, 3, 5, 8, 10)},
     **{f'Markov từng số bậc {k}': (lambda t, k=k: mk_rieng(t, k)) for k in (3, 5, 10)},
     **{f'Hồi quy {w} kỳ': (lambda t, w=w: hq(t, w)) for w in (30, 50, 100)}}
TS = list(range(T - 100, T)); CS = (1, 2, 3, 5, 8, 10)
P = {t: pool(t) for t in TS}
S = {m: {t: f(t) for t in TS} for m, f in M.items()}

def cut(t, sc, c):                       # bỏ c số trong pool có điểm thấp nhất (hoà: giữ thứ tự pool)
    p = P[t]; o = sorted(range(25), key=lambda i: (sc[p[i] - 1], -i))
    bo = {p[i] for i in o[:c]}; return [n for n in p if n not in bo], bo
def rank_in_pool(t, sc):                # hạng 0..24 trong pool (0 = thấp nhất)
    p = P[t]; o = sorted(range(25), key=lambda i: (sc[p[i] - 1], -i)); r = {}
    for k, i in enumerate(o): r[p[i]] = k
    return r
def vote(t, names, c):                  # nhiều phương pháp: cộng hạng trong pool → bỏ c số thấp nhất
    tot = {n: 0 for n in P[t]}
    for m in names:
        for n, k in rank_in_pool(t, S[m][t]).items(): tot[n] += k
    sc = np.zeros(NB)
    for n, v in tot.items(): sc[n - 1] = v
    return cut(t, sc, c)

def danh(fn):
    out = {}
    for c in CS:
        h, bh, bn = [], 0, 0
        for t in TS:
            keep, bo = fn(t, c); h.append(len(R[t] & set(keep))); bh += len(R[t] & bo); bn += len(bo)
        h = np.array(h)
        out[c] = dict(g4=(h >= 4).mean() * 100, n1=(h[:50] >= 4).mean() * 100, n2=(h[50:] >= 4).mean() * 100,
                      g3=(h >= 3).mean() * 100, tb=h.mean(), bo=100 * bh / bn)
    return out
base = np.array([len(R[t] & set(P[t])) for t in TS])
KQ = {'_goc': dict(g4=(base >= 4).mean() * 100, n1=(base[:50] >= 4).mean() * 100, n2=(base[50:] >= 4).mean() * 100,
                   g3=(base >= 3).mean() * 100, tb=base.mean(), giu=100 * base.sum() / 2500)}
for m in M: KQ[m] = danh(lambda t, c, m=m: cut(t, S[m][t], c))
KQ['Gộp tất cả (cộng hạng)'] = danh(lambda t, c: vote(t, list(M), c))
KQ['Gộp Markov chung 1–10'] = danh(lambda t, c: vote(t, [m for m in M if 'chung' in m], c))
KQ['Gộp Markov 3+5 + hồi quy 50'] = danh(lambda t, c: vote(t, ['Markov chung bậc 3', 'Markov chung bậc 5', 'Hồi quy 50 kỳ'], c))
json.dump(KQ, open(os.path.join(B, 'pool25_markovloai.json'), 'w'), ensure_ascii=False, default=float)
b = KQ['_goc']; print(f"GỐC pool 25: ≥4 {b['g4']:.0f}% ({b['n1']:.0f}·{b['n2']:.0f}) ≥3 {b['g3']:.0f}% TB {b['tb']:.2f} số giữ ra {b['giu']:.1f}%")
for m, v in KQ.items():
    if m == '_goc': continue
    print(m); [print(f"  bỏ {c:2d} (còn {25-c}): ≥4 {d['g4']:.0f}% ({d['n1']:.0f}·{d['n2']:.0f}) ≥3 {d['g3']:.0f}% TB {d['tb']:.2f} | số bị loại ra {d['bo']:.1f}%") for c, d in v.items()]
