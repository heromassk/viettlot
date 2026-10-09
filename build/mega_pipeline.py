"""Pipeline Mega nhiều tầng (anh, 09/10/2026) — chỉ dùng ≤200 kỳ gần nhất.
Tầng 1 cộng/trừ: khoảng cách tới số kỳ trước (±0..±5), phiếu ±1 qua 5 kỳ, ±13/±14 qua 5 kỳ.
Tầng 2 luật khác: nhịp vắng, độ nóng 10/20/100, lien2, lt3, zprev, kép, lộn, cùng đuôi.
Tầng 3 tâm linh: cộng điểm cố định lúc gợi ý (không có lịch sử để học).
Học trọng số: hồi quy logistic, mỗi kỳ học trên 100 kỳ ngay trước nó, khởi đầu từ trọng số kỳ trước
(đổi từ từ). Chấm 100 kỳ gần nhất → tổng 200 kỳ.
Dùng: python3 build/mega_pipeline.py [--goiy recs.json] [--linh 15,36]"""
import json, math, sys, os
from itertools import combinations
HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, 'all_data.json')))['mega645']
R = [set(r) for r in D['res']]; T = len(R); NB = 45
arg = sys.argv[1:]
GREC = json.load(open(arg[arg.index('--goiy') + 1])) if '--goiy' in arg else None
LINH = [int(x) for x in arg[arg.index('--linh') + 1].split(',')] if '--linh' in arg else []

def lon(n): return int(f'{n:02d}'[::-1])
NAMES = ['d0', 'd1', 'd2', 'd3', 'd4', 'd5', 'v1', 'v1314', 'g1', 'g2_5', 'g6_10', 'g11_15', 'g16_25', 'g26',
         'c10', 'c20', 'c100', 'lien2', 'lt3', 'zprev', 'kep', 'lon', 'duoi']
def feats(t):
    last = R[t - 1]; out = {}
    for n in range(1, NB + 1):
        d = min(abs(n - x) for x in last)
        g = 0
        while g < 200 and n not in R[t - 1 - g]: g += 1
        g += 1
        v1 = sum((n - 1 in R[t - j]) + (n + 1 in R[t - j]) for j in range(1, 6))
        v13 = sum(sum((n + s * k) in R[t - j] for s in (1, -1) for k in (13, 14)) for j in range(1, 6))
        c = lambda w: sum(n in R[t - j] for j in range(1, w + 1))
        out[n] = [d == 0, d == 1, d == 2, d == 3, d == 4, d == 5, v1 / 2, v13 / 2,
                  g == 1, 2 <= g <= 5, 6 <= g <= 10, 11 <= g <= 15, 16 <= g <= 25, g > 25,
                  c(10) / 2, c(20) / 3, c(100) / 13, n in last and n in R[t - 2], n in last and n in R[t - 3],
                  n == max(last), n % 11 == 0, lon(n) in last and lon(n) != n, n not in last and n % 10 in {x % 10 for x in last}]
        out[n] = [float(x) for x in out[n]]
    return out
LOAI = lambda t: (R[t - 1] & R[t - 2]) | (R[t - 1] & R[t - 3]) | {max(R[t - 1])}   # giữ 3 luật loại Mega đang dùng

START = T - 200
F = {t: feats(t) for t in range(START, T + 1)}
K = len(NAMES)
def p_of(w, x): z = w[-1] + sum(a * b for a, b in zip(w, x)); return 1 / (1 + math.exp(-max(-30, min(30, z))))
def fit(w, ts, ep=8, lr=0.005, l2=0.01):   # học chậm (09/10: lr 0.05 → 1,50; 0.005 → 1,77)
    w = list(w)
    for _ in range(ep):
        for t in ts:
            for n, x in F[t].items():
                e = p_of(w, x) - (n in R[t])
                for i in range(K): w[i] -= lr * (e * x[i] + l2 * w[i])
                w[-1] -= lr * e
    return w

def parts12():
    def rec(rest):
        if not rest: yield []; return
        a = rest[0]
        for b, c in combinations(rest[1:], 2):
            for tail in rec([x for x in rest[1:] if x not in (b, c)]): yield [(a, b, c)] + tail
    return list(rec(list(range(12))))
P12 = parts12()
def mt(nums):
    w = {n: 12 - i for i, n in enumerate(nums)}; best = None
    for pt in P12:
        gs = [[nums[i] for i in g] for g in pt]
        tks = [sorted(a + b) for a, b in combinations(gs, 2)]
        bad = sum(abs(sum(x % 2 for x in tk) - 3) > 1 for tk in tks) * 100 + sum(sum(x % 11 == 0 for x in tk) >= 2 for tk in tks)
        sw = [sum(w[x] for x in tk) for tk in tks]; v = (bad, max(sw) - min(sw))
        if best is None or v < best[0]: best = (v, tks)
    return best[1]
def top20(t):   # máy học chỉ xếp lại trong top 20 của cách hiện tại (goiy.py)
    if GREC and t < T: return set(GREC[t - T]["rk"])
    if t == T and os.path.exists(os.path.join(HERE, 'goiy_latest', 'mega.json')): return set(json.load(open(os.path.join(HERE, 'goiy_latest', 'mega.json')))['rank'][:20])
    return set(range(1, NB + 1))
def pool12(w, t, extra=None):
    lo = LOAI(t); tp = top20(t); sc = {n: p_of(w, x) + (n in tp) + (extra or {}).get(n, 0) for n, x in F[t].items() if n not in lo}
    out, kep = [], 0
    for n in sorted(sc, key=lambda n: (-sc[n], n)):
        if n % 11 == 0:
            if kep: continue
            kep += 1
        out.append(n)
        if len(out) == 12: break
    return out, sc

# Walk-forward 100 kỳ cuối: học trên 100 kỳ trước mỗi kỳ, trọng số chuyển tiếp
w = fit([0.0] * (K + 1), range(START, START + 100), ep=15)
res = []; MLP = {}
for t in range(START + 100, T):
    pl, _ = pool12(w, t); MLP[t] = pl
    tks = mt(pl)
    res.append((t, len(set(pl) & R[t]), max(len(set(tk) & R[t]) for tk in tks)))
    w = fit(w, [t], ep=1)          # học thêm kỳ vừa ra, đổi từ từ
    w0 = w
def tb(xs, i, W): x = xs[-W:]; return sum(r[i] for r in x) / W, sum(r[i] >= 3 for r in x) / W * 100, sum(r[i] >= 4 for r in x) / W * 100
print('## Pipeline Mega (học trọng số) — chấm lùi 100 kỳ\n')
print('| Khung | Pool12 TB | Pool ≥3 | Pool ≥4 | Ma trận TB | MT ≥3 | MT ≥4 |' + (' Hiện tại pool12 TB | ≥3 | MT TB | MT ≥3 | MT ≥4 |' if GREC else ''))
print('|---|---|---|---|---|---|---|' + ('---|---|---|---|---|' if GREC else ''))
G = []
if GREC:
    for r in GREC[-100:]:
        rk = []; kep = 0
        for n in r['rk']:
            if n % 11 == 0:
                if kep: continue
                kep += 1
            rk.append(n)
            if len(rk) == 12: break
        rr = set(r['r']); G.append((0, len(set(rk) & rr), max(len(set(tk) & rr) for tk in mt(rk))))
for W in (10, 20, 50, 100):
    a = tb(res, 1, W); b = tb(res, 2, W)
    s = f'| {W} | {a[0]:.2f} | {a[1]:.0f}% | {a[2]:.0f}% | {b[0]:.2f} | {b[1]:.0f}% | {b[2]:.0f}% |'
    if G:
        c = tb(G, 1, W); d = tb(G, 2, W); s += f' {c[0]:.2f} | {c[1]:.0f}% | {d[0]:.2f} | {d[1]:.0f}% | {d[2]:.0f}% |'
    print(s)
print('\nHai nửa 50 kỳ (pool12 TB): ' + ' · '.join(f'{sum(r[1] for r in res[i:i+50])/50:.2f}' for i in (0, 50)))
print('\n### Trọng số đã học (kỳ mới nhất)\n\n| Đặc trưng | Trọng số |\n|---|---|')
for nm, v in sorted(zip(NAMES, w), key=lambda x: -abs(x[1])): print(f'| {nm} | {v:+.2f} |')
extra = {n: 0.03 for n in LINH}
pl, sc = pool12(w, T, extra)
print(f'\n### Pool 12 kỳ tới: **{" ".join(f"{n:02d}" for n in sorted(pl))}**\n')
for tk in mt(pl): print(' '.join(f'{n:02d}' for n in tk))
tks = mt(pl)
def frame(xs, W): x = xs[-W:]; return [round(sum(r[1] for r in x) / W, 2), round(sum(r[1] >= 3 for r in x) / W * 100), round(sum(r[2] for r in x) / W, 2), round(sum(r[2] >= 3 for r in x) / W * 100)]
# Sổ tiến: chấm pool học đã lưu khi có kết quả mới, rồi lưu pool kỳ tới (cố định cách tính, không sửa lùi)
LOG = os.path.join(HERE, 'hoc_log.jsonl'); log = [json.loads(l) for l in open(LOG)] if os.path.exists(LOG) else []
for e in log:
    if 'trung' not in e and e['t'] < T:
        r = R[e['t']]; e['kq'] = sorted(r); e['trung'] = len(set(e['pool']) & r); e['ve'] = max(len(set(tk) & r) for tk in e['tickets'])
if not log or log[-1]['t'] != T: log.append(dict(t=T, sau=D['dates'][-1], pool=sorted(pl), tickets=tks))
open(LOG, 'w').write(''.join(json.dumps(e, ensure_ascii=False) + '\n' for e in log))
MLP[T] = pl
APP = dict(ml={str(k): v for k, v in MLP.items()}, sau=D['dates'][-1], pool=sorted(pl), tickets=tks, w=sorted(([nm, round(v, 2)] for nm, v in zip(NAMES, w)), key=lambda x: -abs(x[1])),
           bt={W: frame(res, W) for W in (10, 20, 50, 100)}, cur={W: frame(G, W) for W in (10, 20, 50, 100)} if G else {},
           last=[[D['dates'][t], sorted(R[t]), h, v] for t, h, v in res[-10:]], tien=[e for e in log if 'trung' in e][-20:])
json.dump(APP, open(os.path.join(HERE, 'mega_pipeline.json'), 'w'), ensure_ascii=False)
