# Thử nhiều cách chọn 2 số May Mắn Loto (anh 21/10/2026: "vẫn hơi kém"). Mỗi kỳ chỉ dùng dữ liệu trước nó.
import json
d = json.load(open('build/all_data.json'))['loto535']; LK = d['lk']; D = d['dates']; n = len(LK)
ses = lambda t: D[t][-3:]
def prev_s(t, k=1):
    g = ses(t); c = 0
    for u in range(t - 1, -1, -1):
        if D[u].endswith(g):
            c += 1
            if c == k: return u
def cnt(t, W, same=False):
    c = {k: 0 for k in range(1, 13)}; m = 0
    for u in range(t - 1, -1, -1):
        if same and not D[u].endswith(ses(t)): continue
        c[LK[u]] += 1; m += 1
        if m >= W: break
    return c
def lean(t):
    u = prev_s(t)
    if u is None: return None
    m = LK[u]
    if m >= 7: return lambda k: k < m
    if m <= 6 and ses(t) == '21h': return lambda k: k > m
def trans(t, W, same):
    c = {k: 0 for k in range(1, 13)}
    p = LK[prev_s(t)] if same else LK[t - 1]
    for u in range(max(1, t - W), t):
        if same:
            if not D[u].endswith(ses(t)): continue
            pu = prev_s(u)
            if pu is None: continue
            if LK[pu] == p: c[LK[u]] += 1
        elif LK[u - 1] == p: c[LK[u]] += 1
    return c
def gap(t):
    g = {}
    for k in range(1, 13):
        u = t - 1
        while u >= 0 and LK[u] != k: u -= 1
        g[k] = t - u
    return g
M = {}
def cu(t):   # cách đang dùng
    c10, c50, f = cnt(t, 10), cnt(t, 50), lean(t)
    ok = [k for k in range(1, 13) if abs(k - LK[t - 1]) <= 3]
    return sorted(ok, key=lambda k: (-c10[k] - (1 if f and f(k) else 0), -c50[k], k))[:2]
M['đang dùng'] = cu
M['nóng 20 kỳ'] = lambda t: sorted(range(1, 13), key=lambda k: (-cnt(t, 20)[k], k))[:2]
M['nóng cùng buổi 20'] = lambda t: sorted(range(1, 13), key=lambda k: (-cnt(t, 20, True)[k], k))[:2]
M['±3 cùng buổi'] = lambda t: (lambda m, c: sorted([k for k in range(1, 13) if abs(k - m) <= 3], key=lambda k: (-c[k], k))[:2])(LK[prev_s(t)], cnt(t, 10, True))
M['chiều + nóng 20'] = lambda t: (lambda f, c: sorted(range(1, 13), key=lambda k: (-(c[k] + (2 if f and f(k) else 0)), k))[:2])(lean(t), cnt(t, 20))
M['chuyển kỳ 200'] = lambda t: (lambda c: sorted(range(1, 13), key=lambda k: (-c[k], k))[:2])(trans(t, 200, False))
M['chuyển cùng buổi 300'] = lambda t: (lambda c: sorted(range(1, 13), key=lambda k: (-c[k], k))[:2])(trans(t, 300, True))
M['vắng lâu nhất'] = lambda t: (lambda g: sorted(range(1, 13), key=lambda k: (-g[k], k))[:2])(gap(t))
M['vắng 3–8 kỳ'] = lambda t: (lambda g, c: sorted([k for k in range(1, 13) if 3 <= g[k] <= 8] or list(range(1, 13)), key=lambda k: (-c[k], k))[:2])(gap(t), cnt(t, 50))
def combo(t):
    c10, c50, f, tr, g = cnt(t, 10), cnt(t, 50), lean(t), trans(t, 300, True), gap(t)
    s = {k: c10[k] + c50[k] / 5 + (1 if f and f(k) else 0) + tr[k] / 3 - (1 if g[k] == 1 else 0) for k in range(1, 13)}
    return sorted(range(1, 13), key=lambda k: (-s[k], k))[:2]
M['kết hợp'] = combo
print('Số kỳ 2 số May Mắn trúng (20 / 50 / 100 / 200 kỳ):')
for nm, f in M.items():
    r = []
    for W in (20, 50, 100, 200):
        r.append(sum(LK[t] in f(t) for t in range(n - W, n)))
    print(f'{nm:22s}', ' / '.join(map(str, r)))
