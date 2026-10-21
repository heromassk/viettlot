# Chọn cách gợi ý 2 số May Mắn riêng cho từng cách xem: cả 2 buổi / chỉ 13h / chỉ 21h (anh 21/10/2026)
# Mỗi cách: ±w quanh MM trước (của dãy đang xem), bỏ MM trước (tùy), xếp theo số lần ra c kỳ gần (+ chiều nghiêng + tổng/hiệu 2 kỳ trước)
import json, itertools
d = json.load(open('build/all_data.json'))['loto535']; LK = d['lk']; D = d['dates']; N = len(LK)
def seq(g): return [LK[i] for i in range(N) if g is None or D[i].endswith(g)]
def lean_f(s, i, g):   # chiều nghiêng theo MM kỳ trước cùng buổi (dãy s đã là 1 buổi khi g != None)
    m = s[i - 1]
    if m >= 7: return lambda k: k < m
    if m <= 6 and g == ' 21h': return lambda k: k > m
def pick(s, i, g, w, ex, cw, th, ln):
    p = s[i - 1]; c = {k: 0 for k in range(1, 13)}
    for u in range(max(0, i - cw), i): c[s[u]] += 1
    c50 = {k: 0 for k in range(1, 13)}
    for u in range(max(0, i - 50), i): c50[s[u]] += 1
    ok = [k for k in range(1, 13) if abs(k - p) <= w and not (ex and k == p)]
    TH = {s[i - 2] + p, abs(s[i - 2] - p)}
    f = lean_f(s, i, g) if ln and g else None
    return sorted(ok, key=lambda k: (-c[k] - (1 if f and f(k) else 0) - (th if k in TH else 0), -c50[k], k))[:2]
GRID = list(itertools.product((2, 3, 4, 12), (False, True), (10, 20), (0, 1, 2), (False, True)))
out = {}
for g, nm in ((None, 'cả 2 buổi'), (' 13h', 'chỉ 13h'), (' 21h', 'chỉ 21h')):
    s = seq(g); L = len(s); res = []
    for w, ex, cw, th, ln in GRID:
        if ln and not g: continue
        r = [sum(s[i] in pick(s, i, g, w, ex, cw, th, ln) for i in range(L - W, L)) for W in (20, 50, 100, 200)]
        res.append((r[1] + r[2] + r[3], r, (w, ex, cw, th, ln)))
    res.sort(key=lambda x: -x[0])
    print(nm)
    for sc, r, p in res[:5]: print('  ', ' / '.join(map(str, r)), p)
