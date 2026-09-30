"""Kiểm tra các phương pháp phân tích dãy số phổ biến trên thế giới:
1) Mẫu nhóm Gianella / Lotterycodex (nhỏ-lẻ, nhỏ-chẵn, to-lẻ, to-chẵn)
2) Ion Saliu – skip ≤ trung vị FFG
3) Số nguyên tố, Fibonacci trong bộ
4) Học máy (hồi quy logistic) dự đoán số kỳ sau, huấn luyện 60% / kiểm tra 40%
5) Kiểm định ngẫu nhiên: tự tương quan chuỗi trúng/trượt của từng số (lag 1–5)"""
import sys, os, math, random
import numpy as np
from math import comb
from collections import Counter
sys.path.insert(0, os.path.dirname(__file__))
from study import load
from combo import chi2_sf
def zp(z): return math.erfc(abs(z)/math.sqrt(2))

def templates(mx, c, D):
    low = mx//2
    grp = lambda x: ('N' if x <= low else 'T') + ('L' if x % 2 else 'C')      # N=nhỏ T=to, L=lẻ C=chẵn
    sizes = Counter(grp(x) for x in range(1, mx+1)); keys = ['NL', 'NC', 'TL', 'TC']
    def comps(k, left):
        if len(k) == 1: yield (left,); return
        for a in range(left+1):
            for rest in comps(k[1:], left-a): yield (a,) + rest
    th = {}
    for t in comps(keys, c):
        th[t] = math.prod(comb(sizes[k], a) for k, a in zip(keys, t))/comb(mx, c)
    obs = Counter(tuple(Counter(grp(x) for x in s)[k] for k in keys) for s in D)
    n = len(D); top = sorted(th, key=lambda t: -th[t])
    # gộp ô kỳ vọng nhỏ
    oo = ee = 0; x2 = 0; df = 0; small_o = small_e = 0
    for t in top:
        e = th[t]*n
        if e >= 5: x2 += (obs.get(t, 0)-e)**2/e; df += 1
        else: small_o += obs.get(t, 0); small_e += e
    if small_e: x2 += (small_o-small_e)**2/small_e; df += 1
    k6 = top[:6]; share_th = sum(th[t] for t in k6); share_ob = sum(obs.get(t, 0) for t in k6)/n
    return len(th), k6, share_th, share_ob, chi2_sf(x2, df-1), sizes

def ffg_median(mx, c):
    p = c/mx; return math.ceil(math.log(0.5)/math.log(1-p))    # N để P(xuất hiện ít nhất 1 lần) ≥ 50%

def saliu(mx, c, D, start=30):
    med = ffg_median(mx, c); last = {}
    hi = hn = lo = ln = 0; allin = 0; nt = 0; expect_allin = 0
    for i, s in enumerate(D):
        if i >= start:
            skip = {x: (i - last[x] - 1) if x in last else 999 for x in range(1, mx+1)}
            S = {x for x in range(1, mx+1) if skip[x] <= med}
            hi += len(s & S); hn += len(S); lo += len(s - S); ln += mx - len(S)
            allin += s <= S; nt += 1; expect_allin += comb(len(S), c)/comb(mx, c)
        for x in s: last[x] = i
    return med, hi/hn, lo/ln, c/mx, allin, expect_allin, nt

PRIMES = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53}
FIB = {1, 2, 3, 5, 8, 13, 21, 34, 55}
def special_counts(mx, c, D, S):
    K = len([x for x in S if x <= mx]); n = len(D)
    th = {k: comb(K, k)*comb(mx-K, c-k)/comb(mx, c) for k in range(c+1)}
    obs = Counter(len(set(s) & S) for s in D)
    mean_o = sum(k*v for k, v in obs.items())/n; mean_t = c*K/mx
    x2 = 0; df = 0; so = se = 0
    for k in range(c+1):
        e = th[k]*n
        if e >= 5: x2 += (obs.get(k, 0)-e)**2/e; df += 1
        else: so += obs.get(k, 0); se += e
    if se: x2 += (so-se)**2/se; df += 1
    return K, mean_o, mean_t, chi2_sf(x2, df-1)

def features(D, i, mx):
    """Đặc trưng của từng số trước kỳ i: tần suất 5/10/30/100 kỳ, từ đầu, số kỳ vắng, về kỳ trước."""
    F = []
    for x in range(1, mx+1):
        f = [sum(x in s for s in D[max(0, i-w):i])/w for w in (5, 10, 30, 100)]
        f.append(sum(x in s for s in D[:i])/max(i, 1))
        g = next((k for k in range(1, i+1) if x in D[i-k]), i+1)
        f += [min(g, 60)/60, 1.0 if i and x in D[i-1] else 0.0]
        F.append(f)
    return np.array(F)

def ml(mx, c, D, start=100):
    n = len(D); cut = start + int((n-start)*0.6)
    X, Y, G = [], [], []
    for i in range(start, n):
        X.append(features(D, i, mx)); Y.append(np.array([1.0 if x in D[i] else 0.0 for x in range(1, mx+1)])); G.append(i)
    X = np.array(X); Y = np.array(Y)
    tr = [k for k, i in enumerate(G) if i < cut]; te = [k for k, i in enumerate(G) if i >= cut]
    Xtr = X[tr].reshape(-1, X.shape[2]); Ytr = Y[tr].reshape(-1)
    mu, sd = Xtr.mean(0), Xtr.std(0)+1e-9
    Z = (Xtr-mu)/sd; Z = np.hstack([Z, np.ones((len(Z), 1))]); w = np.zeros(Z.shape[1])
    for _ in range(400):                      # hồi quy logistic, gradient descent
        pz = 1/(1+np.exp(-Z@w)); w -= 0.5*(Z.T@(pz-Ytr)/len(Ytr) + 1e-3*w)
    hits = 0
    for k in te:
        z = np.hstack([(X[k]-mu)/sd, np.ones((mx, 1))]); pr = 1/(1+np.exp(-z@w))
        top = np.argsort(-pr, kind='stable')[:c]; hits += Y[k][top].sum()
    E = len(te)*c*c/mx; p = c/mx; V = len(te)*c*p*(1-p)*(mx-c)/(mx-1)
    return len(tr), len(te), hits, E, (hits-E)/math.sqrt(V), w[:-1]

def autocorr(mx, D, lags=(1, 2, 3, 4, 5)):
    n = len(D); Q = 0; zs = []
    for x in range(1, mx+1):
        s = np.array([1.0 if x in d else 0.0 for d in D]); s -= s.mean(); v = (s*s).sum()
        for L in lags:
            r = (s[:-L]*s[L:]).sum()/v; zs.append(r*math.sqrt(n)); Q += n*r*r
    return chi2_sf(Q, mx*len(lags)), max(abs(z) for z in zs), sum(abs(z) > 1.96 for z in zs), len(zs)

if __name__ == '__main__':
    for game in ['power655', 'mega645', 'loto535']:
        mx, c, _, dr = load(game); D = [set(d['nums']) for d in dr]; n = len(D)
        print(f'\n################ {game}: {n} kỳ')
        nt, k6, sth, sob, p, sizes = templates(mx, c, [sorted(s) for s in D])
        print(f'1) MẪU GIANELLA/LOTTERYCODEX: {nt} mẫu; 6 mẫu "ưu thế" {["-".join(map(str,t)) for t in k6]} (thứ tự NL-NC-TL-TC)')
        print(f'   6 mẫu này chiếm {sth*100:.1f}% theo toán học, thực tế {sob*100:.1f}% số kỳ | kiểm định toàn bộ mẫu p={p:.3f}')
        med, ph, pl, pt, allin, eallin, nt2 = saliu(mx, c, D)
        print(f'2) SALIU FFG: trung vị = {med} kỳ. Số có skip ≤ {med}: về {ph*100:.2f}%/kỳ; skip > {med}: {pl*100:.2f}%/kỳ; lý thuyết {pt*100:.2f}%')
        print(f'   Kỳ mà CẢ {c} số đều có skip ≤ trung vị: {allin}/{nt2} (nếu ngẫu nhiên kỳ vọng {eallin:.1f})')
        for name, S in [('số nguyên tố', PRIMES), ('số Fibonacci', FIB)]:
            K, mo, mt, pp = special_counts(mx, c, [s for s in D], S)
            print(f'3) {name} ({K} số trong 1–{mx}): TB mỗi bộ {mo:.2f} (lý thuyết {mt:.2f}), phân bố p={pp:.3f}')
        tr, te, hits, E, z, w = ml(mx, c, D)
        print(f'4) HỌC MÁY (logistic, 7 đặc trưng): học {tr} kỳ, kiểm {te} kỳ: trúng {hits:.0f} / ngẫu nhiên {E:.1f} ({(hits/E-1)*100:+.1f}%, z {z:+.2f}, p={zp(z):.3f})')
        pa, mz, nsig, nz = autocorr(mx, D)
        print(f'5) TỰ TƯƠNG QUAN chuỗi trúng/trượt từng số (lag 1–5): p chung={pa:.3f}; |z| lớn nhất {mz:.2f}; {nsig}/{nz} phép có |z|>1,96 (ngẫu nhiên ~{0.05*nz:.0f})')
