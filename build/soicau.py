#!/usr/bin/env python3
"""Kiểm các cách "luận số / soi cầu" phổ biến trên mạng bằng dữ liệu Vietlott (chạy tiến, 2 nửa 300 kỳ gần).
  python3 build/soicau.py power|mega|loto
- Cầu vị trí: ghép chữ số ở vị trí i và j của kết quả kỳ trước (các số xếp tăng, viết 2 chữ số) → số; "cầu chạy k ngày"
  = k kỳ liền trước cầu đó đều ra. Người chơi tin cầu đang chạy sẽ chạy tiếp → đo tỉ lệ ra theo độ dài cầu.
- Cầu Pascal: cộng dồn từng cặp chữ số liền nhau (mod 10) tới khi còn 2 chữ số.
- Lô kép (11, 22, 33…), lô gan (vắng lâu), lô rơi (lặp kỳ trước): so tỉ lệ ra mỗi số."""
import json, os, sys
GM = {'power': ('power655', 55, 6), 'mega': ('mega645', 45, 6), 'loto': ('loto535', 35, 5)}
key, NB, KB = GM[sys.argv[1]]
D = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'all_data.json')))[key]
R = [set(r) for r in D['res']]; T = len(R); P = KB / NB * 100
dig = lambda t: ''.join(f'{n:02d}' for n in sorted(R[t]))
L = 2 * KB; pairs = [(i, j) for i in range(L) for j in range(L) if i != j]
def cau(t, i, j):
    d = dig(t); return int(d[i] + d[j])
segs = [(T - 300, T - 150), (T - 150, T)]
print(f'## {key} — kiểm các cách soi cầu (bình quân mỗi số {P:.1f}%)\n')
# 1. Cầu vị trí theo độ dài chuỗi đang chạy
res = {k: [[0, 0], [0, 0]] for k in range(0, 5)}
for si, (a, b) in enumerate(segs):
    for t in range(a, b):
        for (i, j) in pairs:
            run = 0
            for back in range(1, 6):        # cầu đã chạy bao nhiêu kỳ liền tới kỳ t-1
                u = t - back
                v = cau(u - 1, i, j)
                if 1 <= v <= NB and v in R[u]: run += 1
                else: break
            v = cau(t - 1, i, j)
            if not 1 <= v <= NB: continue
            k = min(run, 4); res[k][si][0] += v in R[t]; res[k][si][1] += 1
print('**1. Cầu vị trí (ghép 2 chữ số của kỳ trước): số của cầu ra kỳ này bao nhiêu %, theo số ngày cầu đã chạy**')
for k in range(5):
    a, b = res[k]
    print(f'- Cầu đã chạy {k}{"+" if k == 4 else ""} kỳ: {a[0] / max(a[1], 1) * 100:.1f}% (nửa trước, {a[1]} lần) · {b[0] / max(b[1], 1) * 100:.1f}% (nửa gần, {b[1]} lần)')
# 2. Pascal
def pascal(t):
    d = [int(c) for c in dig(t)]
    while len(d) > 2: d = [(d[i] + d[i + 1]) % 10 for i in range(len(d) - 1)]
    return d[0] * 10 + d[1]
for si, (a, b) in enumerate(segs):
    vals = [(pascal(t - 1), t) for t in range(a, b)]; ok = [v in R[t] for v, t in vals if 1 <= v <= NB]
    print(f'**2. Cầu Pascal** ({"nửa trước" if si == 0 else "nửa gần"}): số Pascal hợp lệ {len(ok)}/{b - a} kỳ, ra {sum(ok) / max(len(ok), 1) * 100:.1f}%')
# 3. Lô kép, lô rơi, lô gan
kep = {n for n in range(11, NB + 1, 11)}
def rate(fn):
    out = []
    for a, b in segs:
        h = n = 0
        for t in range(a, b):
            g = fn(t); h += len(g & R[t]); n += len(g)
        out.append(h / max(n, 1) * 100)
    return ' · '.join(f'{x:.1f}%' for x in out)
def gap(t, n):
    g = 0
    while g < t and n not in R[t - 1 - g]: g += 1
    return g
print(f'**3. Lô kép** ({", ".join(map(str, sorted(kep)))}): {rate(lambda t: kep)}')
print(f'**4. Lô rơi** (số kỳ trước rơi lại): {rate(lambda t: R[t - 1])}')
print(f'**5. Lô gan** (vắng ≥{int(NB / KB * 3)} kỳ, gấp 3 nhịp bình quân): {rate(lambda t: {n for n in range(1, NB + 1) if gap(t, n) >= int(NB / KB * 3)})}')
print(f'**6. Đầu câm** (hàng chục vắng mặt kỳ trước) → kỳ này: {rate(lambda t: {n for n in range(1, NB + 1) if n // 10 not in {m // 10 for m in R[t - 1]}})}')
print(f'**7. Đuôi câm** (chữ số cuối vắng mặt kỳ trước) → kỳ này: {rate(lambda t: {n for n in range(1, NB + 1) if n % 10 not in {m % 10 for m in R[t - 1]}})}')

# ---------- Thêm các cách soi khác (05/10/2026) ----------
import datetime
dts = D['dates']
def dmy(t):
    d = datetime.datetime.strptime(dts[t][:10], '%d/%m/%Y'); return d.day, d.month
def kep_lien(t):
    ks = {n for n in R[t - 1] if n % 11 == 0}
    return {m for k in ks for m in (k - 11, k + 11) if 11 <= m <= NB}
def kep_canh(t):
    ks = {n for n in R[t - 1] if n % 11 == 0}
    return {m for k in ks for m in (k - 1, k + 1) if 1 <= m <= NB} - R[t - 1]
def kep_nuoi(t): return {n for n in R[t - 1] if n % 11 == 0}
def lo_kep_giua(t): return {a + 1 for a in R[t - 1] if a + 2 in R[t - 1] and a + 1 not in R[t - 1]}
def ngay(t):
    d, m = dmy(t); return {x for x in (d, m, d + m) if 1 <= x <= NB}
def cham_nhieu(t):
    from collections import Counter
    c = Counter(ch for n in R[t - 1] for ch in f'{n:02d}'); top = c.most_common(1)[0][0]
    return {n for n in range(1, NB + 1) if top in f'{n:02d}'} - R[t - 1]
def bach_thu(t):
    """Cầu vị trí đang chạy dài nhất (ít nhất 1 kỳ) — bạch thủ 1 số."""
    dig = lambda u: ''.join(f'{n:02d}' for n in sorted(R[u])); best = None
    for (i, j) in pairs:
        run = 0
        for back in range(1, 8):
            u = t - back; v = int(dig(u - 1)[i] + dig(u - 1)[j])
            if 1 <= v <= NB and v in R[u]: run += 1
            else: break
        v = int(dig(t - 1)[i] + dig(t - 1)[j])
        if run >= 1 and 1 <= v <= NB and (best is None or run > best[0]): best = (run, v)
    return {best[1]} if best else set()
print(f'\n**8. Bạch thủ** (cầu vị trí chạy dài nhất): {rate(bach_thu)}')
print(f'**9. Nuôi kép** (kép kỳ trước ra lại): {rate(kep_nuoi)} · **kép liền kề** (11↔22↔33): {rate(kep_lien)} · **cạnh kép** (kép ±1): {rate(kep_canh)}')
print(f'**10. Lô kẹp** (kỳ trước có a và a+2 → a+1): {rate(lo_kep_giua)}')
print(f'**11. Theo ngày dương** (số = ngày, tháng, ngày+tháng của kỳ quay): {rate(ngay)}')
print(f'**12. Chạm nhiều nhất** (chữ số xuất hiện nhiều nhất kỳ trước → các số chứa chữ số đó): {rate(cham_nhieu)}')
# xiên 2: cặp hay đi cùng nhất 100 kỳ → kỳ tới cả 2 cùng về?
from itertools import combinations
def xien(t):
    c = {}
    for u in range(t - 100, t):
        for p in combinations(sorted(R[u]), 2): c[p] = c.get(p, 0) + 1
    return max(c, key=lambda p: (c[p], p))
for a, b in segs:
    both = sum(set(xien(t)) <= R[t] for t in range(a, b)) / (b - a) * 100
    print(f'**13. Xiên 2** (cặp đi cùng nhiều nhất 100 kỳ, cả 2 cùng về): {both:.1f}% kỳ (bình thường {KB * (KB - 1) / NB / (NB - 1) * 100:.1f}%)')
