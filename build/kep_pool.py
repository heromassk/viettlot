#!/usr/bin/env python3
"""Giới hạn SỐ KÉP trong pool (anh 15/10/2026: "đéo tăng xác suất được mà còn giảm"). Pool app từng cỡ (bộ cộng điểm pool_chon.json)
đi theo thứ hạng, bỏ số kép vượt mức c (không giới hạn / ≤2 / ≤1 / 0), lấy số kế tiếp cho đủ cỡ. Chạy tiến 100 kỳ, mỗi kỳ chỉ dùng dữ liệu
trước nó. Áp khi ≥3 và ≥4 số ở cả 50 & 100 kỳ không giảm và có tăng. Ghi build/kep_pool.json (goiy.py đọc). Riêng từng game.
  python build/kep_pool.py loto|mega|power"""
import json, os, sys
B = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, B)
GAME = sys.argv[1]
src = open(os.path.join(B, 'pool_chon.py'), encoding='utf-8').read(); src = src[:src.index('CHON = {}; STAT = {}')]
sys.argv = ['pool_chon.py', GAME]; G = {'__file__': os.path.join(B, 'pool_chon.py'), '__name__': 'x'}
exec(compile(src, 'pool_chon.py', 'exec'), G)
GY, TS, R, T, NB, NUMS, SIG = G['GY'], G['TS'], G['R'], G['T'], G['NB'], G['NUMS'], G['SIG']
PCJ = json.load(open(os.path.join(B, 'pool_chon.json'), encoding='utf-8'))[GAME]
def _sc(st): return (st['50'][1] * 2 + st['100'][1], st['50'][0] * 2 + st['100'][0])
KEP = {n for n in range(11, NB + 1, 11)}
CAPS = (None, 2, 1, 0)
out = {}; DS = G['DS']
print(f'## {GAME} — giới hạn số kép trong pool, 100 kỳ đến {DS[-1]}. Ô = % kỳ ≥3 số · ≥4 số, khung 10 / 20 / 50 / 100\n')
print('| Pool | Không giới hạn | ≤2 kép | ≤1 kép | 0 kép | Áp |\n|---|---|---|---|---|---|')
for K in (10, 12, 15, 18, 20, 25):
    k = str(K); a, b = (PCJ.get('stat') or {}).get(k), (PCJ.get('stat50') or {}).get(k)
    items = PCJ['chon50'][k] if a and b and _sc(b) > _sc(a) else PCJ['chon'].get(k, [])
    RK = {}
    for t in TS:
        e = {}
        for nm, w in items:
            for n in NUMS[t].get(nm, ()): e[n] = e.get(n, 0) + w
        f, s = SIG[t]; RK[t] = GY['pool_of'](GY['score'](f, s, e), s, NB - len(s['vang']))
    HC = (5, 1, 2, 4) if GAME == 'power' and K in (10, 15) else ()   # luật hàng của goiy.py (Power pool 10, 15): hàng ra nhiều 10 kỳ chỉ giữ 1 số
    _NH = lambda h: {n for n in range(1, NB + 1) if n // 10 == h}
    _c10 = lambda h, t: sum(len(R[u] & _NH(h)) for u in range(t - 10, t))
    HON = {t: [h for h in HC if _c10(h, t) >= sorted(_c10(h, u) for u in range(t - 200, t))[160]] for t in TS} if HC else {}
    def pool(t, c):
        o, nk, ch = [], 0, {}
        for n in RK[t]:
            if n // 10 in HON.get(t, ()) and ch.get(n // 10, 0) >= 1: continue
            if n in KEP:
                if c is not None and nk >= c: continue
                nk += 1
            ch[n // 10] = ch.get(n // 10, 0) + 1; o.append(n)
            if len(o) == K: break
        return set(o)
    res = {}
    for c in CAPS:
        st = {}
        for W in (10, 20, 50, 100):
            hs = [len(pool(t, c) & R[t]) for t in range(T - W, T)]; st[W] = (sum(h >= 3 for h in hs), sum(h >= 4 for h in hs))
        res[c] = st
    f = lambda st: ' / '.join(f'{st[W][0] * 100 // W}·{st[W][1] * 100 // W}' for W in (10, 20, 50, 100))
    base = res[None]; best = None
    for c in CAPS[1:]:
        st = res[c]
        if any(st[W][j] < base[W][j] for W in (10, 50, 100) for j in (0, 1)): continue   # + 10 kỳ gần (anh 15/10/2026)
        g = (sum(st[W][1] - base[W][1] for W in (50, 100)), sum(st[W][0] - base[W][0] for W in (50, 100)))
        if g > (0, 0) and (best is None or g > best[0]): best = (g, c)
    if best: out[k] = best[1]
    print(f"| {K} | {f(res[None])} | {f(res[2])} | {f(res[1])} | {f(res[0])} | {('≤' + str(best[1]) + ' kép') if best else 'không'} |")
P = os.path.join(B, 'kep_pool.json'); allc = json.load(open(P, encoding='utf-8')) if os.path.exists(P) else {}
allc[GAME] = dict(cap=out, den=DS[-1]); json.dump(allc, open(P, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(f'\nĐã ghi kep_pool.json [{GAME}]: {out or "không áp cỡ nào"}')
