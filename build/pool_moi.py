#!/usr/bin/env python3
"""Pool mới (anh, 14/10/2026): gộp phương pháp mới tra được (連休回数, tỉ lệ vắng/vắng TB, KNN theo vắng, HMM 2 trạng thái, 斜连, 隔号)
+ Markov kiểu bộ số (bậc 1–4, trễ 2–3) + Markov chuỗi ra/vắng bậc 1–10 + luật loại trong sổ + điểm pool hiện tại.
  python build/pool_moi.py power|mega|loto [--json file]
CHẠY TIẾN hoàn toàn: ở mỗi kỳ t, máy chỉ nhìn 100 kỳ trước t để
  1) chọn LUẬT LOẠI: luật đúng ≥70% ở khung 50 & 100 và số bị loại ra ≤ TB; thêm dần từ luật có số bị loại ra ít nhất,
     miễn cả nhóm loại gộp vẫn đúng ≥70% ở khung 50 & 100 → bỏ hẳn các số đó;
  2) chọn PHƯƠNG PHÁP CỘNG ĐIỂM: top 15 của phương pháp ra > TB ở cả khung 50 & 100; trọng số = (tỉ lệ ra 100 kỳ ÷ TB − 1);
  3) pool K = K số điểm cao nhất còn lại.
Chấm pool ở 100 kỳ gần nhất, báo 4 khung 10/20/50/100 kỳ; so với pool app đang dùng (goiy.py) chạy cùng cách."""
import argparse, json, os, sys, time
from itertools import product
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
B = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, B)
ap = argparse.ArgumentParser(); ap.add_argument('game', choices=('power', 'mega', 'loto')); ap.add_argument('--json'); ap.add_argument('--tung', action='store_true'); ap.add_argument('--hoc', action='store_true'); ap.add_argument('--hoc2', action='store_true'); ap.add_argument('--ve', action='store_true'); A = ap.parse_args()
if A.hoc2: A.hoc = True
GAME = A.game
_src = open(os.path.join(B, 'goiy.py'), encoding='utf-8').read(); _argv = sys.argv; sys.argv = ['goiy.py', GAME]
GY = {'__file__': os.path.join(B, 'goiy.py'), '__name__': 'goiy_head'}
exec(compile(_src[:_src.index('# ---------- Đà tổng')], 'goiy.py', 'exec'), GY); sys.argv = _argv; GY['CUR'] = None
import theodoi as TD
key, NB, KB = TD.GM[GAME]; R = GY['R']; T = GY['T']; RL = [sorted(r) for r in R]; P0 = KB / NB
if GAME == 'loto': TD.SESS = GY['SES']
TEST = 100; SEL = 200 if '--hoc2' in sys.argv else 100; T0 = T - TEST - SEL            # đặc trưng từ T0 (kỳ đầu cần chọn phương pháp) tới T (kỳ tới)
WS = (50, 100, 200) if GAME == 'loto' else (50, 100)
Y = np.array([[n in R[t] for n in range(1, NB + 1)] for t in range(T)], dtype=np.int8)          # [kỳ, số]

# ---- độ vắng: G[t, n] = số kỳ vắng của số n tính tới trước kỳ t; thống kê khoảng nghỉ đã qua (cho KNN, tỉ lệ vắng) ----
G = np.zeros((T + 1, NB), dtype=np.int32); GS = np.zeros((T + 1, NB, 5))            # [vắng hiện tại, TB, max, min, độ lệch]
for n in range(NB):
    g = 0; gaps = []; s = s2 = 0.0; mx = 0; mn = 999
    for t in range(T + 1):
        G[t, n] = g
        k = len(gaps)
        GS[t, n] = (g, s / k if k else g, max(mx, g), mn if k else g, (np.sqrt(max(0, s2 / k - (s / k) ** 2)) if k else 0))
        if t < T:
            if Y[t, n]:
                if t: gaps.append(g); s += g; s2 += g * g; mx = max(mx, g); mn = min(mn, g)
                g = 0
            else: g += 1
HB = np.zeros((T + 1, NB), dtype=np.int32)                     # 10 kỳ gần nhất của từng số (bit 0 = kỳ t−1)
for t in range(1, T + 1): HB[t] = ((HB[t - 1] << 1) | Y[t - 1]) & 1023

def rank01(v):
    o = np.argsort(-v, kind='stable'); r = np.empty(NB); r[o] = 1 - np.arange(NB) / (NB - 1); return r

# ---- các phương pháp cho ĐIỂM (mỗi hàm: t → vector điểm NB số, chỉ dùng dữ liệu trước t) ----
def mk_bac(t, k, W):
    cur = set(product(*[RL[t - k + i] for i in range(k)])); c = {}; tn = {}
    for u in range(max(k, t - W), t):
        for tup in product(*[RL[u - k + i] for i in range(k)]):
            if tup in cur:
                c[tup] = c.get(tup, 0) + 1
                for n in RL[u]: tn[(tup, n)] = tn.get((tup, n), 0) + 1
    sc = np.zeros(NB)
    for (tup, n), v in tn.items(): sc[n - 1] += v / c[tup]
    return sc
def mk_tre(t, k, W):
    sc = np.zeros(NB); cx = np.zeros(NB + 1); M = np.zeros((NB + 1, NB))
    for u in range(max(k, t - W), t):
        for x in RL[u - k]:
            cx[x] += 1; M[x] += Y[u]
    for x in RL[t - k]:
        if cx[x]: sc += M[x] / cx[x]
    return sc
def chuoi(t, k, W, rieng):
    m = (1 << k) - 1; st = HB[t] & m; lo = max(k, t - W); H = HB[lo:t] & m; Yw = Y[lo:t]; a = 3.0
    if rieng:
        eq = H == st; return ((eq & (Yw == 1)).sum(0) + a * P0) / (eq.sum(0) + a)
    c = np.bincount(H.ravel(), minlength=1024); h = np.bincount(H.ravel(), weights=Yw.ravel(), minlength=1024)
    return (h[st] + a * P0) / (c[st] + a)
def lienhuu(t, rieng, W=100):         # 連休回数: số đã vắng đúng g kỳ → lịch sử ra ngay kỳ kế
    g = np.minimum(G[t], 60); a = 3.0
    if rieng:
        Gs = np.minimum(G[:t], 60); eq = Gs == g; return ((eq & (Y[:t] == 1)).sum(0) + a * P0) / (eq.sum(0) + a)
    lo = max(0, t - W); Gw = np.minimum(G[lo:t], 60).ravel(); Yw = Y[lo:t].ravel()
    c = np.bincount(Gw, minlength=61); h = np.bincount(Gw, weights=Yw, minlength=61)
    return (h[g] + a * P0) / (c[g] + a)
def tile_vang(t): return GS[t, :, 0] / np.maximum(GS[t, :, 1], 1)        # vắng hiện tại / vắng TB của chính số
def knn(t, W=100):                                                       # KNN 5 đặc trưng vắng (cnblogs)
    lo = t - W; Xtr = GS[lo:t].reshape(-1, 5); ytr = Y[lo:t].ravel()
    sd = Xtr.std(0) + 1e-9; m = KNeighborsClassifier(n_neighbors=9).fit(Xtr / sd, ytr)
    return m.predict_proba(GS[t] / sd)[:, list(m.classes_).index(1)] if 1 in m.classes_ else np.zeros(NB)
def hmm(t, W=100, it=15):                                                # HMM 2 trạng thái (nóng/nguội) cho từng số, Bernoulli
    O = Y[t - W:t].T.astype(float); S = 2
    A_ = np.tile(np.array([[0.9, 0.1], [0.1, 0.9]]), (NB, 1, 1)); E = np.tile(np.array([P0 * 0.6, P0 * 1.6]), (NB, 1)); pi = np.full((NB, S), 0.5)
    for _ in range(it):
        em = lambda o: np.where(o[:, None] == 1, E, 1 - E)
        al = np.zeros((NB, W, S)); be = np.ones((NB, W, S)); c = np.zeros((NB, W))
        a0 = pi * em(O[:, 0]); c[:, 0] = a0.sum(1); al[:, 0] = a0 / c[:, :1]
        for i in range(1, W):
            a1 = np.einsum('ns,nsr->nr', al[:, i - 1], A_) * em(O[:, i]); c[:, i] = a1.sum(1); al[:, i] = a1 / c[:, i:i + 1]
        for i in range(W - 2, -1, -1):
            be[:, i] = np.einsum('nsr,nr->ns', A_, em(O[:, i + 1]) * be[:, i + 1]) / c[:, i + 1:i + 2]
        ga = al * be; ga /= ga.sum(2, keepdims=True)
        xi = al[:, :-1, :, None] * A_[:, None] * (em_all := np.stack([em(O[:, i + 1]) for i in range(W - 1)], 1))[:, :, None, :] * be[:, 1:, None, :]
        xi /= xi.sum((2, 3), keepdims=True)
        pi = ga[:, 0]; A_ = xi.sum(1) / ga[:, :-1].sum(1)[:, :, None]
        E = np.clip((ga * O[:, :, None]).sum(1) / ga.sum(1), 1e-3, 0.999)
    return np.einsum('ns,nsr,nr->n', al[:, -1], A_, E)                  # P(ra kỳ t)
def xielian(t):                                                          # 斜连: a ở t−2, a±1 ở t−1 → a±2 ở t
    v = np.zeros(NB)
    for a in RL[t - 2]:
        for d in (1, -1):
            if a + d in R[t - 1] and 1 <= a + 2 * d <= NB: v[a + 2 * d - 1] = 1
    return v
def gehao(t):                                                            # 隔号: cách số kỳ trước đúng ±2
    v = np.zeros(NB)
    for a in RL[t - 1]:
        for d in (2, -2):
            if 1 <= a + d <= NB and a + d not in R[t - 1]: v[a + d - 1] = 1
    return v

SCO = {}
def addS(nm, f): SCO[nm] = f
addS('Pool app đang dùng (điểm goiy)', None)
for k in (1, 2, 3, 4):
    for W in (50, 100): addS(f'Markov bộ số bậc {k}, học {W}', lambda t, k=k, W=W: mk_bac(t, k, W))
for k in (2, 3):
    for W in (50, 100): addS(f'Markov trễ {k} kỳ, học {W}', lambda t, k=k, W=W: mk_tre(t, k, W))
for r in (False, True):
    for k in range(1, 11):
        for W in WS: addS(f'Chuỗi ra/vắng bậc {k}, {"riêng" if r else "chung"}, học {W}', lambda t, k=k, W=W, r=r: chuoi(t, k, W, r))
addS('連休回数 riêng từng số (cả lịch sử)', lambda t: lienhuu(t, True))
addS('連休回数 chung mọi số (100 kỳ)', lambda t: lienhuu(t, False))
addS('Tỉ lệ vắng/vắng TB (cao = đến hạn)', tile_vang)
addS('Tỉ lệ vắng/vắng TB (thấp = vừa ra)', lambda t: -tile_vang(t))
addS('KNN 5 đặc trưng vắng', knn)
addS('HMM 2 trạng thái nóng/nguội', hmm)
addS('斜连 số chéo', xielian)
addS('隔号 cách số kỳ trước ±2', gehao)

t0 = time.time()
TT = list(range(T0, T + 1))
SC = {nm: {} for nm in SCO}
for t in TT:
    if t < T: pass
    rk = GY['pool_of'](GY['score'](*GY['signals'](t)), GY['signals'](t)[1], NB)
    v = np.zeros(NB); v[np.array(rk) - 1] = NB - np.arange(len(rk)); SC['Pool app đang dùng (điểm goiy)'][t] = v
    for nm, f in SCO.items():
        if f is not None: SC[nm][t] = np.asarray(f(t), float)
print(f'{key}: {len(SCO)} phương pháp điểm, dựng {time.time() - t0:.0f}s', file=sys.stderr)

# ---- các nhóm LOẠI: luật sổ + Markov điểm 0 + chuỗi/連休 điểm thấp (≤60% TB, đã gặp đủ mẫu) ----
LO = {}
for i, l, f in TD.RULES:
    LO['Luật: ' + l] = {t: {n - 1 for n in f(R, t, TD.ctx(R, NB, t))} for t in TT}
for nm in [x for x in SCO if x.startswith('Markov')]:
    LO[nm + ' — điểm 0'] = {t: set(np.nonzero(SC[nm][t] == 0)[0]) for t in TT}
for nm in [x for x in SCO if x.startswith('Chuỗi') or x.startswith('連休')]:
    LO[nm + ' — điểm ≤60% TB'] = {t: set(np.nonzero(SC[nm][t] <= 0.6 * P0)[0]) for t in TT}
LO['KNN — xác suất 0'] = {t: set(np.nonzero(SC['KNN 5 đặc trưng vắng'][t] == 0)[0]) for t in TT}
LO['HMM — xác suất ≤60% TB'] = {t: set(np.nonzero(SC['HMM 2 trạng thái nóng/nguội'][t] <= 0.6 * P0)[0]) for t in TT}

# ---- thống kê theo kỳ để chọn phương pháp chạy tiến ----
RS = {t: set(np.nonzero(Y[t])[0]) for t in range(T0, T)}
TOPS = {nm: {t: set(np.argsort(-SC[nm][t], kind='stable')[:15]) for t in TT} for nm in SCO}
def sel(t, NG=70):
    """chọn luật loại + phương pháp cộng điểm, chỉ nhìn 100 kỳ trước t"""
    w100, w50 = range(t - 100, t), range(t - 50, t)
    cand = []
    for nm, S in LO.items():
        z = sum(len(S[u]) for u in w100)
        if z < 30: continue
        ok100 = sum(not (S[u] & RS[u]) for u in w100) / 100; ok50 = sum(not (S[u] & RS[u]) for u in w50) / 50
        ra = sum(len(S[u] & RS[u]) for u in w100) / z
        if ok100 >= 0.7 and ok50 >= 0.7 and ra <= P0: cand.append((ra, nm))
    hard = []; cur = {u: set() for u in w100}
    for ra, nm in sorted(cand):
        nxt = {u: cur[u] | LO[nm][u] for u in w100}
        if sum(not (nxt[u] & RS[u]) for u in w100) >= NG and sum(not (nxt[u] & RS[u]) for u in w50) >= NG / 2: hard.append(nm); cur = nxt
    wts = {}
    for nm in SCO:
        l100 = sum(len(TOPS[nm][u] & RS[u]) for u in w100) / (15 * 100) / P0
        l50 = sum(len(TOPS[nm][u] & RS[u]) for u in w50) / (15 * 50) / P0
        if l100 > 1 and l50 > 1: wts[nm] = l100 - 1
    return hard, wts
def pool_at(t, hard, wts):
    ex = set().union(*[LO[nm][t] for nm in hard]) if hard else set()
    sc = np.zeros(NB)
    for nm, w in wts.items(): sc += w * rank01(SC[nm][t])
    sc += 1e-6 * rank01(SC['Pool app đang dùng (điểm goiy)'][t])
    od = [int(i) for i in np.argsort(-sc, kind='stable') if i not in ex]
    return od, ex
SELS = {}; ODS = {}; EXS = {}
for t in range(T - TEST, T + 1):
    SELS[t] = sel(t); ODS[t], EXS[t] = pool_at(t, *SELS[t])
BASE = {t: [int(i) for i in np.argsort(-SC['Pool app đang dùng (điểm goiy)'][t], kind='stable')] for t in range(T - TEST, T + 1)}
# (C) pool đang dùng + bỏ thêm nhóm loại hẳn (≥70%) · (D) như C nhưng nhóm loại phải đúng ≥80%
EX80 = {t: (set().union(*[LO[nm][t] for nm in h]) if (h := sel(t, 80)[0]) else set()) for t in range(T - TEST, T + 1)}
CVAR = {t: [n for n in BASE[t] if n not in EXS[t]] for t in range(T - TEST, T + 1)}
DVAR = {t: [n for n in BASE[t] if n not in EX80[t]] for t in range(T - TEST, T + 1)}

def stat(OD, K, W):
    ts = range(T - W, T); hs = [len(set(OD[t][:K]) & RS[t]) for t in ts]
    return [sum(h >= j for h in hs) / W * 100 for j in (2, 3, 4)] + [sum(hs) / W]
pc = lambda v: f'{v:.0f}%'
L = [f'## {key} — pool mới (chạy tiến, tự chọn phương pháp theo 100 kỳ trước mỗi kỳ) so với pool đang dùng, đến {GY["D"]["dates"][-1]}\n']
exn = [len(EXS[t]) for t in range(T - TEST, T)]; exh = [len(EXS[t] & RS[t]) for t in range(T - TEST, T)]
e8n = [len(EX80[t]) for t in range(T - TEST, T)]; e8h = [len(EX80[t] & RS[t]) for t in range(T - TEST, T)]
L.append(f'Loại hẳn TB **{np.mean(exn):.1f} số/kỳ** (10 kỳ gần {np.mean(exn[-10:]):.1f}) · kỳ không loại nhầm số nào: '
         + ' / '.join(f"{sum(h == 0 for h in exh[-W:]) / W * 100:.0f}%" for W in (10, 20, 50, 100)) + ' (khung 10/20/50/100)\n')
L.append('| Pool | Cách | Kỳ ≥3 số: 10 / 20 / 50 / 100 kỳ | Kỳ ≥4 số: 10 / 20 / 50 / 100 kỳ | TB số trúng (100 kỳ) |\n|---|---|---|---|---|')
OUT = {}
for K in (10, 15, 18):
    for nm, OD in (('Pool mới (gộp hết)', ODS), ('(C) đang dùng + loại ≥70%', CVAR), ('(D) đang dùng + loại ≥80%', DVAR), ('Pool đang dùng', BASE)):
        s = {W: stat(OD, K, W) for W in (10, 20, 50, 100)}; OUT[f'{nm}|{K}'] = s
        L.append(f"| {K} | {nm} | {' / '.join(pc(s[W][1]) for W in (10, 20, 50, 100))} | {' / '.join(pc(s[W][2]) for W in (10, 20, 50, 100))} | {s[100][3]:.2f} |")
# phương pháp hay được chọn
from collections import Counter
ch = Counter(); cl = Counter()
for t in range(T - TEST, T):
    for nm in SELS[t][1]: ch[nm] += 1
    for nm in SELS[t][0]: cl[nm] += 1
L.append('\n**Luật loại được chọn nhiều nhất** (số kỳ/100): ' + ' · '.join(f'{nm} ({c})' for nm, c in cl.most_common(8)))
L.append('\n**Phương pháp cộng điểm được chọn nhiều nhất** (số kỳ/100): ' + ' · '.join(f'{nm} ({c})' for nm, c in ch.most_common(12)))
newm = ['連休回数 riêng từng số (cả lịch sử)', '連休回数 chung mọi số (100 kỳ)', 'Tỉ lệ vắng/vắng TB (cao = đến hạn)', 'Tỉ lệ vắng/vắng TB (thấp = vừa ra)', 'KNN 5 đặc trưng vắng', 'HMM 2 trạng thái nóng/nguội', '斜连 số chéo', '隔号 cách số kỳ trước ±2']
L.append('\n**Riêng các phương pháp mới tra được** — top 15 ra mỗi số (10 / 20 / 50 / 100 kỳ), được chọn bao nhiêu kỳ:')
for nm in newm:
    r = [sum(len(TOPS[nm][u] & RS[u]) for u in range(T - W, T)) / (15 * W) * 100 for W in (10, 20, 50, 100)]
    L.append(f"- {nm}: {' / '.join(f'{x:.1f}%' for x in r)} (TB {P0 * 100:.1f}%) · chọn {ch[nm]} kỳ")
hard, wts = SELS[T]
L.append(f'\n**Kỳ tới**: loại hẳn {" ".join(f"{n + 1:02d}" for n in sorted(EXS[T]))} · pool 18: ' + ' '.join(f'{n + 1:02d}' for n in ODS[T][:18]))
txt = '\n'.join(L) + '\n'; print(txt)
if A.json: json.dump(dict(game=GAME, out=OUT, next=dict(ex=sorted(int(n) + 1 for n in EXS[T]), rank=[int(n) + 1 for n in ODS[T]], hard=hard, wts={k: float(v) for k, v in wts.items()})), open(A.json, 'w', encoding='utf-8'), ensure_ascii=False)

# ---------- THỬ TỪNG PHƯƠNG PHÁP (anh 14/10: "thử từng phương pháp chứ đừng dùng nhóm") ----------
# Mỗi lần chỉ gắn 1 phương pháp vào pool đang dùng; so với pool đang dùng ở pool 10/15/18, 4 khung.
if '--tung' in sys.argv:
    TS = range(T - TEST, T)
    def st2(OD, K):
        o = {}
        for W in (10, 20, 50, 100):
            hs = [len(set(OD[t][:K]) & RS[t]) for t in range(T - W, T)]
            o[W] = (sum(h >= 3 for h in hs) / W * 100, sum(h >= 4 for h in hs) / W * 100)
        return o
    BS = {K: st2(BASE, K) for K in (10, 15, 18)}
    rows = []
    def cmp(nm, kieu, OD, extra=''):
        r = {K: st2(OD, K) for K in (10, 15, 18)}
        # hơn = ≥3 hoặc ≥4 tăng ở CẢ khung 50 và 100, và không giảm cái còn lại ở 2 khung đó
        tot = 0; good = []
        for K in (10, 15, 18):
            for j, lab in ((0, '≥3'), (1, '≥4')):
                d50 = r[K][50][j] - BS[K][50][j]; d100 = r[K][100][j] - BS[K][100][j]; tot += d50 + d100
                if d50 > 0 and d100 > 0: good.append(f'P{K} {lab}')
        rows.append((tot, nm, kieu, r, good, extra))
    for nm, S in LO.items():
        sz = np.mean([len(S[t]) for t in TS]); miss = sum(bool(S[t] & RS[t]) for t in TS)
        if sz < 0.2: continue
        cmp(nm, 'loại', {t: [n for n in BASE[t] if n not in S[t]] for t in TS}, f'bỏ {sz:.1f} số/kỳ, loại nhầm {miss}/100 kỳ')
    for nm in SCO:
        if nm.startswith('Pool app'): continue
        cmp(nm, 'riêng', {t: [int(i) for i in np.argsort(-SC[nm][t], kind='stable')] for t in TS})
        cmp(nm, 'gộp 50/50', {t: [int(i) for i in np.argsort(-(rank01(SC[nm][t]) + rank01(SC['Pool app đang dùng (điểm goiy)'][t])), kind='stable')] for t in TS})
    fmt = lambda r, K: ' / '.join(f'{r[K][W][0]:.0f}·{r[K][W][1]:.0f}' for W in (10, 20, 50, 100))
    print(f'\n## {key} — thử TỪNG phương pháp gắn vào pool đang dùng ({len(rows)} lần thử)\n')
    print('Ô = % kỳ ≥3 số · % kỳ ≥4 số, theo khung 10 / 20 / 50 / 100 kỳ.\n')
    print(f'| Phương pháp | Cách gắn | Pool 15 | Pool 18 | Hơn pool đang dùng ở (cả khung 50 & 100) | Ghi chú |\n|---|---|---|---|---|---|')
    print(f'| **Pool đang dùng** | — | {fmt(BS, 15)} | {fmt(BS, 18)} | — | |')
    win = [x for x in rows if x[4]]
    for tot, nm, kieu, r, good, extra in sorted(win, key=lambda x: (-len(x[4]), -x[0]))[:25]:
        print(f'| {nm} | {kieu} | {fmt(r, 15)} | {fmt(r, 18)} | {", ".join(good)} | {extra} |')
    print(f'\nSố phương pháp hơn pool đang dùng ít nhất 1 chỉ số (ở cả khung 50 & 100): {len(win)}/{len(rows)}')

# ---------- MÁY TỰ HỌC (anh 14/10/2026: "máy học được cách gợi ý theo dữ liệu quá khứ từ pool") ----------
# Mỗi kỳ t, riêng cho từng cỡ pool K ∈ {10, 15, 18}: bắt đầu từ pool đang dùng; thử chồng thêm TỪNG phương pháp
# (cộng hạng hoặc loại số); giữ phương pháp làm kỳ ≥4 số trong pool K TĂNG ở cả 50 và 100 kỳ trước t (ưu tiên ≥4, hòa thì xét ≥3);
# lặp tối đa 4 lần. Chấm chính máy học bằng cách cho nó học lại ở từng kỳ của 100 kỳ gần nhất (chỉ dùng dữ liệu trước kỳ đó).
if A.hoc:
    IDX = {t: i for i, t in enumerate(TT)}
    R01 = {nm: np.stack([rank01(SC[nm][t]) for t in TT]) for nm in SCO}          # [kỳ, số]
    YT = np.stack([Y[t] if t < T else np.zeros(NB, np.int8) for t in TT])
    LOM = {nm: np.stack([np.isin(np.arange(NB), list(S[t])) for t in TT]) for nm, S in LO.items()
           if np.mean([len(S[t]) for t in TT]) <= 8 and np.mean([len(S[t]) for t in TT]) >= 0.2}
    CANS = [('cộng', nm) for nm in SCO if not nm.startswith('Pool app')] + [('loại', nm) for nm in LOM]
    def hits(Sv, Ex, ids, K):
        v = np.where(Ex[ids], -1e9, Sv[ids]); top = np.argsort(-v, axis=1, kind='stable')[:, :K]
        return np.take_along_axis(YT[ids], top, 1).sum(1)
    def rate(h, j): return (h >= j).mean()
    WL = (100, 200) if A.hoc2 else (50, 100); MAXS = 2 if A.hoc2 else 4
    def learn(t, K, maxstep=MAXS):
        i = IDX[t]; w100 = np.arange(i - WL[1], i)
        Sv = R01['Pool app đang dùng (điểm goiy)'].copy(); Ex = np.zeros_like(YT, dtype=bool); chosen = []
        def score(Sv, Ex):
            h = hits(Sv, Ex, w100, K); return (rate(h[-WL[0]:], 4), rate(h, 4), rate(h[-WL[0]:], 3), rate(h, 3))
        cur = score(Sv, Ex)
        for _ in range(maxstep):
            best = None
            for kind, nm in CANS:
                if (kind, nm) in chosen: continue
                S2, E2 = (Sv + R01[nm], Ex) if kind == 'cộng' else (Sv, Ex | LOM[nm])
                s = score(S2, E2)
                if s[0] > cur[0] and s[1] > cur[1]:
                    g = (s[0] - cur[0] + s[1] - cur[1], s[2] + s[3])
                    if best is None or g > best[0]: best = (g, kind, nm, S2, E2, s)
            if not best: break
            _, kind, nm, Sv, Ex, cur = best; chosen.append((kind, nm))
        return chosen, Sv, Ex
    def apply(t, Sv, Ex, K):
        i = IDX[t]; v = np.where(Ex[i], -1e9, Sv[i]); return [int(n) for n in np.argsort(-v, kind='stable')[:K]]
    OUT = {}; LOG = {}
    print(f'\n## {key} — máy tự học (ưu tiên kỳ ≥4 số, học riêng pool 10/15/18), chấm bằng cách học lại ở từng kỳ của 100 kỳ gần nhất\n')
    print('Ô = % kỳ ≥3 số · % kỳ ≥4 số theo khung 10 / 20 / 50 / 100 kỳ.\n')
    print('| Pool | Máy tự học | Pool đang dùng | Số về rơi vào hạng (máy học, 100 kỳ): top 10 / 11–15 / 16–18 / ngoài |\n|---|---|---|---|')
    base_i = {t: apply(t, R01['Pool app đang dùng (điểm goiy)'], np.zeros_like(YT, dtype=bool), 18) for t in range(T - TEST, T)}
    for K in (10, 15, 18):
        got = {}; ranks = []
        for t in range(T - TEST, T + 1):
            ch, Sv, Ex = learn(t, K); LOG.setdefault(K, {})[t] = ch
            i = IDX[t]; v = np.where(Ex[i], -1e9, Sv[i]); od = [int(n) for n in np.argsort(-v, kind='stable')]
            got[t] = od[:K]
            if t < T: ranks += [od.index(n) for n in RS[t]]
        def cell(OD, K):
            out = []
            for W in (10, 20, 50, 100):
                hs = [len(set(OD[t][:K]) & RS[t]) for t in range(T - W, T)]
                out.append(f'{sum(h >= 3 for h in hs) / W * 100:.0f}·{sum(h >= 4 for h in hs) / W * 100:.0f}')
            return ' / '.join(out)
        rk = np.array(ranks); dist = [(rk < 10).mean(), ((rk >= 10) & (rk < 15)).mean(), ((rk >= 15) & (rk < 18)).mean(), (rk >= 18).mean()]
        print(f"| {K} | **{cell(got, K)}** | {cell(base_i, K)} | {' / '.join(f'{x * 100:.0f}%' for x in dist)} |")
        OUT[K] = dict(next=[n + 1 for n in got[T]], chosen=[list(c) for c in LOG[K][T]])
    from collections import Counter
    for K in (10, 15, 18):
        c = Counter(nm for t in range(T - TEST, T) for kind, nm in LOG[K][t])
        print(f'\n**Pool {K}** — phương pháp máy hay chọn (số kỳ/100): ' + (' · '.join(f'{nm} ({n})' for nm, n in c.most_common(6)) or 'không chọn thêm gì (giữ pool đang dùng)'))
        print(f'Kỳ tới máy chọn: ' + (', '.join(f'{k} {nm}' for k, nm in LOG[K][T]) or 'giữ pool đang dùng') + ' → ' + ' '.join(f'{n:02d}' for n in OUT[K]['next']))
    json.dump(dict(game=GAME, last=GY['D']['dates'][-1], pools=OUT, cach='học 100 & 200 kỳ, tối đa 2' if A.hoc2 else 'học 50 & 100 kỳ, tối đa 4'), open(os.path.join(B, f'may_hoc_{GAME}{"_2" if A.hoc2 else ""}.json'), 'w', encoding='utf-8'), ensure_ascii=False)

# ---------- HỌC GHÉP DÃY TỪ POOL (anh 14/10/2026): pool có sẵn → học từ quá khứ số nào hay về / hay về cùng nhau → ghép vé nhiều số trúng nhất ----------
if A.ve:
    from itertools import combinations
    KP = 18; NV = 5
    ORD = {t: [int(i) for i in np.argsort(-SC['Pool app đang dùng (điểm goiy)'][t], kind='stable')] for t in TT}
    CB = np.array(list(combinations(range(KP), KB)))                       # mọi dãy trong pool (theo vị trí hạng)
    PR = np.array(list(combinations(range(KB), 2)))                        # các cặp trong 1 dãy
    def rank_rate(t, W=100):     # tỉ lệ về theo hạng trong pool (học 100 kỳ trước)
        c = np.zeros(KP)
        for u in range(t - W, t):
            for r, n in enumerate(ORD[u][:KP]): c[r] += Y[u, n]
        return (c + 3 * P0) / (W + 3)
    def pair_mat(t, W=100):      # số lần 2 số về cùng kỳ trong 100 kỳ
        M = np.zeros((NB, NB))
        for u in range(t - W, t):
            s_ = np.nonzero(Y[u])[0]; M[np.ix_(s_, s_)] += 1
        np.fill_diagonal(M, 0); return M / W
    def follow_pair(t, W=100):   # cặp hay về ngay sau kỳ có số x, với x thuộc kỳ trước
        M = np.zeros((NB, NB)); prev = np.nonzero(Y[t - 1])[0]; cnt = 0
        for u in range(max(1, t - W), t):
            if len(set(np.nonzero(Y[u - 1])[0]) & set(prev)):
                s_ = np.nonzero(Y[u])[0]; w = len(set(np.nonzero(Y[u - 1])[0]) & set(prev)); M[np.ix_(s_, s_)] += w; cnt += w
        np.fill_diagonal(M, 0); return M / max(cnt, 1)
    def freq(t, W=100): return Y[t - W:t].mean(0)
    def pick(scores, pool):
        od = np.argsort(-scores, kind='stable'); out = []
        for i in od:
            c = set(pool[j] for j in CB[i])
            if all(len(c & o) <= 3 for o in out): out.append(c)
            if len(out) == NV: break
        return out
    def tickets(t, how):
        pool = ORD[t][:KP]
        if how == 'hang':
            return [set(pool[i * 3: i * 3 + KB]) if i * 3 + KB <= KP else set(pool[KP - KB:]) for i in range(NV)]
        rr = rank_rate(t); fq = freq(t)[pool]; p = rr / rr.mean() + 0.5 * fq / max(fq.mean(), 1e-9)
        sc = p[CB].sum(1)
        if how in ('cap', 'cap_sau'):
            Mp = pair_mat(t)[np.ix_(pool, pool)]; a = Mp[CB[:, PR[:, 0]], CB[:, PR[:, 1]]].sum(1); sc = sc + a / max(a.mean(), 1e-9)
        if how == 'cap_sau':
            Mf = follow_pair(t)[np.ix_(pool, pool)]; b = Mf[CB[:, PR[:, 0]], CB[:, PR[:, 1]]].sum(1); sc = sc + b / max(b.mean(), 1e-9)
        return pick(sc, pool)
    HOW = (('hang', 'Theo hạng (như app)'), ('xs', 'Học tỉ lệ về theo hạng + tần suất'), ('cap', '+ cặp hay về cùng nhau'), ('cap_sau', '+ cặp hay về sau kỳ trước'))
    res = {h: {} for h, _ in HOW}
    for t in range(T - TEST, T + 1):
        for h, _ in HOW: res[h][t] = tickets(t, h)
    print(f'\n## {key} — học ghép {NV} vé từ pool {KP} (chạy tiến 100 kỳ gần)\n')
    print('Ô theo khung 10 / 20 / 50 / 100 kỳ.\n')
    print('| Cách ghép vé | Kỳ có vé ≥3 số | Kỳ có vé ≥4 số | Kỳ có vé ≥5 số (100 kỳ) | TB số trúng của vé tốt nhất (100 kỳ) |\n|---|---|---|---|---|')
    for h, lab in HOW:
        best = {t: max(len(v & RS[t]) for v in res[h][t]) for t in range(T - TEST, T)}
        f = lambda j: ' / '.join(f"{sum(best[t] >= j for t in range(T - W, T)) / W * 100:.0f}%" for W in (10, 20, 50, 100))
        print(f"| {lab} | {f(3)} | {f(4)} | {sum(best[t] >= 5 for t in range(T - 100, T))}% | {np.mean([best[t] for t in range(T - 100, T)]):.2f} |")
    pool = ORD[T][:KP]
    for h, lab in HOW[1:]:
        print(f'\nKỳ tới — {lab}: ' + ' · '.join(' '.join(f'{n + 1:02d}' for n in sorted(v)) for v in res[h][T]))
