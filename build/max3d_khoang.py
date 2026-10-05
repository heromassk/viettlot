#!/usr/bin/env python3
"""Max 3D+ / Pro — 6 chữ số của 2 bộ ĐB (bộ 1 = ĐB quay trước, bộ 2 = ĐB quay sau):
mỗi vị trí (bộ 1 trăm/chục/đơn vị, bộ 2 trăm/chục/đơn vị) biến thiên thế nào và THU HẸP KHOẢNG chữ số kỳ tới.
Chấm từng kỳ trên 3 đoạn 100 kỳ gần → xa; khoảng k chữ số, chia đều = k×10%.
  python3 build/max3d_khoang.py [--file build/max3dpro_data.json]"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
f = sys.argv[sys.argv.index('--file') + 1] if '--file' in sys.argv else os.path.join(HERE, 'max3d_data.json')
D = json.load(open(f)); L = D['res']; T = len(L)
POS = [(b, h) for b in (0, 1) for h in (0, 1, 2)]
NAME = lambda b, h: f'Bộ {b + 1} · {["trăm", "chục", "đơn vị"][h]}'
dig = lambda t, b, h: int(L[t][b][h])
def cnt_pos(t, W, b, h): c = [0] * 10; [c.__setitem__(dig(u, b, h), c[dig(u, b, h)] + 1) for u in range(max(0, t - W), t)]; return c
def cnt_hang(t, W, h):   # cả 20 bộ cùng hàng (chung lồng bi)
    c = [0] * 10
    for u in range(max(0, t - W), t):
        for s in L[u]: c[int(s[h])] += 1
    return c
def topk(c, k): return set(sorted(range(10), key=lambda d: (-c[d], d))[:k])
def near(v, k):   # k chữ số gần v nhất (vòng 0–9)
    return set(sorted(range(10), key=lambda d: (min(abs(d - v), 10 - abs(d - v)), d))[:k])
def lin(v, k):    # khoảng liền k chữ số quanh v, không vòng
    lo = max(0, min(10 - k, v - k // 2)); return set(range(lo, lo + k))
M = {
    'Nhiều nhất ở chính vị trí, 20 kỳ': lambda t, b, h, k: topk(cnt_pos(t, 20, b, h), k),
    'Nhiều nhất ở chính vị trí, 50 kỳ': lambda t, b, h, k: topk(cnt_pos(t, 50, b, h), k),
    'Nhiều nhất ở chính vị trí, 100 kỳ': lambda t, b, h, k: topk(cnt_pos(t, 100, b, h), k),
    'Nhiều nhất cả hàng (20 bộ), 20 kỳ': lambda t, b, h, k: topk(cnt_hang(t, 20, h), k),
    'Nhiều nhất cả hàng (20 bộ), 50 kỳ': lambda t, b, h, k: topk(cnt_hang(t, 50, h), k),
    'Nhiều nhất cả hàng (20 bộ), 100 kỳ': lambda t, b, h, k: topk(cnt_hang(t, 100, h), k),
    'Quanh chữ số kỳ trước (vòng)': lambda t, b, h, k: near(dig(t - 1, b, h), k),
    'Quanh chữ số kỳ trước (khoảng liền)': lambda t, b, h, k: lin(dig(t - 1, b, h), k),
    'Quanh trung vị 10 kỳ': lambda t, b, h, k: lin(sorted(dig(u, b, h) for u in range(t - 10, t))[5], k),
    'Bỏ chữ số kỳ trước + ít nhất 20 kỳ': lambda t, b, h, k: set(range(10)) - {dig(t - 1, b, h)} - set(sorted(range(10), key=lambda d: (cnt_pos(t, 20, b, h)[d], -d))[:9 - k]) if k < 9 else set(range(10)) - {dig(t - 1, b, h)},
}
segs = [(T - 100, T), (T - 200, T - 100), (T - 300, T - 200)]
print(f'## {os.path.basename(f)} — 6 chữ số của 2 bộ ĐB, {T} kỳ ({D["dates"][0]} → {D["dates"][-1]})\n')
# biến thiên
print('### Biến thiên từng vị trí (300 kỳ gần)\n\n| Vị trí | TB | Đổi so với kỳ trước: giữ nguyên · ±1 · ±2–3 · ±4–5 (vòng) | Chữ số ra nhiều nhất / ít nhất 100 kỳ |\n|---|---|---|---|')
for b, h in POS:
    xs = [dig(t, b, h) for t in range(T - 300, T)]; ds = [min(abs(a - c), 10 - abs(a - c)) for a, c in zip(xs, xs[1:])]
    g = lambda lo, hi: sum(lo <= d <= hi for d in ds) / len(ds) * 100
    c = cnt_pos(T, 100, b, h); hi_ = max(range(10), key=lambda d: c[d]); lo_ = min(range(10), key=lambda d: c[d])
    print(f'| {NAME(b, h)} | {sum(xs) / len(xs):.2f} | {g(0, 0):.0f}% · {g(1, 1):.0f}% · {g(2, 3):.0f}% · {g(4, 5):.0f}% (chia đều 10 · 20 · 40 · 30) | {hi_} ({c[hi_]} lần) / {lo_} ({c[lo_]} lần) |')
for k in (5, 7):
    print(f'\n### Khoảng {k} chữ số — % kỳ chữ số rơi vào khoảng (chia đều {k * 10}%), TB 6 vị trí · từng đoạn gần → xa\n')
    print('| Cách thu hẹp | Đoạn 1 | Đoạn 2 | Đoạn 3 | Tệ nhất / tốt nhất trong 6 vị trí (đoạn 1) |\n|---|---|---|---|---|')
    for name, fn in M.items():
        segv = []; per = []
        for si, (a, b_) in enumerate(segs):
            hp = []
            for b, h in POS:
                hp.append(sum(dig(t, b, h) in fn(t, b, h, k) for t in range(a, b_)) / (b_ - a) * 100)
            segv.append(sum(hp) / 6)
            if si == 0: per = hp
        print(f'| {name} | ' + ' | '.join(f'{x:.1f}%' for x in segv) + f' | {min(per):.0f}% / {max(per):.0f}% |')
