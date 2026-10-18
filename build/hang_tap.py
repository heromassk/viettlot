#!/usr/bin/env python3
"""Nhóm DẠNG CHIA HÀNG có tỉ lệ về cao cho kỳ tới, dựng từ dữ liệu quá khứ (anh 14/10/2026).
Mỗi hàng: kỳ sau ra mấy số tùy theo kỳ trước hàng đó ra mấy số (và 2 kỳ trước) — học 200 kỳ trước kỳ đang xét.
Ghép các hàng → xác suất từng dạng → lấy các dạng khả năng cao nhất cho tới khi cộng dồn đạt ngưỡng (50/70/80%).
Chấm lùi (chạy tiến): % kỳ dạng thật nằm trong nhóm + nhóm trung bình mấy dạng, khung 10 / 20 / 50 / 100 kỳ.
  python build/hang_tap.py power|mega|loto"""
import json, os, sys, itertools
from collections import Counter
B = os.path.dirname(os.path.abspath(__file__))
GAME = sys.argv[1]
key, NB, KB = {'power': ('power655', 55, 6), 'mega': ('mega645', 45, 6), 'loto': ('loto535', 35, 5)}[GAME]
D = json.load(open(os.path.join(B, 'all_data.json'), encoding='utf-8'))[key]
R = [sorted(r) for r in D['res']]; DT = D['dates']; T = len(R)
H = list(range(NB // 10 + 1)); NH = len(H)
SZ = [sum(1 for n in range(1, NB + 1) if n // 10 == h) for h in H]
C = [tuple(sum(1 for n in r if n // 10 == h) for h in H) for r in R]
ALL = [p for p in itertools.product(*[range(min(s, KB) + 1) for s in SZ]) if sum(p) == KB]
L = 200; cap = lambda v: min(v, 2)

def model(t, how):
    """xác suất từng dạng cho kỳ t"""
    P = []
    for i in range(NH):
        if how == 'deu':      # từng hàng hay ra bao nhiêu (200 kỳ), không theo kỳ trước
            cc = Counter(C[u][i] for u in range(t - L, t))
        else:
            k1 = cap(C[t - 1][i]); k2 = cap(C[t - 2][i])
            cc = Counter(C[u][i] for u in range(t - L, t) if cap(C[u - 1][i]) == k1 and (how == 'truoc1' or cap(C[u - 2][i]) == k2))
            if sum(cc.values()) < 12:
                cc = Counter(C[u][i] for u in range(t - L, t) if cap(C[u - 1][i]) == k1)
        n = sum(cc.values()); P.append({k: (cc.get(k, 0) + 0.3) / (n + 0.3 * (KB + 1)) for k in range(KB + 1)})
    sc = {}
    for p in ALL:
        v = 1.0
        for i in range(NH): v *= P[i][p[i]]
        sc[p] = v
    z = sum(sc.values()); return {p: v / z for p, v in sc.items()}
def nhom(pr, th):
    out, acc = [], 0.0
    for p in sorted(pr, key=lambda p: -pr[p]):
        out.append(p); acc += pr[p]
        if acc >= th: break
    return out
HOW = {'deu': 'Từng hàng hay ra (không theo kỳ trước)', 'truoc1': 'Theo kỳ trước (1 kỳ)', 'truoc2': 'Theo 2 kỳ trước'}
WS = (10, 20, 50, 100)
PR = {h: {t: model(t, h) for t in range(T - 100, T + 1)} for h in HOW}
print(f'## {GAME} — nhóm dạng chia hàng tỉ lệ cao ({"-".join(f"{h}x" for h in H)}, {len(ALL)} dạng có thể), đến {DT[-1]}\n')
print('Mỗi ô: % kỳ dạng thật nằm trong nhóm · nhóm trung bình mấy dạng — khung 10 / 20 / 50 / 100 kỳ\n')
print('| Cách | Nhóm cộng dồn 50% | Nhóm 70% | Nhóm 80% |\n|---|---|---|---|')
for h, lab in HOW.items():
    cells = []
    for th in (0.5, 0.7, 0.8):
        G = {t: nhom(PR[h][t], th) for t in range(T - 100, T + 1)}
        cells.append(' / '.join(f"{sum(C[t] in G[t] for t in range(T - W, T)) * 100 // W}%·{sum(len(G[t]) for t in range(T - W, T)) / W:.0f}" for W in WS))
    print(f'| {lab} | ' + ' | '.join(cells) + ' |')
# dạng thô: mỗi hàng 0 / 1 / ≥2
print('\n### Dạng THÔ (mỗi hàng: 0 = vắng, 1 = 1 số, 2 = ≥2 số) — cùng cách chấm\n')
def tho(p): return tuple(cap(v) for v in p)
TH = sorted({tho(p) for p in ALL})
print(f'{len(TH)} dạng thô có thể.\n')
print('| Cách | Nhóm 50% | Nhóm 70% | Nhóm 80% |\n|---|---|---|---|')
PRT = {}
for h, lab in HOW.items():
    PRT[h] = {}
    for t in range(T - 100, T + 1):
        q = Counter()
        for p, v in PR[h][t].items(): q[tho(p)] += v
        PRT[h][t] = dict(q)
    cells = []
    for th in (0.5, 0.7, 0.8):
        G = {t: nhom(PRT[h][t], th) for t in range(T - 100, T + 1)}
        cells.append(' / '.join(f"{sum(tho(C[t]) in G[t] for t in range(T - W, T)) * 100 // W}%·{sum(len(G[t]) for t in range(T - W, T)) / W:.0f}" for W in WS))
    print(f'| {lab} | ' + ' | '.join(cells) + ' |')
print(f"\n### Kỳ tới (kỳ trước {DT[-1]}: {'-'.join(map(str, C[-1]))})\n")
for h, lab in HOW.items():
    g = nhom(PRT[h][T], 0.7)
    print(f"- {lab} — nhóm thô 70% ({len(g)} dạng): " + ' · '.join(f"{'-'.join('≥2' if v == 2 else str(v) for v in p)} {PRT[h][T][p] * 100:.0f}%" for p in g[:12]) + (' …' if len(g) > 12 else ''))
