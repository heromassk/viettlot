""""Đấu loại" các phương pháp gợi ý trên 500 kỳ gần nhất — có KIỂM CHỨNG để tránh tự lừa mình.
- Mỗi phương pháp, trước mỗi kỳ chỉ dùng dữ liệu các kỳ trước, cho ra một tập số; đếm số trùng với kết quả kỳ đó.
- Chia 500 kỳ: 300 kỳ đầu để CHỌN (xếp hạng phương pháp), 200 kỳ sau để KIỂM (phương pháp đứng đầu có giữ phong độ không).
- Thêm bản "cuốn chiếu": trước mỗi kỳ trong 200 kỳ kiểm, chọn lại top phương pháp theo 300 kỳ ngay trước nó.
Chạy: python3 research/tournament.py loto535 [--json out.json]"""
import sys, os, math, json, random
from collections import Counter
from itertools import permutations
sys.path.insert(0, os.path.dirname(__file__))
from study import load
from report import all_rules
from recency import pick
from community import methods as cmethods

game = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith('-') else 'loto535'
mx, c, _, dr = load(game); D = [set(d['nums']) for d in dr]; n = len(D)
LAST, SEL = 500, 300
A = n - LAST                      # kỳ đầu tiên của 500 kỳ
idx = list(range(A, n))

# ---- tập số của từng phương pháp cho mỗi kỳ trong 500 kỳ ----
M = {}
for k, f in all_rules(mx).items():
    M['Ngày: ' + k] = [f(dr[i]['info']) for i in idx]
for mode, lab in (('num', 'nóng'), ('cold', 'lạnh')):
    for w in (5, 10, 20, 30, 50, 100, 200, None):
        M[f"Gần đây: {c} số {lab} {'từ đầu' if w is None else f'{w} kỳ'}"] = [set(pick(D[:i] if w is None else D[max(0, i-w):i], mx, mode, c)) for i in idx]
def gan(i, k):
    last = {x: -1 for x in range(1, mx+1)}
    for j in range(i):
        for x in D[j]: last[x] = j
    return set(sorted(range(1, mx+1), key=lambda x: (last[x], x))[:k])
M[f'Gần đây: {c} số gan nhất'] = [gan(i, c) for i in idx]
CM = cmethods(mx, c)
st = {'follow': Counter(), 'cnt': Counter(), 'pos': list(permutations(range(2*c), 2))}
cres = {k: [] for k in CM}
for i in range(1, n):
    if i >= A:
        for k, f in CM.items(): cres[k].append(f(D[:i], st))
    for x in D[i-1]:
        st['cnt'][x] += 1
        for y in D[i]: st['follow'][(x, y)] += 1
for k, v in cres.items(): M['Cộng đồng: ' + k] = v
M = {k: v for k, v in M.items() if sum(map(len, v))}

def stats(k, a, b):
    """trúng, kỳ vọng, z trên kỳ a..b-1 (chỉ số trong 500 kỳ)."""
    H = E = V = 0.0
    for j in range(a, b):
        S = M[k][j]; q = len(S)/mx
        H += len(S & D[idx[j]]); E += c*q; V += c*q*(1-q)*(mx-c)/(mx-1)
    return H, E, ((H-E)/math.sqrt(V) if V > 0 else 0.0)

rows = []
for k in M:
    hS, eS, zS = stats(k, 0, SEL); hV, eV, zV = stats(k, SEL, LAST)
    if eS == 0: continue
    rows.append(dict(rule=k, size=round(sum(map(len, M[k]))/LAST, 1), sel_hits=int(hS), sel_exp=round(eS, 1), sel_lift=round(hS/eS, 3), sel_z=round(zS, 2),
                     val_hits=int(hV), val_exp=round(eV, 1), val_lift=round(hV/eV, 3) if eV else None, val_z=round(zV, 2)))
rows.sort(key=lambda r: -r['sel_z'])

def vote_hits(methods_for, a, b, k=c):
    """Gộp phiếu: mỗi phương pháp trong danh sách cho 1 phiếu/số (chia đều theo kích thước tập) → lấy k số nhiều phiếu nhất."""
    hits = 0
    for j in range(a, b):
        sc = Counter()
        for m in methods_for(j):
            S = M[m][j]
            for x in S: sc[x] += 1/len(S)
        rng = random.Random(j); tie = {x: rng.random() for x in range(1, mx+1)}
        top = sorted(range(1, mx+1), key=lambda x: (-sc[x], tie[x]))[:k]
        hits += len(set(top) & D[idx[j]])
    return hits/(b-a)

if __name__ == '__main__':
    TOP = 10
    top = [r['rule'] for r in rows[:TOP]]
    print(f'{game}: {len(M)} phương pháp, 500 kỳ gần nhất ({dr[A]["info"]["d"]}/{dr[A]["info"]["m"]}/{dr[A]["info"]["y"]} → cuối). Chọn trên 300 kỳ đầu, kiểm trên 200 kỳ sau.')
    print(f"\nTOP {TOP} theo 300 kỳ CHỌN        | {'chọn: lift  z':>14s} | {'kiểm: lift   z':>15s}")
    for r in rows[:TOP]:
        print(f"{r['rule'][:44]:44s} | {(r['sel_lift']-1)*100:+5.0f}% {r['sel_z']:+5.2f} | {(r['val_lift']-1)*100 if r['val_lift'] else 0:+6.0f}% {r['val_z']:+5.2f}")
    vz = [r['val_z'] for r in rows[:TOP]]; allv = [r['val_z'] for r in rows]
    print(f"\nz kiểm TB của top {TOP}: {sum(vz)/len(vz):+.2f}  | z kiểm TB của mọi phương pháp: {sum(allv)/len(allv):+.2f}")
    # tương quan hạng chọn ↔ kiểm
    xs = [r['sel_z'] for r in rows]; ys = [r['val_z'] for r in rows]; mxs, mys = sum(xs)/len(xs), sum(ys)/len(ys)
    corr = sum((a-mxs)*(b-mys) for a, b in zip(xs, ys))/math.sqrt(sum((a-mxs)**2 for a in xs)*sum((b-mys)**2 for b in ys))
    print(f'Tương quan điểm chọn ↔ điểm kiểm trên {len(rows)} phương pháp: r = {corr:+.3f} (≈0 nghĩa là đứng đầu lúc chọn không giữ được phong độ)')
    # gộp phiếu top 10: cố định và cuốn chiếu
    fixed = vote_hits(lambda j: top, SEL, LAST)
    def rolling(j):
        cand = []
        for k in M:
            h, e, z = stats(k, j-SEL, j)
            if e: cand.append((z, k))
        cand.sort(reverse=True); return [k for _, k in cand[:TOP]]
    roll = vote_hits(rolling, SEL, LAST)
    print(f'\nGộp phiếu top {TOP} → chọn {c} số mỗi kỳ, trên 200 kỳ kiểm: cố định {fixed:.3f} số/kỳ | cuốn chiếu {roll:.3f} | ngẫu nhiên {c*c/mx:.3f}')
    if '--json' in sys.argv:
        json.dump(dict(game=game, last=LAST, sel=SEL, top=TOP, corr=round(corr, 3), fixed=round(fixed, 3), rolling=round(roll, 3),
                       random=round(c*c/mx, 3), rows=rows), open(sys.argv[sys.argv.index('--json')+1], 'w'), ensure_ascii=False)
        print('đã ghi')
