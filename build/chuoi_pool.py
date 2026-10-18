#!/usr/bin/env python3
"""Pool dựng bằng CHUỖI phương pháp tốt nhất mỗi giai đoạn (anh 15/10/2026): từ pool đầy đủ, mỗi giai đoạn lấy cách (trong loai_dan.py)
giữ được nhiều số trúng nhất, bỏ dần tới các cỡ 30,25,20,18,15,12,10; chấm ≥3 số · ≥4 số ở 50 / 100 kỳ gần như pool của app.
  python build/chuoi_pool.py loto|mega|power"""
import os, sys, json
B = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, B)
GAME = sys.argv[1]
src = open(os.path.join(B, 'loai_dan.py'), encoding='utf-8').read()
src = src[:src.index('STAGES = []')]
sys.argv = ['loai_dan.py', GAME]
G = {'__file__': os.path.join(B, 'loai_dan.py'), '__name__': 'x'}
exec(compile(src, 'loai_dan.py', 'exec'), G)
R, T, TS, NB, KB, M, bo, N = G['R'], G['T'], G['TS'], G['NB'], G['KB'], G['M'], G['bo'], G['N']
SIZES = [int(x) for x in os.environ.get('SIZES', '30,25,20,18,15,12,10').split(',')]
P = {t: set(N) for t in TS}; size = NB; PATH = {}
for tgt in SIZES:
    k = size - tgt; best = None
    for nm in M:
        Q = {t: bo(P[t], nm, t, k) for t in TS}
        h1 = sum(len(Q[t] & set(R[t])) for t in TS); h0 = sum(len(P[t] & set(R[t])) for t in TS)
        sc = (h1 / h0 if h0 else 1)
        if best is None or sc > best[0]: best = (sc, nm, Q)
    P = best[2]; size = tgt; PATH[tgt] = (best[1], best[0], {t: set(P[t]) for t in TS})
def st(PP):
    o = []
    for W in (50, 100):
        hs = [len(PP[t] & set(R[t])) for t in range(T - W, T)]
        o += [sum(h >= 3 for h in hs) * 100 // W, sum(h >= 4 for h in hs) * 100 // W, round(sum(hs) / W, 2)]
    return o
# pool của app (bộ cộng điểm riêng từng cỡ) để so
sys.argv = ['pool_chon.py', GAME]
os.environ['KS'] = ','.join(map(str, sorted(set(SIZES) & {10, 12, 15, 18, 20, 25}))) or '10'
pc = open(os.path.join(B, 'pool_chon.py'), encoding='utf-8').read(); pc = pc[:pc.index("print(f'## ")]
GP = {'__file__': os.path.join(B, 'pool_chon.py'), '__name__': 'x'}
exec(compile(pc, 'pool_chon.py', 'exec'), GP)
ranks = GP['ranks']
PCJ = json.load(open(os.path.join(B, 'pool_chon.json'), encoding='utf-8'))[GAME]
def sc2(s): return (s['50'][1] * 2 + s['100'][1], s['50'][0] * 2 + s['100'][0])
print(f'## {GAME} — pool dựng bằng chuỗi phương pháp tốt nhất mỗi giai đoạn, đến {G["DATES"][-1]}\n')
print('Mỗi ô: % kỳ trúng ≥3 số · % kỳ trúng ≥4 số · TB số trúng/kỳ, khung 50 kỳ | 100 kỳ\n')
print('| Pool | Chuỗi (cách bỏ ở giai đoạn này) | Pool từ chuỗi | Pool của app |\n|---|---|---|---|')
for tgt in SIZES:
    nm, ret, PP = PATH[tgt]
    a = st(PP)
    app = '— | —'
    K = str(tgt)
    if K in PCJ.get('chon', {}) :
        s1, s2 = PCJ['stat'].get(K), PCJ.get('stat50', {}).get(K)
        CH = PCJ['chon50'][K] if s1 and s2 and sc2(s2) > sc2(s1) else PCJ['chon'][K]
        rk = ranks([tuple(x) for x in CH])
        b = st({t: set(rk[t][:tgt]) for t in range(T - 100, T)})
        app = f'{b[0]}·{b[1]}·{b[2]} | {b[3]}·{b[4]}·{b[5]}'
    print(f'| {tgt} | {nm.replace(" (có trong PP → giữ)", "")} ({ret * 100:.0f}% giữ) | {a[0]}·{a[1]}·{a[2]} | {a[3]}·{a[4]}·{a[5]} | {app} |')

# ---- Lai: chuỗi bỏ tới cỡ HY rồi để điểm của app xếp hạng tiếp trong số còn lại ----
HY = [int(x) for x in os.environ.get('HY', '30,25').split(',')]
GY2, SIG2, NUMS2 = GP['GY'], GP['SIG'], GP['NUMS']
def app_full(t, K, CHset):
    e = {}
    for nm, w in CHset:
        for n in NUMS2[t].get(nm, ()): e[n] = e.get(n, 0) + w
    f, s = SIG2[t]; return GY2['pool_of'](GY2['score'](f, s, e), s, NB)
print('\n### Lai: chuỗi bỏ tới cỡ H, rồi điểm của app chọn tiếp trong số còn lại (50 kỳ | 100 kỳ)\n')
print('| Pool | Cỡ H | Lai 50 kỳ | Lai 100 kỳ | App 50 kỳ | App 100 kỳ |\n|---|---|---|---|---|---|')
for tgt in sorted(set(SIZES) & {10, 12, 15, 18, 20, 25}, reverse=True):
    K = str(tgt)
    s1, s2 = PCJ['stat'].get(K), PCJ.get('stat50', {}).get(K)
    CH = [tuple(x) for x in (PCJ['chon50'][K] if s1 and s2 and sc2(s2) > sc2(s1) else PCJ['chon'][K])]
    rk = ranks(CH)
    app = st({t: set(rk[t][:tgt]) for t in range(T - 100, T)})
    for H in HY:
        if H <= tgt or H not in PATH: continue
        PH = PATH[H][2]
        pp = {}
        for t in range(T - 100, T):
            full = app_full(t, tgt, CH)
            sel = [n for n in full if n in PH[t]][:tgt]
            sel += [n for n in full if n not in sel][:tgt - len(sel)]
            pp[t] = set(sel)
        b = st(pp)
        print(f'| {tgt} | {H} | {b[0]}·{b[1]}·{b[2]} | {b[3]}·{b[4]}·{b[5]} | {app[0]}·{app[1]}·{app[2]} | {app[3]}·{app[4]}·{app[5]} |')
