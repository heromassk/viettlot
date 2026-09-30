"""Thử các cách chọn 10 bộ Loto 5/35 và "đoán lại quá khứ" một cách TRUNG THỰC (walk-forward):
trước mỗi kỳ t, chỉ dùng dữ liệu các kỳ < t để (1) chọn tín hiệu "hy vọng nhỏ", (2) chấm điểm số, (3) ghép 10 bộ.
So với cùng cách ghép nhưng điểm số ngẫu nhiên → tách được phần nhờ "tín hiệu" và phần nhờ "cách ghép bộ".
Chạy: python3 research/strategy_loto.py [kỳ bắt đầu, mặc định 300]"""
import sys, os, math, random, itertools
from collections import Counter
sys.path.insert(0, os.path.dirname(__file__))
from study import load
from report import all_rules
from recency import pick

mx, c, _, D = load('loto535'); n = len(D)
START = int(sys.argv[1]) if len(sys.argv) > 1 else 300
W = [d['nums'] for d in D]

# ---- tín hiệu: quy luật theo ngày + số nóng/lạnh theo mốc (tập số mỗi kỳ) ----
R = all_rules(mx)
sig = {k: [f(d['info']) for d in D] for k, f in R.items()}
for mode in ('num', 'cold'):
    for w in (5, 10, 20, 30, 50, 100, 200):
        sig[f'Gần đây: {mode} {w}'] = [set(pick(W[max(0, i-w):i], mx, mode, c)) if i else set() for i in range(n)]
sig = {k: v for k, v in sig.items() if sum(map(len, v))}
names = list(sig)
# tổng tích lũy H (trúng), E (kỳ vọng), V (phương sai) để tính z trên đoạn bất kỳ trong O(1)
pre = {}
for k in names:
    H = [0.0]; E = [0.0]; V = [0.0]
    for S, w in zip(sig[k], W):
        K = len(S); p = K/mx
        H.append(H[-1] + len(S & w)); E.append(E[-1] + c*p); V.append(V[-1] + c*p*(1-p)*(mx-c)/(mx-1))
    pre[k] = (H, E, V)
def zseg(k, a, b):
    H, E, V = pre[k]; v = V[b]-V[a]
    return ((H[b]-H[a]) - (E[b]-E[a]))/math.sqrt(v) if v > 0 else 0.0
def scores_at(t):
    """Điểm từng số trước kỳ t: cộng ln(lift) của các tín hiệu đạt 'hy vọng nhỏ' tính trên kỳ 0..t-1."""
    cut = int(0.6*t); s = [0.0]*(mx+1); used = 0
    for k in names:
        zA = zseg(k, 0, t)
        if abs(zA) < 1.5: continue
        zO, zN = zseg(k, 0, cut), zseg(k, cut, t)
        if zO*zN <= 0: continue
        H, E, _ = pre[k]; lift = (H[t]-H[0])/(E[t]-E[0]) if E[t] > 0 else 1
        if lift <= 0: continue
        used += 1
        for x in sig[k][t]: s[x] += math.log(lift)
    return s, used

# ---- hình dạng hay gặp: 1–4 số lẻ, 2–3 số nhỏ (≤17), tổng ở 70% giữa ----
sums = sorted(sum(random.Random(1).sample(range(1, mx+1), c)) for _ in range(1))
rs = random.Random(2); tot = sorted(sum(rs.sample(range(1, mx+1), c)) for _ in range(100000))
LO, HI = tot[15000], tot[85000]
def shape_ok(s):
    o = sum(x % 2 for x in s); lo = sum(x <= mx//2 for x in s); t = sum(s)
    return 1 <= o <= 4 and 2 <= lo <= 3 and LO <= t <= HI

COMBOS = {}
def gen_sets(order, score, max_share, K=20, n_sets=10):
    """Ghép 10 bộ: xét mọi bộ 5 số trong K số đầu, xếp theo tổng điểm; lấy tham lam, 2 bộ bất kỳ chung ≤ max_share số."""
    top = order[:K]; cand = []
    for s in itertools.combinations(sorted(top), c):
        if shape_ok(s): cand.append((sum(score[x] for x in s), s))
    cand.sort(key=lambda z: -z[0]); out = []
    for _, s in cand:
        if all(len(set(s) & set(o)) <= max_share for o in out):
            out.append(s)
            if len(out) == n_sets: break
    return out

def evaluate(get_order, label, max_share, reps=1):
    one = best = ge2 = ge3 = tot = cnt = 0; hitdist = Counter()
    for r in range(reps):
        rng = random.Random(100 + r)
        for t in range(START, n):
            order, score = get_order(t, rng)
            S = gen_sets(order, score, max_share, K=20 if max_share >= 3 else 24)
            h = [len(set(s) & W[t]) for s in S]
            one += h[0]; best += max(h); ge2 += max(h) >= 2; ge3 += max(h) >= 3; tot += sum(h)/len(h); cnt += 1
            for x in h: hitdist[x] += 1
    return dict(label=label, share=max_share, one=one/cnt, best=best/cnt, ge2=ge2/cnt, ge3=ge3/cnt, avg=tot/cnt,
                d3=hitdist[3]/sum(hitdist.values()), sets=sum(hitdist.values())/cnt)

SC = {t: scores_at(t) for t in range(START, n)}
def by_signal(t, rng):
    s, _ = SC[t]; tie = [rng.random() for _ in range(mx+1)]
    return sorted(range(1, mx+1), key=lambda x: (-s[x], tie[x])), s
def by_random(t, rng):
    s = [rng.random() for _ in range(mx+1)]
    return sorted(range(1, mx+1), key=lambda x: -s[x]), s

if __name__ == '__main__':
    used = [SC[t][1] for t in SC]
    print(f'Loto: đoán lại {n-START} kỳ (từ kỳ {START}); số tín hiệu được chọn mỗi kỳ TB {sum(used)/len(used):.1f}')
    p = lambda k: math.comb(c, k)*math.comb(mx-c, c-k)/math.comb(mx, c)
    print(f'Mỗi bộ ngẫu nhiên: TB {c*c/mx:.3f} số, P(≥2)={sum(p(k) for k in range(2,6)):.3f}, P(≥3)={sum(p(k) for k in range(3,6)):.4f}')
    print(f"{'cách':34s} {'chung≤':>6s} {'bộ#1':>6s} {'TB/bộ':>6s} {'tốt nhất':>8s} {'≥2 số':>6s} {'≥3 số':>6s}")
    for share in (3, 2, 1):
        for lab, fn, reps in (('Tín hiệu (walk-forward)', by_signal, 1), ('Điểm ngẫu nhiên (đối chứng)', by_random, 3)):
            r = evaluate(fn, lab, share, reps)
            print(f"{r['label']:34s} {share:6d} {r['one']:6.3f} {r['avg']:6.3f} {r['best']:8.3f} {100*r['ge2']:5.1f}% {100*r['ge3']:5.1f}%")
