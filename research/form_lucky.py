"""Số may mắn Loto (1..12) theo "phong độ gần đây" + đấu loại phương pháp.
Phương pháp = quy luật theo ngày (report.all_rules(12)) + tín hiệu lịch sử (lucky.rules: nóng/lạnh, gan, bạc nhớ, giờ quay...).
(A) Đấu loại trên 500 kỳ gần: xếp hạng ở 300 kỳ đầu, kiểm ở 200 kỳ sau.
(B) Phong độ: trước mỗi kỳ, chọn phương pháp z ≥ 1,5 ở 200 kỳ gần và z ≥ 0 ở 300 kỳ trước đó → gộp phiếu → 2 số; kiểm từng kỳ, chỉ dùng dữ liệu trước nó.
Chạy: python3 research/form_lucky.py [--json out.json]"""
import sys, os, math, json, random
sys.path.insert(0, os.path.dirname(__file__))
from study import load
from report import all_rules
from lucky import rules as lrules, contexts, L

mx, c, _, dr = load('loto535'); n = len(dr); W = [d['lucky'] for d in dr]
M = {}
for k, f in all_rules(L).items(): M['Ngày: ' + k] = [f(d['info']) for d in dr]
ctx = contexts(dr)
for k, f in lrules().items(): M['May mắn: ' + k] = [f(x) for x in ctx]
M = {k: v for k, v in M.items() if sum(map(len, v))}
names = list(M)
pre = {}
for k in names:
    H = [0.0]; E = [0.0]; V = [0.0]
    for S, w in zip(M[k], W):
        p = len(S)/L; H.append(H[-1] + (w in S)); E.append(E[-1] + p); V.append(V[-1] + p*(1-p))
    pre[k] = (H, E, V)
def seg(k, a, b):
    H, E, V = pre[k]; h, e, v = H[b]-H[a], E[b]-E[a], V[b]-V[a]
    return h, e, ((h-e)/math.sqrt(v) if v > 0 else 0.0)

# (A) đấu loại 500 kỳ gần: chọn 300 / kiểm 200
A = n-500; rows = []
for k in names:
    hs, es, zs = seg(k, A, A+300); hv, ev, zv = seg(k, A+300, n)
    if es and ev: rows.append(dict(rule=k, size=round(sum(len(s) for s in M[k][A:])/500, 1), sel_z=round(zs, 2), sel_lift=round(hs/es, 3),
                                   val_hits=int(hv), val_exp=round(ev, 1), val_lift=round(hv/ev, 3), val_z=round(zv, 2)))
rows.sort(key=lambda r: -r['sel_z'])
xs = [r['sel_z'] for r in rows]; ys = [r['val_z'] for r in rows]; mxs, mys = sum(xs)/len(xs), sum(ys)/len(ys)
corr = sum((a-mxs)*(b-mys) for a, b in zip(xs, ys))/math.sqrt(sum((a-mxs)**2 for a in xs)*sum((b-mys)**2 for b in ys))

# (B) phong độ, đi từng kỳ
RW, PW, TEST = 200, 300, 300
def select(t):
    a = max(0, t-RW); b0 = max(0, a-PW); out = []
    for k in names:
        h, e, z = seg(k, a, t)
        if e <= 0 or z < 1.5: continue
        if a-b0 >= 50 and seg(k, b0, a)[2] < 0: continue
        out.append((k, h/e))
    return out
def top2(t, rng, sel):
    sc = [0.0]*(L+1)
    for k, lift in sel:
        S = M[k][t]
        for x in S: sc[x] += 1 + 0.2*math.log(lift)
    tie = [rng.random()*1e-3 for _ in range(L+1)]
    return sorted(range(1, L+1), key=lambda x: -(sc[x]+tie[x]))[:2]
hit = hitR = nsel = 0; rng = random.Random(9); rr = random.Random(10)
for t in range(n-TEST, n):
    sel = select(t); nsel += len(sel)
    hit += W[t] in top2(t, rng, sel)
    hitR += W[t] in rr.sample(range(1, L+1), 2)
form = dict(n=TEST, hit=hit, rate=round(100*hit/TEST, 1), rnd=round(100*hitR/TEST, 1), nsel=round(nsel/TEST, 1))

if __name__ == '__main__':
    print(f'Số may mắn Loto: {len(names)} phương pháp. Đấu loại 500 kỳ gần (chọn 300 / kiểm 200): tương quan hạng r = {corr:+.3f}')
    print('TOP 10 lúc chọn → lúc kiểm:')
    for r in rows[:10]: print(f"  {r['rule'][:55]:55s} chọn {100*(r['sel_lift']-1):+4.0f}% z{r['sel_z']:+.2f} | kiểm {100*(r['val_lift']-1):+4.0f}% z{r['val_z']:+.2f}")
    print('TOP 10 của 200 kỳ gần nhất:')
    for r in sorted(rows, key=lambda r: -r['val_z'])[:10]: print(f"  {r['rule'][:55]:55s} {r['val_hits']}/{r['val_exp']} {100*(r['val_lift']-1):+4.0f}% z{r['val_z']:+.2f} | 300 kỳ trước z{r['sel_z']:+.2f}")
    print(f"Phong độ gần đây (2 số, đi từng kỳ {TEST} kỳ): trúng {form['hit']}/{TEST} = {form['rate']}% | 2 số ngẫu nhiên {form['rnd']}% | lý thuyết 16.7% | PP/kỳ {form['nsel']}")
    if '--json' in sys.argv:
        json.dump(dict(corr=round(corr, 3), rows=rows, form=form), open(sys.argv[sys.argv.index('--json')+1], 'w'), ensure_ascii=False); print('đã ghi')
