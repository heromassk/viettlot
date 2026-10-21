# Thử thêm "chiều nghiêng" (âm dương) vào cách chọn 3 số May Mắn Loto (anh 21/10/2026)
# Cách cũ (goiy.py): ±3 quanh MM kỳ trước (liền 2 buổi), xếp theo số lần ra 10 kỳ, rồi 50 kỳ.
# Chiều nghiêng lấy theo MM kỳ trước CÙNG BUỔI m: 21h — m ≤6 → lớn hơn m, m ≥7 → nhỏ hơn m; 13h — chỉ m ≥7 → nhỏ hơn m.
import json
d = json.load(open('build/all_data.json'))['loto535']; LK = d['lk']; D = d['dates']
def ses_prev(t):
    g = D[t][-3:]
    for u in range(t - 1, -1, -1):
        if D[u].endswith(g): return LK[u]
def lean(t, mode):
    m = ses_prev(t); g = D[t][-3:]
    if m is None: return None
    if mode == 'chi21' and g != '21h': return None
    if m >= 7: return lambda k: k < m
    if m <= 6 and (g == '21h' or mode == 'ca2lv'): return lambda k: k > m
    return None
def pick(t, mode):
    c10 = {k: sum(LK[u] == k for u in range(max(0, t - 10), t)) for k in range(1, 13)}
    c50 = {k: sum(LK[u] == k for u in range(max(0, t - 50), t)) for k in range(1, 13)}
    ok = [k for k in range(1, 13) if abs(k - LK[t - 1]) <= 3]
    if mode == 'cu': return sorted(ok, key=lambda k: (-c10[k], -c50[k], k))[:3]
    f = lean(t, mode.replace('loc_', ''))
    if mode.startswith('loc_') and f:   # chỉ giữ số đúng chiều trong ±3, thiếu thì bù số ngoài chiều
        return sorted(ok, key=lambda k: (not f(k), -c10[k], -c50[k], k))[:3]
    return sorted(ok, key=lambda k: (-c10[k], -c50[k], k))[:3] if not f else sorted(ok, key=lambda k: (-c10[k] - (1 if f(k) else 0), -c50[k], k))[:3]
n = len(LK)
for mode in ('cu', 'ca2', 'chi21', 'loc_ca2', 'loc_chi21'):
    row = []
    for W in (20, 50, 100, 200):
        h = [LK[t] in pick(t, mode) for t in range(n - W, n)]
        p1 = [pick(t, mode)[0] == LK[t] for t in range(n - W, n)]
        row.append(f'{W}: {sum(h)}/{W} ({sum(h)/W*100:.0f}%) ưu tiên 1 {sum(p1)}')
    print(f'{mode:10s}', ' | '.join(row))
