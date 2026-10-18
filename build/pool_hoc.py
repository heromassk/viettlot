#!/usr/bin/env python3
"""Cải thiện pool để tăng % kỳ có ≥4 số về nằm trong pool (anh, 13/10/2026). Thử nhiều cách ghép mọi tín hiệu app có.
  python build/kiemtra_app.py 400      # (khi dữ liệu đổi) lấy 16 PP pool + 20 PP tâm linh từ code app
  python build/pool_hoc.py power|mega|loto
Mỗi kỳ t chỉ dùng dữ liệu TRƯỚC t (cả đặc trưng lẫn phần học) → số liệu 100 / 200 kỳ gần là chấm trên kỳ chưa thấy.
Đặc trưng mỗi số: luật sổ (theodoi RULES + CLAIMS), tín hiệu goiy.py, 16 PP pool app (thứ hạng), 20 PP tâm linh + tổng phiếu,
Markov trễ 1–3 kỳ, Markov bậc 2–3, độ vắng, số lần ra 5/10/20/100 kỳ."""
import argparse, json, os, sys, time
from itertools import product
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingClassifier
B = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, B)
ap = argparse.ArgumentParser(); ap.add_argument('game', choices=('power', 'mega', 'loto'))
ap.add_argument('--json'); A = ap.parse_args(); GAME = A.game
_src = open(os.path.join(B, 'goiy.py'), encoding='utf-8').read(); _argv = sys.argv; sys.argv = ['goiy.py', GAME]
GY = {'__file__': os.path.join(B, 'goiy.py'), '__name__': 'goiy_head'}
exec(compile(_src[:_src.index('# ---------- Đà tổng')], 'goiy.py', 'exec'), GY); sys.argv = _argv; GY['CUR'] = None
import theodoi as TD
key, NB, KB = TD.GM[GAME]; R, T = GY['R'], GY['T']; BQ = KB / NB
if GAME == 'loto': TD.SESS = GY['SES']
APP = json.load(open(os.path.join(B, 'kiemtra_app.json'), encoding='utf-8'))[GAME]
assert APP['L'] == T, 'kiemtra_app.json cũ → chạy lại kiemtra_app.py'
W0 = len(APP['dates']); T0 = T - W0; TEST = 200; KV = int(NB * 0.3 + 0.5)

# ---- ~300 phương pháp của app chính index.html (tập số từng kỳ nén sẵn trong file) ----
import re as _re, base64 as _b64, gzip as _gz
def load_index():
    html = open(os.path.join(os.path.dirname(B), 'index.html'), encoding='utf-8').read()
    m = _re.search(r'<script id="data-%s" type="application/json">(.*?)</script>' % key, html, _re.S)
    d = json.loads(m.group(1)); meta = d['meta']; Wd = meta.get('words', 2)
    U = np.frombuffer(_gz.decompress(_b64.b64decode(d['b64'])), dtype='<u4').reshape(len(meta['methods']), meta['L'] + meta['ND'], Wd)
    assert meta['L'] == T, f'index.html có {meta["L"]} kỳ, dữ liệu có {T}'
    bit = np.arange(32, dtype=np.uint32)
    lo = ((U[:, :, 0:1] >> bit) & 1).astype(np.int8); hi = ((U[:, :, 1:2] >> bit) & 1).astype(np.int8)
    S = np.concatenate([lo, hi], 2)[:, :, :NB]          # [phương pháp, kỳ, số]
    return [x['n'] for x in meta['methods']], S
IXN, IXS = load_index() if os.path.exists(os.path.join(os.path.dirname(B), 'index.html')) else ([], None)   # index.html đã xoá 14/10/2026

def markov_lag(t, k, W):
    sc = np.zeros(NB + 1); cx = np.zeros(NB + 1); M = np.zeros((NB + 1, NB + 1))
    for u in range(max(k, t - W), t):
        for x in R[u - k]:
            cx[x] += 1
            for n in R[u]: M[x, n] += 1
    for x in R[t - k]:
        if cx[x]: sc += M[x] / cx[x]
    return sc[1:]

def markov_bac(t, k, W):
    cur = set(product(*[sorted(R[t - k + i]) for i in range(k)])); c = {}; Tn = {}
    for u in range(max(k, t - W), t):
        for tup in product(*[sorted(R[u - k + i]) for i in range(k)]):
            if tup in cur:
                c[tup] = c.get(tup, 0) + 1
                for n in R[u]: Tn[(tup, n)] = Tn.get((tup, n), 0) + 1
    sc = np.zeros(NB)
    for (tup, n), v in Tn.items(): sc[n - 1] += v / c[tup]
    return sc

def rank01(v):
    o = np.argsort(-v, kind='stable'); r = np.empty(len(v)); r[o] = 1 - np.arange(len(v)) / (len(v) - 1); return r

NAMES = []; BIN = []
def feats(t):
    a = t - T0; cols = []; nm = []; isb = []
    c = TD.ctx(R, NB, t)
    def setcol(name, st, b=True):
        v = np.zeros(NB)
        for n in st:
            if 1 <= n <= NB: v[n - 1] = 1
        cols.append(v); nm.append(name); isb.append(b)
    for i, l, f in TD.RULES: setcol('so_' + i, f(R, t, c))
    for i, l, f in TD.CLAIMS: setcol('so_' + i, f(R, t, c, NB, KB)[1])
    fg, s = GY['signals'](t)
    for k in ('hot', 'ke', 'de', 'kho', 'vang', 'chuyen', 'phien', 'chin', 'g610', 'duoi', 'lap', 'tuan', 'ben', 'it100', 'lien2', 'lt3', 'zprev', 'tx15', 'vang1', 'nong35', 'thua'):
        if k in s: setcol('gy_' + k, s[k])
    for i, x in APP['pm'].items():
        o = x['ord'][a]; v = np.zeros(NB)
        if o:
            for p, n in enumerate(o): v[n - 1] = 1 - p / (NB - 1)
        cols.append(v); nm.append('pm_' + i); isb.append(False)
    vt = np.zeros(NB)
    for x in APP['kx']:
        ns = x['nums'][a] or []
        setcol('tl_' + x['id'], ns)
        for n in set(ns):
            if 1 <= n <= NB: vt[n - 1] += 1
    cols.append(vt / 20); nm.append('tl_phieu'); isb.append(False)
    for j, n2 in enumerate(IXN):
        cols.append(IXS[j, t].astype(float)); nm.append('ix_' + n2); isb.append(True)
    for k, W in ((1, 100), (2, 100), (3, 100), (1, 50)):
        cols.append(rank01(markov_lag(t, k, W))); nm.append(f'mk_tre{k}_{W}'); isb.append(False)
    for k, W in ((2, 50), (2, 100), (3, 50)):
        cols.append(rank01(markov_bac(t, k, W))); nm.append(f'mk_bac{k}_{W}'); isb.append(False)
    g = np.array([c['gap'][n] for n in range(1, NB + 1)], float)
    for nm2, v in (('gap', np.minimum(g, 40) / 40), ('c5', np.array([c['c5'][n] for n in range(1, NB + 1)]) / 5),
                   ('c10', np.array([c['c10'][n] for n in range(1, NB + 1)]) / 10), ('c20', np.array([c['c20'][n] for n in range(1, NB + 1)]) / 20),
                   ('c100', np.array([c['c100'][n] for n in range(1, NB + 1)]) / (100 * BQ))):
        cols.append(v); nm.append(nm2); isb.append(False)
    if not NAMES: NAMES.extend(nm); BIN.extend(isb)
    assert nm == NAMES, 'đặc trưng lệch giữa các kỳ'
    return np.stack(cols, 1)

t0 = time.time()
X = {t: feats(t) for t in range(T0 + 0, T + 1)}         # T: kỳ tới
Y = {t: np.array([n in R[t] for n in range(1, NB + 1)], float) for t in range(T0, T)}
BASE = {t: GY['pool_of'](GY['score'](*GY['signals'](t)), GY['signals'](t)[1], NB) for t in range(T - TEST, T + 1)}
print(f'{key}: {len(NAMES)} đặc trưng, {len(X)} kỳ, dựng {time.time() - t0:.0f}s', file=sys.stderr)
F = len(NAMES); BI = np.array(BIN)

def order_from_score(sc): return [int(i) + 1 for i in np.argsort(-sc, kind='stable')]

# ---- các cách xếp hạng (mỗi hàm: t → thứ tự số, chỉ dùng kỳ < t) ----
def m_base(t):
    rk = BASE[t]; rest = [n for n in range(1, NB + 1) if n not in rk]; return rk + rest

def lift_w(t, W):
    """hệ số ra của từng đặc trưng nhị phân trong W kỳ trước; chỉ giữ đặc trưng nghiêng CÙNG CHIỀU ở 2 nửa."""
    h1 = range(t - W, t - W // 2); h2 = range(t - W // 2, t)
    def lift(ts):
        num = np.zeros(F); den = np.zeros(F)
        for u in ts: num += Y[u] @ X[u]; den += X[u].sum(0)
        return np.where(den > 0, num / np.maximum(den, 1e-9) / BQ, 1.0), den
    l1, d1 = lift(h1); l2, d2 = lift(h2); lA, dA = lift(range(t - W, t))
    ok = BI & (np.sign(l1 - 1) == np.sign(l2 - 1)) & (dA * BQ >= 10)
    return np.where(ok, lA - 1, 0.0)
CACHE_W = {}
def m_lift(W):
    def f(t):
        k = (W, t // 5 * 5)
        if k not in CACHE_W: CACHE_W[k] = lift_w(t, W)
        return order_from_score(X[t] @ CACHE_W[k])
    return f

MODELS = {}
def m_fit(kind, W, every):
    def f(t):
        k = (kind, W, (t - (T - TEST)) // every)
        if k not in MODELS:
            ts = range(t - W, t)
            Xt = np.concatenate([X[u] for u in ts]); yt = np.concatenate([Y[u] for u in ts])
            if kind == 'lr':
                mu, sd = Xt.mean(0), Xt.std(0) + 1e-6
                m = LogisticRegression(C=0.05, max_iter=500).fit((Xt - mu) / sd, yt); MODELS[k] = ('lr', m, mu, sd)
            else:
                m = HistGradientBoostingClassifier(max_depth=3, max_iter=120, learning_rate=0.05, l2_regularization=1.0, min_samples_leaf=40, random_state=0).fit(Xt, yt)
                MODELS[k] = ('gb', m, None, None)
        kd, m, mu, sd = MODELS[k]
        p = m.predict_proba((X[t] - mu) / sd if kd == 'lr' else X[t])[:, 1]
        return order_from_score(p)
    return f

def m_col(name):
    j = NAMES.index(name); return lambda t: order_from_score(X[t][:, j] + 1e-6 * np.arange(NB, 0, -1))

def m_ens(fs):
    def f(t):
        sc = np.zeros(NB)
        for g in fs:
            o = g(t)
            for p, n in enumerate(o): sc[n - 1] += 1 - p / (NB - 1)
        return order_from_score(sc)
    return f

IXJ = [j for j, n2 in enumerate(NAMES) if n2.startswith('ix_')]
def m_top(nm_top=50, W=100, weighted=False):
    def f(t):
        num = np.zeros(F); den = np.zeros(F)
        for u in range(t - W, t): num += Y[u] @ X[u]; den += X[u].sum(0)
        rate = np.where(den * BQ >= 5, num / np.maximum(den, 1e-9) / BQ, 0)
        top = sorted(IXJ, key=lambda j: -rate[j])[:nm_top]
        w = np.zeros(F)
        for j in top: w[j] = (rate[j] - 1) if weighted else 1
        return order_from_score(X[t] @ w + 1e-6 * np.arange(NB, 0, -1))
    return f

CAND = {
    'Pool app đang dùng': m_base,
    'Điểm theo tỉ lệ ra 100 kỳ gần': m_lift(100),
    'Điểm theo tỉ lệ ra 200 kỳ gần': m_lift(200),
    'Hồi quy logistic học 100 kỳ': m_fit('lr', 100, 5),
    'Hồi quy logistic học 200 kỳ': m_fit('lr', 200, 5),
    'Cây tăng cường học 200 kỳ': m_fit('gb', 200, 10),
    'Markov bậc 2 (học 50 kỳ)': m_col('mk_bac2_50'),
    'Markov bậc 2 (học 100 kỳ)': m_col('mk_bac2_100'),
    'Markov bậc 3 (học 50 kỳ)': m_col('mk_bac3_50'),
    'App chính: top 50 PP (100 kỳ) bầu phiếu': m_top(50, 100),
    'App chính: top 100 PP (100 kỳ) bầu phiếu': m_top(100, 100),
    'Top 50 PP (200 kỳ), phiếu theo tỉ lệ ra': m_top(50, 200, True),
}
CAND['Gộp: app + logistic 200 + Markov bậc 2'] = m_ens([CAND['Pool app đang dùng'], CAND['Hồi quy logistic học 200 kỳ'], CAND['Markov bậc 2 (học 50 kỳ)']])
CAND['Gộp: app + tỉ lệ ra 200 + Markov bậc 2'] = m_ens([CAND['Pool app đang dùng'], CAND['Điểm theo tỉ lệ ra 200 kỳ gần'], CAND['Markov bậc 2 (học 50 kỳ)']])
CAND['Gộp: app + top 50 PP + Markov bậc 2'] = m_ens([CAND['Pool app đang dùng'], CAND['App chính: top 50 PP (100 kỳ) bầu phiếu'], CAND['Markov bậc 2 (học 50 kỳ)']])
CAND['Gộp tất cả cách trên'] = m_ens([CAND[k] for k in list(CAND)])

SIZES = (10, 12, 15, 18, 20)
TS = range(T - TEST, T)
ORD = {}
for nm, f in CAND.items():
    t1 = time.time(); ORD[nm] = {t: f(t) for t in list(TS) + [T]}; print(f'  {nm}: {time.time() - t1:.0f}s', file=sys.stderr)
# chọn động: mỗi kỳ dùng cách có % kỳ ≥3 số trong pool 18 cao nhất ở 50 kỳ trước (chỉ các kỳ đã chấm, không nhìn tương lai)
names = list(CAND)
def dyn(t, K=18, L=50):
    best = max(names, key=lambda nm: sum(len(set(ORD[nm][u][:K]) & R[u]) >= 3 for u in range(max(T - TEST, t - L), t)) if t > T - TEST + 10 else (nm == 'Pool app đang dùng'))
    return ORD[best][t]
ORD['Tự chọn cách tốt nhất 50 kỳ trước'] = {t: dyn(t) for t in list(TS) + [T]}

def st(o, ts, K):
    hs = [len(set(o[t][:K]) & R[t]) for t in ts]; n = len(hs)
    return [sum(h >= j for h in hs) / n * 100 for j in (2, 3, 4, 5)]
OUT = {}
L = [f'## {key} — tăng % kỳ có ≥4 số về trong pool (chạy tiến, mọi số liệu là kỳ chưa thấy; dữ liệu đến {GY["D"]["dates"][-1]})\n',
     f'{F} đặc trưng/số: luật sổ, tín hiệu gợi ý, 16 PP pool app, 20 PP tâm linh + tổng phiếu, Markov trễ 1–3 & bậc 2–3, vắng, số lần ra.\n']
for K in SIZES:
    L.append(f'\n### Pool {K} — % kỳ về ≥3 / ≥4 / ≥5 số trong pool (100 kỳ gần · 200 kỳ gần)\n')
    L.append('| Cách | ≥3 số | **≥4 số** | ≥5 số |\n|---|---|---|---|')
    rows = []
    for nm, o in ORD.items():
        a, b = st(o, range(T - 100, T), K), st(o, TS, K); rows.append((b[2], nm, a, b))
        OUT.setdefault(nm, {})[K] = dict(r100=a, r200=b)
    for _, nm, a, b in sorted(rows, key=lambda x: (-x[0], -x[3][1])):
        L.append(f"| {nm} | {a[1]:.0f}% · {b[1]:.0f}% | **{a[2]:.0f}% · {b[2]:.0f}%** | {a[3]:.0f}% · {b[3]:.1f}% |")
# chấm riêng ~300 PP app chính: tỉ lệ ra so với BQ, 100 kỳ gần / 100 kỳ trước
def lf_col(j, ts):
    h = sum(X[u][:, j] @ Y[u] for u in ts); z = sum(X[u][:, j].sum() for u in ts); return (h / z / BQ if z else None), z
IXR = []
for j in IXJ:
    a, za = lf_col(j, range(T - 100, T)); b, zb = lf_col(j, range(T - 200, T - 100))
    ms = min(za, zb) * BQ < 10
    IXR.append((NAMES[j][3:], a, b, za / 100, ms, (not ms) and a > 1 and b > 1))
nd = sum(r[5] for r in IXR); nms = sum(r[4] for r in IXR)
L.append(f'\n### {len(IXR)} phương pháp của app chính (index.html) — tỉ lệ ra so với BQ\n')
L.append(f'- Đạt (ra nhiều hơn BQ ở cả 100 kỳ gần và 100 kỳ trước): **{nd}** · ít mẫu (chọn quá ít số): {nms} · không đạt: {len(IXR) - nd - nms}')
L.append('- Top đạt: ' + ', '.join(f'{n} ×{a:.2f}/×{b:.2f} ({z:.1f} số/kỳ)' for n, a, b, z, ms, ok in sorted([r for r in IXR if r[5]], key=lambda r: -(r[1] + r[2]))[:15]))
txt = '\n'.join(L) + '\n'; print(txt)
if A.json: json.dump(dict(game=GAME, out=OUT, next={nm: o[T] for nm, o in ORD.items()}, feats=NAMES), open(A.json, 'w', encoding='utf-8'), ensure_ascii=False)
