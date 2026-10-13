"""Ghép các phép LOẠI trong Pool 25 Power (anh 13/10/2026: "làm hết đi rồi chấm quá khứ").
Lớp A: gộp Markov chung 3+5 + hồi quy 50 (cộng hạng trong pool) bỏ a số thấp nhất.
Lớp B: tâm linh — bỏ số có đúng v phiếu (phiếu quá khứ: build/tamlinh_ls_power.json từ tamlinh_ls.js).
Chấm 100 kỳ gần (2 nửa 50·50). python3 build/pool25_ghep.py"""
import json, os, numpy as np
B = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(B, 'pool25_markovloai.py')).read(); src = src[:src.index('M = {')]
g = {'__file__': os.path.join(B, 'pool25_markovloai.py')}; exec(src, g)
R, T, pool, mk, hq = g['R'], g['T'], g['pool'], g['mk_chung'], g['hq']
D = json.load(open(os.path.join(B, 'all_data.json')))['power655']['dates']
TL = {e['date']: e['vt'] for e in json.load(open(os.path.join(B, 'tamlinh_ls_power.json')))}
# đối chiếu: phiếu chấm lại phải khớp phiếu thật đã lưu trong sổ Pool 25 (lỗi 13/10: lệch 38/55 số mà không ai biết)
_lech = [e['ky'] for e in map(json.loads, open(os.path.join(B, 'pool25_power_log.jsonl'))) if 'vt' in e and e['ky'] in TL and TL[e['ky']] != e['vt']]
if _lech: raise SystemExit(f'DỪNG: phiếu tâm linh chấm lại lệch phiếu thật ở kỳ {_lech} — chạy lại node build/tamlinh_ls.js power')
TS = list(range(T - 100, T)); P = {t: pool(t) for t in TS}
def hangA(t):                             # tổng hạng 3 cách trong pool (thấp = loại trước)
    p = P[t]; tot = {n: 0 for n in p}
    for s in (mk(t, 3), mk(t, 5), hq(t, 50)):
        o = sorted(range(25), key=lambda i: (s[p[i] - 1], -i))
        for k, i in enumerate(o): tot[p[i]] += k
    return tot
HA = {t: hangA(t) for t in TS}
def loaiA(t, keep, a):
    if not a: return keep
    o = sorted(keep, key=lambda n: (HA[t][n], -P[t].index(n))); return [n for n in keep if n not in o[:a]]
def loaiB(t, keep, rule):
    vt = TL[D[t]]
    if rule is None: return keep
    if rule == 'b3': return [n for n in keep if vt[n] != 3]
    if rule == 'le3': return [n for n in keep if vt[n] > 3]
    if rule == 'b2': return [n for n in keep if vt[n] != 2]
    if rule.startswith('thap'):            # bỏ k số ít phiếu nhất
        k = int(rule[4:]); o = sorted(keep, key=lambda n: (vt[n], -P[t].index(n))); return [n for n in keep if n not in o[:k]]
def cham(fn):
    h, sz, bo_h, bo_n = [], [], 0, 0
    for t in TS:
        keep = fn(t); h.append(len(R[t] & set(keep))); sz.append(len(keep))
        bo = set(P[t]) - set(keep); bo_h += len(R[t] & bo); bo_n += len(bo)
    h = np.array(h)
    return dict(sz=np.mean(sz), g4=(h >= 4).mean() * 100, n1=(h[:50] >= 4).mean() * 100, n2=(h[50:] >= 4).mean() * 100,
                g3=(h >= 3).mean() * 100, tb=h.mean(), bo=100 * bo_h / max(bo_n, 1), t13=int(h[-1]))
KQ = {}
for a in (0, 2, 3, 4, 5):
    for rule in (None, 'b3', 'b2', 'le3', 'thap2', 'thap3', 'thap5'):
        KQ[f'A{a}·{rule}'] = cham(lambda t, a=a, rule=rule: loaiB(t, loaiA(t, P[t], a), rule))
        KQ[f'{rule}·A{a}'] = cham(lambda t, a=a, rule=rule: loaiA(t, loaiB(t, P[t], rule), a))
json.dump(KQ, open(os.path.join(B, 'pool25_ghep.json'), 'w'), ensure_ascii=False, default=float)
for m, d in sorted(KQ.items(), key=lambda x: (round(x[1]['sz']), -x[1]['g4'])):
    print(f"{m:16s} còn {d['sz']:4.1f}: ≥4 {d['g4']:3.0f}% ({d['n1']:.0f}·{d['n2']:.0f}) ≥3 {d['g3']:3.0f}% TB {d['tb']:.2f} | bị loại ra {d['bo']:.1f}%")
