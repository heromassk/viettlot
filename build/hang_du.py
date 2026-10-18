#!/usr/bin/env python3
"""Đoán DẠNG chia hàng kỳ tới (bao nhiêu số ở 0x, 1x, 2x…) từ các kỳ trước (anh 14/10/2026).
Mỗi cách cho một danh sách dạng xếp theo khả năng; chấm % kỳ dạng thật nằm trong top 1 / 3 / 5 / 10 của cách đó,
chạy tiến (mỗi kỳ chỉ học các kỳ trước), khung 10 / 20 / 50 / 100 kỳ gần. Thêm: đoán hàng vắng, hàng ra ≥2.
  python build/hang_du.py power|mega|loto"""
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
L = 200   # số kỳ học

def m_tansuat(t):
    c = Counter(C[t - L:t]); return {p: c.get(p, 0) + 0.01 for p in ALL}
def per(t, cond_prev=True, recent=0):
    """xác suất số lượng từng hàng: theo số lượng kỳ trước (200 kỳ), trộn thêm 20 kỳ gần nếu recent>0."""
    P = []
    for i in range(NH):
        cc = Counter(C[u][i] for u in range(t - L, t) if not cond_prev or C[u - 1][i] == C[t - 1][i])
        if sum(cc.values()) < 15: cc = Counter(C[u][i] for u in range(t - L, t))
        n = sum(cc.values()); pr = {k: (cc.get(k, 0) + 0.5) / (n + 0.5 * (KB + 1)) for k in range(KB + 1)}
        if recent:
            rc = Counter(C[u][i] for u in range(t - 20, t)); pr = {k: (1 - recent) * pr[k] + recent * (rc.get(k, 0) + 0.5) / (20 + 0.5 * (KB + 1)) for k in pr}
        P.append(pr)
    out = {}
    for p in ALL:
        v = 1.0
        for i in range(NH): v *= P[i][p[i]]
        out[p] = v
    return out
def m_hang(t): return per(t, False)
def m_hang_truoc(t): return per(t, True)
def m_hang_truoc_gan(t): return per(t, True, 0.4)
def m_gan(t):   # 20 kỳ gần, không theo kỳ trước
    return per(t, False, 1.0)
def m_lang_gieng(t, K=25):
    """kỳ quá khứ có 2 kỳ trước giống 2 kỳ trước của kỳ này nhất → dạng của kỳ kế tiếp chúng"""
    cur = C[t - 1] + C[t - 2]
    ds = sorted(range(t - L, t), key=lambda u: sum(abs(a - b) for a, b in zip(C[u - 1] + C[u - 2], cur)))[:K]
    c = Counter(C[u] for u in ds); base = m_hang(t)
    return {p: c.get(p, 0) + base[p] * 3 for p in ALL}
M = {'Dạng hay gặp 200 kỳ': m_tansuat, 'Từng hàng hay ra (200 kỳ)': m_hang, 'Từng hàng theo kỳ trước': m_hang_truoc,
     'Từng hàng theo kỳ trước + 20 kỳ gần': m_hang_truoc_gan, 'Từng hàng theo 20 kỳ gần': m_gan, 'Giống 2 kỳ trước nhất (25 kỳ)': m_lang_gieng}
WS = (10, 20, 50, 100); TOPS = (1, 3, 5, 10)
RK = {nm: {} for nm in M}
for t in range(T - 100, T + 1):
    for nm, f in M.items():
        sc = f(t); RK[nm][t] = sorted(ALL, key=lambda p: -sc[p])
print(f'## {GAME} — đoán dạng chia hàng ({"-".join(f"{h}x" for h in H)}), {len(ALL)} dạng có thể, đến {DT[-1]}\n')
print('### % kỳ dạng thật nằm trong top 1 / 3 / 5 / 10 dạng đoán (khung 10 / 20 / 50 / 100 kỳ)\n')
print('| Cách | Top 1 | Top 3 | Top 5 | Top 10 |\n|---|---|---|---|---|')
for nm in M:
    cells = []
    for k in TOPS:
        cells.append(' / '.join(f"{sum(C[t] in RK[nm][t][:k] for t in range(T - W, T)) * 100 // W}" for W in WS))
    print(f'| {nm} | ' + ' | '.join(cells) + ' |')
# đoán từng hàng: vắng / ≥2 — theo cách "Từng hàng theo kỳ trước + 20 kỳ gần"
print('\n### Đoán từng hàng (cách "theo kỳ trước + 20 kỳ gần"): % kỳ đoán đúng hàng VẮNG / hàng RA ≥2 số (khung 10 / 20 / 50 / 100)\n')
def marg(t):
    sc = per(t, True, 0.4); z = sum(sc.values())
    return [{k: sum(v for p, v in sc.items() if p[i] == k) / z for k in range(KB + 1)} for i in range(NH)]
MG = {t: marg(t) for t in range(T - 100, T + 1)}
print('| Hàng | Đoán vắng khi P(vắng) ≥ 50%: đúng | số lần đoán (100 kỳ) | Đoán ra ≥2 khi P(≥2) ≥ 50%: đúng | số lần (100 kỳ) |\n|---|---|---|---|---|')
for i, h in enumerate(H):
    def acc(test, ok):
        out = []
        for W in WS:
            ts = [t for t in range(T - W, T) if test(t)]; out.append(f"{sum(ok(t) for t in ts) * 100 // len(ts)}%" if ts else '—')
        return ' / '.join(out), sum(1 for t in range(T - 100, T) if test(t))
    a, na = acc(lambda t: MG[t][i][0] >= 0.5, lambda t: C[t][i] == 0)
    b, nb = acc(lambda t: sum(v for k, v in MG[t][i].items() if k >= 2) >= 0.5, lambda t: C[t][i] >= 2)
    print(f'| {h}x | {a} | {na} | {b} | {nb} |')
print(f"\n### Kỳ tới (sau {DT[-1]}: {'-'.join(map(str, C[-1]))})\n")
for nm in M: print(f"- {nm}: " + ' · '.join('-'.join(map(str, p)) for p in RK[nm][T][:5]))
m = MG[T]
print('\nXác suất từng hàng (cách theo kỳ trước + 20 kỳ gần): ' + ' · '.join(f"{h}x: vắng {m[i][0] * 100:.0f}%, 1 số {m[i][1] * 100:.0f}%, ≥2 {sum(v for k, v in m[i].items() if k >= 2) * 100:.0f}%" for i, h in enumerate(H)))

# ---------- Bộ lọc dạng: ghép các luật hàng đạt ≥70% (hang_dauvet.py) ----------
def idx(h): return H.index(h)
def run0(i, t):
    g = 0
    while g < t and C[t - 1 - g][i] == 0: g += 1
    return g
def avg(i, t): return sum(C[u][i] for u in range(t - 10, t)) / 10 / SZ[i]
# luật: (tên, điều kiện kỳ t, hàm kiểm dạng p)
LU = [('Không hàng nào ≥4 số', lambda t: True, lambda t, p: max(p) <= 3),
      ('Dạng khác kỳ trước', lambda t: True, lambda t, p: p != C[t - 1])]
def vang_co(h): return (f'{h}x vắng kỳ trước → có ≥1', lambda t, i=idx(h): C[t - 1][i] == 0, lambda t, p, i=idx(h): p[i] >= 1)
def nhieu_it(h, m=2): return (f'{h}x ra ≥{m} kỳ trước → ≤1', lambda t, i=idx(h): C[t - 1][i] >= m, lambda t, p, i=idx(h): p[i] <= 1)
nong = ('Hàng dày nhất 10 kỳ có ≥1', lambda t: True, lambda t, p: p[max(range(NH), key=lambda i: (avg(i, t), -i))] >= 1)
nguoi = ('Hàng thưa nhất 10 kỳ có ≥1', lambda t: True, lambda t, p: p[min(range(NH), key=lambda i: (avg(i, t), i))] >= 1)
vang_lai = ('Hàng vắng kỳ trước: ≥1 hàng ra lại', lambda t: 0 in C[t - 1], lambda t, p: any(p[i] for i in range(NH) if C[t - 1][i] == 0))
co_mat = lambda m: (f'≥{m} hàng có mặt', lambda t: True, lambda t, p: sum(1 for v in p if v) >= m)
het_day = ('Hàng dày nhất kỳ trước không còn dày nhất', lambda t: True, lambda t, p: p[C[t - 1].index(max(C[t - 1]))] < max(p))
LU += {'loto': lambda: [vang_co(1), vang_co(2), vang_co(0), co_mat(3), nhieu_it(0), nhieu_it(3), nong, vang_lai],
       'mega': lambda: [vang_co(3), vang_co(0), nguoi, nong, co_mat(4), vang_lai],
       'power': lambda: [nhieu_it(5), nhieu_it(1), nhieu_it(3), nhieu_it(2, 3), vang_lai, het_day]}[GAME]()
if os.environ.get('MANH') == '1':   # chỉ giữ luật đúng ≥85% ở cả 50 & 100 kỳ (đo trước kỳ đang xét: dùng 50/100 kỳ gần nhất)
    def _ac(cond, ok, W):
        ts = [t for t in range(T - W, T) if cond(t)]; return sum(ok(t, C[t]) for t in ts) / len(ts) * 100 if ts else 0
    LU = [x for x in LU if _ac(x[1], x[2], 50) >= 85 and _ac(x[1], x[2], 100) >= 85]
FREQ = Counter(C[T - 400:T - 200]) if T > 400 else Counter(C[:T - 200])
def loc(t): return [p for p in ALL if all(ok(t, p) for _, cond, ok in LU if cond(t))]
print('\n### Bộ lọc dạng (ghép các luật hàng đạt) — khung 10 / 20 / 50 / 100 kỳ\n')
print('Luật ghép: ' + ' · '.join(nm for nm, _, _ in LU) + '\n')
ok_all = {t: C[t] in loc(t) for t in range(T - 100, T)}
def giu(t):   # phần dạng giữ lại, tính theo độ hay gặp của dạng ở 200 kỳ trước đó
    c = Counter(C[t - L:t]); ks = set(loc(t)); return sum(v for p, v in c.items() if p in ks) / L
print('| | 10 kỳ | 20 kỳ | 50 kỳ | 100 kỳ |\n|---|---|---|---|---|')
print('| Dạng thật lọt bộ lọc (% kỳ) | ' + ' | '.join(f"{sum(ok_all[t] for t in range(T - W, T)) * 100 // W}%" for W in WS) + ' |')
print('| Dạng giữ lại (tính theo độ hay gặp) | ' + ' | '.join(f"{sum(giu(t) for t in range(T - W, T)) / W * 100:.0f}%" for W in WS) + ' |')
print('| Số dạng giữ lại / tổng | ' + ' | '.join(f"{sum(len(loc(t)) for t in range(T - W, T)) / W:.0f}/{len(ALL)}" for W in WS) + ' |')
for nm, cond, ok in LU:
    r = []
    for W in WS:
        ts = [t for t in range(T - W, T) if cond(t)]; r.append(f"{sum(ok(t, C[t]) for t in ts) * 100 // len(ts)}%" if ts else '—')
    print(f"| · {nm} | " + ' | '.join(r) + ' |')
act = [nm for nm, cond, _ in LU if cond(T)]
LT = loc(T); best = RK['Từng hàng theo kỳ trước + 20 kỳ gần'][T]
LT = sorted(LT, key=best.index)
print(f"\nKỳ tới — luật đang áp: {' · '.join(act)}")
print(f"Còn {len(LT)}/{len(ALL)} dạng; 10 dạng khả năng nhất: " + ' · '.join('-'.join(map(str, p)) for p in LT[:10]))
