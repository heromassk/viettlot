"""Số / cặp số về nhiều trong N kỳ gần nhất: chọn trước mỗi kỳ, xem có trúng hơn ngẫu nhiên không (kỳ cũ vs kỳ mới)."""
import sys, os, math
from math import comb
from collections import Counter
from itertools import combinations
sys.path.insert(0, os.path.dirname(__file__))
from study import load

def pick(past, mx, mode, k):
    """Tập dự đoán từ các kỳ trước (past). 'num' = k số nóng, 'cold' = k số lạnh, 'pair' = k cặp hay về cùng."""
    if mode == 'pair':
        pc = Counter(p for s in past for p in combinations(sorted(s), 2))
        return sorted(pc, key=lambda p: (-pc[p], -max(j for j, s in enumerate(past) if p[0] in s and p[1] in s), p))[:k]
    f = Counter(x for s in past for x in s)
    last = {x: max((j for j, s in enumerate(past) if x in s), default=-1) for x in range(1, mx+1)}
    sign = -1 if mode == 'num' else 1
    return sorted(range(1, mx+1), key=lambda x: (sign*f.get(x, 0), -last[x], x))[:k]

def test(D, c, mx, lo, hi, window, mode, k):
    """mode 'num': chọn k số về nhiều nhất trong window kỳ trước; 'pair': k cặp về cùng nhiều nhất; 'cold': k số về ít nhất."""
    hit = tot = 0
    for i in range(lo, hi):
        past = D[max(0, i-window):i] if window else D[:i]
        if mode == 'pair':
            pc = Counter(p for s in past for p in combinations(sorted(s), 2))
            best = sorted(pc, key=lambda p: (-pc[p], -max(j for j, s in enumerate(past) if p[0] in s and p[1] in s), p))[:k]
            hit += sum(a in D[i] and b in D[i] for a, b in best); tot += len(best)
        else:
            f = Counter(x for s in past for x in s)
            last = {x: max((j for j, s in enumerate(past) if x in s), default=-1) for x in range(1, mx+1)}
            sign = -1 if mode == 'num' else 1
            best = sorted(range(1, mx+1), key=lambda x: (sign*f.get(x, 0), -last[x], x))[:k]
            hit += len(set(best) & D[i]); tot += len(best)
    pr = comb(c, 2)/comb(mx, 2) if mode == 'pair' else c/mx
    E = tot*pr; z = (hit-E)/math.sqrt(E*(1-pr)) if E else 0
    return hit, E, z

LABEL = {'num': 'Số NÓNG', 'cold': 'Số LẠNH', 'pair': 'Cặp hay về cùng'}
def rule_name(mode, w): return f"{LABEL[mode]} {'từ đầu' if w is None else f'{w} kỳ gần'}"

if __name__ == '__main__' and '--json' in sys.argv:
    import json, random
    out, dump = {}, {}
    for game in ['power655', 'mega645', 'loto535']:
        mx, c, _, dr = load(game); D = [set(d['nums']) for d in dr]; n = len(D); start = 50; cut = start + int((n-start)*0.6)
        rows = []
        for mode, k in [('num', c), ('cold', c), ('pair', 10)]:
            for w in (5, 10, 20, 30, 50, 100, None):
                a = test(D, c, mx, start, cut, w, mode, k); b = test(D, c, mx, cut, n, w, mode, k); t = test(D, c, mx, start, n, w, mode, k)
                rows.append(dict(rule=rule_name(mode, w), mode=mode, window=w, k=k, hits=t[0], expected=round(t[1], 1), lift=round(t[0]/t[1], 3),
                                 z=round(t[2], 2), p=round(math.erfc(abs(t[2])/math.sqrt(2)), 4), z_old=round(a[2], 2), z_new=round(b[2], 2), consistent=a[2]*b[2] > 0, size=None))
        out[game] = rows
        rng = random.Random(4); idx = [n] + rng.sample(range(60, n), 15)
        dump[game] = {i: {r['rule']: [list(x) if isinstance(x, tuple) else x for x in pick(D[:i] if r['window'] is None else D[max(0, i-r['window']):i], mx, r['mode'], r['k'])] for r in rows} for i in idx}
    json.dump(out, open(sys.argv[sys.argv.index('--json')+1], 'w'), ensure_ascii=False)
    if '--dump' in sys.argv: json.dump(dump, open(sys.argv[sys.argv.index('--dump')+1], 'w'))
    print('đã ghi')
elif __name__ == '__main__':
    for game in ['power655', 'mega645', 'loto535']:
        mx, c, _, dr = load(game); D = [set(d['nums']) for d in dr]; n = len(D); start = 50; cut = start + int((n-start)*0.6)
        print(f'\n######## {game}: kiểm {n-start} kỳ (cũ {cut-start}, mới {n-cut})')
        for mode, k, label in [('num', c, f'{c} số NÓNG'), ('cold', c, f'{c} số LẠNH'), ('pair', 10, '10 cặp hay về cùng')]:
            for w in (5, 10, 20, 30, 50, 100, None):
                a = test(D, c, mx, start, cut, w, mode, k); b = test(D, c, mx, cut, n, w, mode, k); t = test(D, c, mx, start, n, w, mode, k)
                ok = a[2]*b[2] > 0 and abs(t[2]) >= 1.5
                print(f"  {label:20s} {('từ đầu' if w is None else f'{w} kỳ gần'):>10s}: toàn {t[0]:4d}/{t[1]:6.1f} ({(t[0]/t[1]-1)*100:+4.0f}%, z {t[2]:+.2f}) | cũ z {a[2]:+.2f} mới z {b[2]:+.2f} {'★ HY VỌNG NHỎ' if ok and t[2]>0 else ('▼ nên tránh' if ok else '')}")
