"""Cấu trúc bộ số trúng (chẵn/lẻ, nhỏ/lớn, tổng, số liền nhau, lặp kỳ trước, số <=31) so với lý thuyết ngẫu nhiên."""
import sys, os, random, math
from math import comb
from collections import Counter
sys.path.insert(0, os.path.dirname(__file__))
from study import load

def chi2_sf(x, k):
    """P(X > x) cho phân phối chi-bình-phương k bậc tự do (hàm gamma trên, chuẩn hoá)."""
    a, x = k/2, x/2
    if x <= 0: return 1.0
    if x < a+1:   # chuỗi
        term = s = 1/a; n = a
        while abs(term) > 1e-12*abs(s): n += 1; term *= x/n; s += term
        return 1 - s*math.exp(-x + a*math.log(x) - math.lgamma(a))
    b = x+1-a; c = 1e300; d = 1/b; h = d   # phân số liên tục
    for i in range(1, 300):
        an = -i*(i-a); b += 2; d = an*d+b; d = 1/d if d else 1e300; c = b+an/c; h *= d*c
        if abs(d*c-1) < 1e-12: break
    return math.exp(-x + a*math.log(x) - math.lgamma(a))*h
def chisquare(o, e):
    class R: pass
    r = R(); r.pvalue = chi2_sf(sum((a-b)**2/b for a, b in zip(o, e)), len(o)-1); return r

def hyper(N, K, n, k): return comb(K, k)*comb(N-K, n-k)/comb(N, n)
def compare(name, obs_vals, probs, n):
    keys = sorted(probs); obs = Counter(obs_vals)
    o = [obs.get(k, 0) for k in keys]; e = [probs[k]*n for k in keys]
    # gộp các ô kỳ vọng < 5 vào ô kề để chi-square hợp lệ
    oo, ee = [], []
    for a, b in zip(o, e):
        if ee and ee[-1] < 5: oo[-1] += a; ee[-1] += b
        else: oo.append(a); ee.append(b)
    if len(ee) > 1 and ee[-1] < 5: oo[-2] += oo.pop(); ee[-2] += ee.pop()
    pv = chisquare(oo, [x*sum(oo)/sum(ee) for x in ee]).pvalue
    print(f'  {name}: p={pv:.3f}  ' + ' | '.join(f'{k}: {obs.get(k,0)} (lt {probs[k]*n:.1f})' for k in keys if probs[k]*n >= 0.5))

def sim(mx, c, f, trials=200000, seed=1):
    rng = random.Random(seed); cnt = Counter()
    for _ in range(trials): cnt[f(sorted(rng.sample(range(1, mx+1), c)))] += 1
    return {k: v/trials for k, v in cnt.items()}

if __name__ == '__main__':
    for game in ['power655', 'mega645', 'loto535']:
        mx, c, _, draws = load(game); n = len(draws)
        D = [sorted(d['nums']) for d in draws]
        print(f'\n=== {game}: {n} kỳ, chọn {c}/{mx}')
        odd = (mx+1)//2
        compare('Số lẻ trong bộ', [sum(x % 2 for x in s) for s in D], {k: hyper(mx, odd, c, k) for k in range(c+1)}, n)
        low = mx//2
        compare(f'Số nhỏ (<= {low})', [sum(x <= low for x in s) for s in D], {k: hyper(mx, low, c, k) for k in range(c+1)}, n)
        compare('Số <= 31 (ngày sinh)', [sum(x <= 31 for x in s) for s in D], {k: hyper(mx, 31, c, k) for k in range(c+1)}, n)
        cons = lambda s: sum(b-a == 1 for a, b in zip(s, s[1:]))
        compare('Cặp số liền nhau', [cons(s) for s in D], sim(mx, c, cons), n)
        rep = [len(set(D[i]) & set(D[i-1])) for i in range(1, n)]
        compare('Số lặp lại từ kỳ trước', rep, {k: hyper(mx, c, c, k) for k in range(c+1)}, n-1)
        band = lambda s: (sum(s)-c*(mx+1)/2)//(c*(mx+1)/2*0.1)   # nhóm tổng theo 10% quanh trung bình
        sums = [sum(s) for s in D]
        ps = sim(mx, c, sum); lo, hi, acc = None, None, 0
        for k in sorted(ps):
            acc += ps[k]
            if lo is None and acc >= 0.15: lo = k
            if hi is None and acc >= 0.85: hi = k
        inside = sum(lo <= s <= hi for s in sums)
        print(f'  Tổng bộ số: TB {sum(sums)/n:.1f} (lý thuyết {c*(mx+1)/2:.1f}); trong khoảng giữa 70% [{lo}–{hi}]: {inside}/{n} = {inside/n*100:.1f}% (lý thuyết 70%)')
        dec = lambda s: len({(x-1)//10 for x in s})
        compare('Số nhóm chục khác nhau', [dec(s) for s in D], sim(mx, c, dec), n)
