"""Phong cách "theo phong độ gần đây": trước mỗi kỳ t, chọn các phương pháp
  (1) trúng tốt trong 200 kỳ ngay trước t (z ≥ 1,5), và (2) không thua ngẫu nhiên ở 300 kỳ trước đó (z ≥ 0);
rồi gộp phiếu các phương pháp đó → xếp số → ghép 10 bộ, 2 bộ bất kỳ chung tối đa 1 số.
Kiểm tra TRUNG THỰC: đi lần lượt từng kỳ, chỉ dùng dữ liệu trước kỳ đó. So với đối chứng (điểm ngẫu nhiên, cùng cách ghép).
Chạy: python3 research/form.py loto535 [số kỳ kiểm, mặc định 300]"""
import sys, os, math, random, itertools
from collections import Counter
from itertools import permutations
sys.path.insert(0, os.path.dirname(__file__))
from study import load
from report import all_rules
from recency import pick
from community import methods as cmethods

game = sys.argv[1] if len(sys.argv) > 1 else 'loto535'
TEST = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() else 300
RW = int(sys.argv[sys.argv.index('--w')+1]) if '--w' in sys.argv else 200
PW = 300
TOPK = int(sys.argv[sys.argv.index('--k')+1]) if '--k' in sys.argv else 5
mx, c, _, dr = load(game); D = [set(d['nums']) for d in dr]; n = len(D)

M = {}
for k, f in all_rules(mx).items(): M['Ngày: ' + k] = [f(d['info']) for d in dr]
for mode, lab in (('num', 'nóng'), ('cold', 'lạnh')):
    for w in (5, 10, 20, 30, 50, 100, 200, None):
        M[f"Gần đây: {c} số {lab} {'từ đầu' if w is None else f'{w} kỳ'}"] = [set(pick(D[:i] if w is None else D[max(0, i-w):i], mx, mode, c)) if i else set() for i in range(n)]
last = {x: -1 for x in range(1, mx+1)}; G = []
for i in range(n):
    G.append(set(sorted(range(1, mx+1), key=lambda x: (last[x], x))[:c]))
    for x in D[i]: last[x] = i
M[f'Gần đây: {c} số gan nhất'] = G
CM = cmethods(mx, c); st = {'follow': Counter(), 'cnt': Counter(), 'pos': list(permutations(range(2*c), 2))}
cres = {k: [set()] for k in CM}
for i in range(1, n):
    for k, f in CM.items(): cres[k].append(f(D[:i], st))
    for x in D[i-1]:
        st['cnt'][x] += 1
        for y in D[i]: st['follow'][(x, y)] += 1
for k, v in cres.items(): M['Cộng đồng: ' + k] = v
names = [k for k in M if sum(map(len, M[k]))]
pre = {}
for k in names:
    H = [0.0]; E = [0.0]; V = [0.0]
    for S, w in zip(M[k], D):
        q = len(S)/mx; H.append(H[-1] + len(S & w)); E.append(E[-1] + c*q); V.append(V[-1] + c*q*(1-q)*(mx-c)/(mx-1))
    pre[k] = (H, E, V)
def seg(k, a, b):
    H, E, V = pre[k]; e = E[b]-E[a]; v = V[b]-V[a]; h = H[b]-H[a]
    return h, e, ((h-e)/math.sqrt(v) if v > 0 else 0.0)

TOP5 = '--top5' in sys.argv or '--k' in sys.argv   # lấy TOPK phương pháp tốt nhất RW kỳ gần (xếp theo z), không xét 300 kỳ trước
def select(t):
    a = max(0, t-RW); b0 = max(0, a-PW); out = []
    for k in names:
        h, e, z = seg(k, a, t)
        if TOP5:
            if e > 0 and h > e and M[k][t] if t < n else e > 0 and h > e: out.append((k, h/e, z))
            continue
        if e <= 0 or z < 1.5: continue
        if a - b0 >= 50 and seg(k, b0, a)[2] < 0: continue
        out.append((k, h/e, z))
    if TOP5 and '--hits' in sys.argv:   # xếp theo số lần đúng nhiều nhất (không so với ngẫu nhiên)
        out = sorted(out, key=lambda r: (-seg(r[0], max(0, t-RW), t)[0], -r[2]))[:TOPK]
    elif TOP5: out = sorted(out, key=lambda r: -r[2])[:TOPK]
    return out

rs = random.Random(2); tot = sorted(sum(rs.sample(range(1, mx+1), c)) for _ in range(100000))
LO, HI = tot[15000], tot[85000]; half = mx//2
def shape_ok(s):
    o = sum(x % 2 for x in s); lo = sum(x <= half for x in s)
    return 1 <= o <= c-1 and (2 if c >= 5 else 1) <= lo <= c-2 and LO <= sum(s) <= HI
def gen(order, score, K=22, share=1):
    # ứng viên: 5 số đầu của mỗi nhóm (nhỏ-lẻ, nhỏ-chẵn, to-lẻ, to-chẵn) + các số xếp đầu còn lại cho đủ K
    # → luôn ghép được bộ cân bằng chẵn/lẻ, nhỏ/to dù các phương pháp dồn phiếu về một nhóm
    pool = []
    for lo in (True, False):
        for od in (1, 0): pool += [x for x in order if (x <= half) == lo and x % 2 == od][:5]
    pool += [x for x in order if x not in pool][:K-len(pool)]
    cand = [(sum(score[x] for x in s), s) for s in itertools.combinations(sorted(pool), c) if shape_ok(s)]
    cand.sort(key=lambda z: -z[0]); out = []
    for sh in (share, share+1):   # vé 6 số: 10 bộ chung ≤ 1 số từ 22 số đầu không phải lúc nào cũng đủ → nới lên 2
        for _, s in cand:
            if len(out) == 10: break
            if s not in out and all(len(set(s) & set(o)) <= sh for o in out): out.append(s)
    return out

def run(scorer, reps=1):
    one = top5 = best = ge2 = ge3 = cnt = 0; nsel = 0
    for r in range(reps):
        rng = random.Random(50+r)
        for t in range(n-TEST, n):
            order, score, k = scorer(t, rng); nsel += k
            top5 += len(set(order[:c]) & D[t])
            S = gen(order, score); h = [len(set(s) & D[t]) for s in S]
            one += h[0]; best += max(h); ge2 += max(h) >= 2; ge3 += max(h) >= 3; cnt += 1
    return dict(top5=top5/cnt, one=one/cnt, best=best/cnt, ge2=ge2/cnt, ge3=ge3/cnt, nsel=nsel/cnt)
def form_scorer(t, rng):
    sel = select(t); sc = [0.0]*(mx+1); tie = [rng.random()*1e-3 for _ in range(mx+1)]
    for k, lift, z in sel:
        for x in M[k][t]: sc[x] += 1 + 0.2*math.log(lift)
    order = sorted(range(1, mx+1), key=lambda x: -(sc[x]+tie[x])); return order, [s+tie[i] for i, s in enumerate(sc)], len(sel)
def rand_scorer(t, rng):
    sc = [rng.random() for _ in range(mx+1)]; return sorted(range(1, mx+1), key=lambda x: -sc[x]), sc, 0

if __name__ == '__main__':
    p = lambda k: math.comb(c, k)*math.comb(mx-c, c-k)/math.comb(mx, c)
    print(f'{game}: kiểm {TEST} kỳ gần nhất, mỗi kỳ chọn {TOPK if TOP5 else "các"} phương pháp tốt nhất {RW} kỳ trước')
    print(f'Ngẫu nhiên 1 bộ: {c*c/mx:.3f} số')
    if '--list' in sys.argv:   # TOPK phương pháp đúng nhiều nhất RW kỳ gần nhất (tính cho kỳ sắp tới)
        for k, lift, z in select(n):
            h, e, _ = seg(k, n-RW, n); print(f"  {k[:60]:60s} đúng {int(h):4d} số / {RW} kỳ = {h/RW:.2f} số/kỳ (ngẫu nhiên {e/RW:.2f}, +{100*(lift-1):.0f}%, z {z:+.2f})")
        sys.exit()
    a = run(form_scorer); b = run(rand_scorer, 3)
    for lab, r in (('Phong độ gần đây', a), ('Đối chứng ngẫu nhiên', b)):
        print(f"{lab:22s} PP/kỳ {r['nsel']:4.1f} | top{c} số {r['top5']:.3f} | bộ#1 {r['one']:.3f} | tốt nhất {r['best']:.3f} | có bộ ≥2 {100*r['ge2']:.1f}% | ≥3 {100*r['ge3']:.1f}%")
