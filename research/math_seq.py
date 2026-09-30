"""Các phép toán tìm quy luật trong dãy số:
1) Phân tích Fourier: chuỗi trúng/trượt của từng số có chu kỳ (cứ k kỳ lại về) không?
2) Đồng dư: phân bố số trúng theo mod 3,4,5,7,9 có lệch không; mod của kỳ sau có phụ thuộc kỳ trước không
3) Chuỗi tổng các số qua từng kỳ: có xu hướng, chu kỳ hay tự tương quan không
4) Độ nén (entropy): dãy kết quả thật có nén được hơn dãy ngẫu nhiên không (có quy luật thì nén được hơn)"""
import sys, os, math, random, zlib
import numpy as np
from collections import Counter
sys.path.insert(0, os.path.dirname(__file__))
from study import load
from combo import chi2_sf

def fourier(D, mx, sims=200, seed=1):
    n = len(D); rng = random.Random(seed)
    def peak(DD):
        best = 0
        for x in range(1, mx+1):
            s = np.array([1.0 if x in d else 0.0 for d in DD]); s -= s.mean()
            p = np.abs(np.fft.rfft(s))[1:]**2 / (s*s).sum()
            best = max(best, p.max())
        return best
    real = peak(D); sim = sorted(peak([set(rng.sample(range(1, mx+1), len(D[0]))) for _ in range(n)]) for _ in range(sims))
    return real, sim[int(0.95*sims)], sum(v >= real for v in sim)/sims
def modular(D, mx, c):
    out = []
    for m in (3, 4, 5, 7, 9):
        pool = Counter(x % m for x in range(1, mx+1)); obs = Counter(x % m for d in D for x in d)
        n = len(D)*c; x2 = sum((obs[r]-n*pool[r]/mx)**2/(n*pool[r]/mx) for r in range(m))
        # tổng mod m của kỳ sau có phụ thuộc kỳ trước không (bảng chuyển tiếp)
        seq = [sum(d) % m for d in D]; T = Counter(zip(seq, seq[1:])); rows = Counter(seq[:-1]); cols = Counter(seq[1:]); N = len(seq)-1
        x2t = sum((T[(a, b)]-rows[a]*cols[b]/N)**2/(rows[a]*cols[b]/N) for a in range(m) for b in range(m) if rows[a]*cols[b])
        out.append((m, chi2_sf(x2, m-1), chi2_sf(x2t, (m-1)**2)))
    return out
def sums(D):
    s = np.array([sum(d) for d in D], float); n = len(s); t = np.arange(n)
    slope = np.polyfit(t, s, 1)[0]; resid = s - np.polyval(np.polyfit(t, s, 1), t)
    se = math.sqrt((resid**2).sum()/(n-2)/((t-t.mean())**2).sum())
    z = s - s.mean(); ac = [(z[:-k]*z[k:]).sum()/(z*z).sum() for k in range(1, 11)]
    Q = n*(n+2)*sum(r*r/(n-k) for k, r in enumerate(ac, 1))
    return slope*100, abs(slope/se), chi2_sf(Q, 10), max(ac, key=abs)
def compress(D, mx, c, sims=50, seed=2):
    rng = random.Random(seed)
    enc = lambda DD: bytes(x for d in DD for x in sorted(d))
    real = len(zlib.compress(enc(D), 9))
    sim = [len(zlib.compress(enc([set(rng.sample(range(1, mx+1), c)) for _ in D]), 9)) for _ in range(sims)]
    return real, sum(sim)/sims, min(sim), max(sim)

if __name__ == '__main__':
    for game in ['power655', 'mega645', 'loto535']:
        mx, c, _, dr = load(game); D = [set(d['nums']) for d in dr]
        print(f'\n######## {game}: {len(D)} kỳ')
        real, thr, p = fourier(D, mx)
        print(f'1) FOURIER: đỉnh chu kỳ mạnh nhất trong {mx} số = {real:.4f}; dãy ngẫu nhiên thường ≤ {thr:.4f} (95%) → p={p:.2f}')
        for m, p1, p2 in modular(D, mx, c):
            print(f'2) ĐỒNG DƯ mod {m}: phân bố p={p1:.3f}; tổng mod {m} kỳ sau phụ thuộc kỳ trước p={p2:.3f}')
        sl, zs, pq, acm = sums(D)
        print(f'3) CHUỖI TỔNG: xu hướng {sl:+.2f} mỗi 100 kỳ (z {zs:.2f}); tự tương quan 10 độ trễ p={pq:.3f} (mạnh nhất r={acm:+.3f})')
        r, m_, lo, hi = compress(D, mx, c)
        print(f'4) ĐỘ NÉN: dãy thật nén còn {r} byte; dãy ngẫu nhiên {m_:.0f} byte (khoảng {lo}–{hi})')
